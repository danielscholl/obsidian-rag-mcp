"""
OpenAI embedding wrapper with batching, retries, and logging.

Supports both OpenAI and Azure OpenAI endpoints. Azure OpenAI is auto-detected
when AZURE_OPENAI_ENDPOINT and AZURE_API_KEY environment variables are set.
"""

import logging
import os
from dataclasses import dataclass

import httpx
from openai import APIConnectionError, APITimeoutError, OpenAI, RateLimitError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


@dataclass
class EmbedderConfig:
    """Configuration for the embedder."""

    model: str = "text-embedding-3-small"
    batch_size: int = 100  # OpenAI allows up to 2048
    dimensions: int | None = None  # Use model default
    max_retries: int = 3
    query_max_chars: int = 8000  # Stricter limit for queries


def _create_openai_client(api_key: str | None = None) -> OpenAI:
    """
    Create an OpenAI client, auto-detecting Azure OpenAI when configured.

    Precedence:
    1. Explicit api_key parameter → standard OpenAI
    2. AZURE_OPENAI_ENDPOINT + AZURE_API_KEY → Azure OpenAI
    3. OPENAI_API_KEY env var → standard OpenAI
    """
    # Explicit api_key takes precedence over Azure env vars
    if api_key:
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        if azure_endpoint:
            logger.warning(
                "Explicit api_key provided; ignoring AZURE_OPENAI_ENDPOINT. "
                "Remove api_key to use Azure OpenAI."
            )
        return OpenAI(api_key=api_key)

    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    azure_api_key = os.getenv("AZURE_API_KEY", "")
    azure_api_version = os.getenv("AZURE_OPENAI_VERSION", "2024-10-21")
    azure_deployment = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")

    if azure_endpoint and azure_api_key:
        base_url = f"{azure_endpoint}/openai/deployments/{azure_deployment}"
        logger.info(f"Using Azure OpenAI endpoint: {azure_endpoint}")
        return OpenAI(
            api_key=azure_api_key,
            base_url=base_url,
            default_query={"api-version": azure_api_version},
            http_client=httpx.Client(
                headers={"api-key": azure_api_key},
            ),
        )

    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class OpenAIEmbedder:
    """
    Wrapper around OpenAI's embedding API.

    Features:
    - Batched embedding for efficiency
    - Automatic retries with exponential backoff
    - Configurable model and dimensions
    - Simple interface
    - Auto-detects Azure OpenAI via environment variables
    """

    def __init__(
        self, api_key: str | None = None, config: EmbedderConfig | None = None
    ):
        self.config = config or EmbedderConfig()
        self.client = _create_openai_client(api_key)

        # Validate API key
        if not self.client.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable "
                "or AZURE_OPENAI_ENDPOINT + AZURE_API_KEY for Azure OpenAI."
            )

        logger.debug(f"Initialized embedder with model={self.config.model}")

    def embed_text(self, text: str, is_query: bool = True) -> list[float]:
        """
        Embed a single text string.

        Args:
            text: Text to embed
            is_query: If True, apply stricter length limit for queries

        Returns:
            Embedding vector as list of floats
        """
        result = self.embed_texts([text], is_query=is_query)
        return result[0]

    def embed_texts(
        self, texts: list[str], is_query: bool = False
    ) -> list[list[float]]:
        """
        Embed multiple texts efficiently with batching.

        Args:
            texts: List of texts to embed
            is_query: If True, apply stricter length limits

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        all_embeddings = []
        total_batches = (
            len(texts) + self.config.batch_size - 1
        ) // self.config.batch_size

        logger.debug(f"Embedding {len(texts)} texts in {total_batches} batches")

        # Process in batches
        for batch_num, i in enumerate(range(0, len(texts), self.config.batch_size)):
            batch = texts[i : i + self.config.batch_size]

            # Clean texts (remove null bytes, excessive whitespace)
            max_chars = self.config.query_max_chars if is_query else 30000
            batch = [self._clean_text(t, max_chars) for t in batch]

            # Call OpenAI API with retries
            batch_embeddings = self._embed_batch(batch)
            all_embeddings.extend(batch_embeddings)

            logger.debug(f"Completed batch {batch_num + 1}/{total_batches}")

        return all_embeddings

    @retry(
        retry=retry_if_exception_type(
            (RateLimitError, APIConnectionError, APITimeoutError)
        ),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _embed_batch(self, batch: list[str]) -> list[list[float]]:
        """
        Embed a single batch with retry logic.

        Args:
            batch: List of cleaned texts to embed

        Returns:
            List of embedding vectors
        """
        kwargs = {
            "model": self.config.model,
            "input": batch,
        }
        if self.config.dimensions:
            kwargs["dimensions"] = self.config.dimensions

        response = self.client.embeddings.create(**kwargs)

        # Extract embeddings in order
        batch_embeddings: list[list[float] | None] = [None] * len(batch)
        for item in response.data:
            batch_embeddings[item.index] = item.embedding

        # Verify we got all embeddings back - fail explicitly if count doesn't match
        result = [e for e in batch_embeddings if e is not None]
        if len(result) != len(batch):
            raise RuntimeError(
                f"OpenAI returned {len(result)} embeddings for {len(batch)} inputs. "
                "This indicates content was filtered or an API error occurred."
            )
        return result

    def _clean_text(self, text: str, max_chars: int = 30000) -> str:
        """Clean text for embedding while preserving code structure."""
        import re

        # Remove null bytes
        text = text.replace("\x00", "")
        # Dedupe excessive blank lines (3+ -> 2) but preserve structure
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Strip trailing whitespace from lines
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        # Truncate if too long
        if len(text) > max_chars:
            text = text[:max_chars]
            logger.debug(f"Truncated text to {max_chars} characters")
        return text

    @property
    def embedding_dimension(self) -> int:
        """Get the embedding dimension for the current model."""
        if self.config.dimensions:
            return self.config.dimensions

        # Default dimensions by model
        defaults = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        return defaults.get(self.config.model, 1536)
