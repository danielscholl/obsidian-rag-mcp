"""
OpenAI embedding wrapper with batching and caching.
"""

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class EmbedderConfig:
    """Configuration for the embedder."""
    
    model: str = "text-embedding-3-small"
    batch_size: int = 100  # OpenAI allows up to 2048
    dimensions: Optional[int] = None  # Use model default


class OpenAIEmbedder:
    """
    Wrapper around OpenAI's embedding API.
    
    Features:
    - Batched embedding for efficiency
    - Configurable model and dimensions
    - Simple interface
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[EmbedderConfig] = None
    ):
        self.config = config or EmbedderConfig()
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
        # Validate API key
        if not self.client.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
    
    def embed_text(self, text: str) -> list[float]:
        """
        Embed a single text string.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        result = self.embed_texts([text])
        return result[0]
    
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple texts efficiently with batching.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        all_embeddings = []
        
        # Process in batches
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            
            # Clean texts (remove null bytes, excessive whitespace)
            batch = [self._clean_text(t) for t in batch]
            
            # Call OpenAI API
            kwargs = {
                "model": self.config.model,
                "input": batch,
            }
            if self.config.dimensions:
                kwargs["dimensions"] = self.config.dimensions
            
            response = self.client.embeddings.create(**kwargs)
            
            # Extract embeddings in order
            batch_embeddings = [None] * len(batch)
            for item in response.data:
                batch_embeddings[item.index] = item.embedding
            
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings
    
    def _clean_text(self, text: str) -> str:
        """Clean text for embedding."""
        # Remove null bytes
        text = text.replace('\x00', '')
        # Normalize whitespace
        text = ' '.join(text.split())
        # Truncate if too long (model limit is ~8191 tokens)
        max_chars = 30000  # ~7500 tokens with buffer
        if len(text) > max_chars:
            text = text[:max_chars]
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
