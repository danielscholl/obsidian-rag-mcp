"""
Conclusion extraction from text chunks using LLM.

Extracts deductive, inductive, and abductive conclusions from
indexed content to build a reasoning layer.
"""

import hashlib
import json
import logging
import os
from dataclasses import dataclass
from datetime import UTC, datetime

from openai import OpenAI

from .models import ChunkContext, Conclusion, ConclusionType

logger = logging.getLogger(__name__)


@dataclass
class ExtractorConfig:
    """Configuration for the conclusion extractor."""

    model: str = "gpt-4o-mini"
    max_conclusions_per_chunk: int = 5
    min_confidence: float = 0.5
    temperature: float = 0.3
    # Which conclusion types to extract
    extract_deductive: bool = True
    extract_inductive: bool = True
    extract_abductive: bool = False  # Most speculative, off by default
    # Batch processing
    batch_size: int = 5  # Number of chunks per LLM call
    max_batch_tokens: int = 12000  # Max tokens per batch (leave room for response)


EXTRACTION_PROMPT = '''Analyze this text and extract logical conclusions.

For each conclusion, identify:
1. The type:
   - "deductive" (logically certain)
   - "inductive" (pattern-based generalization)
   - "abductive" (best explanation)
2. A clear, concise statement of the conclusion
3. Confidence level (0.0 to 1.0)
4. Key evidence phrases from the text that support this conclusion

Context:
- Source file: {source_path}
- Section: {heading}
- Tags: {tags}

Text to analyze:
"""
{content}
"""

Extract up to {max_conclusions} conclusions. Focus on:
- Facts and relationships explicitly stated (deductive)
- Patterns that suggest general principles (inductive)
{abductive_instruction}

Respond with a JSON object containing a "conclusions" array:
{{
  "conclusions": [
    {{
      "type": "deductive|inductive|abductive",
      "statement": "The conclusion statement",
      "confidence": 0.85,
      "evidence": ["supporting phrase 1", "supporting phrase 2"]
    }}
  ]
}}

If no meaningful conclusions can be extracted, return: {{"conclusions": []}}
'''

BATCH_EXTRACTION_PROMPT = """Analyze multiple text chunks and extract logical conclusions from each.

For each conclusion, identify:
1. The type: "deductive", "inductive", or "abductive"
2. A clear, concise statement of the conclusion
3. Confidence level (0.0 to 1.0)
4. Key evidence phrases from the text
5. The chunk_id it came from

{abductive_instruction}

Chunks to analyze:
{chunks_json}

Respond with a JSON object mapping chunk_id to conclusions:
{{
  "results": {{
    "chunk_id_1": {{
      "conclusions": [
        {{
          "type": "deductive|inductive|abductive",
          "statement": "The conclusion",
          "confidence": 0.85,
          "evidence": ["phrase 1", "phrase 2"]
        }}
      ]
    }},
    "chunk_id_2": {{
      "conclusions": []
    }}
  }}
}}

Extract up to {max_conclusions} conclusions per chunk. Focus on meaningful insights.
"""


class ConclusionExtractor:
    """
    Extracts logical conclusions from text chunks using LLM.

    Features:
    - Configurable conclusion types (deductive, inductive, abductive)
    - Confidence thresholds
    - Structured output with evidence tracking
    """

    def __init__(
        self,
        api_key: str | None = None,
        config: ExtractorConfig | None = None,
    ):
        self.config = config or ExtractorConfig()
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

        if not self.client.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable."
            )

        logger.debug(f"Initialized extractor with model={self.config.model}")

    def extract_conclusions(
        self,
        chunk: str,
        chunk_id: str,
        context: ChunkContext,
    ) -> list[Conclusion]:
        """
        Extract conclusions from a text chunk.

        Args:
            chunk: The text content to analyze
            chunk_id: Unique identifier for the source chunk
            context: Metadata about the chunk's source

        Returns:
            List of extracted conclusions
        """
        if not chunk or not chunk.strip():
            return []

        # Build prompt
        abductive_instruction = (
            "- Hypotheses that best explain observations (abductive)"
            if self.config.extract_abductive
            else ""
        )

        prompt = EXTRACTION_PROMPT.format(
            source_path=context.source_path,
            heading=context.heading or "(no heading)",
            tags=", ".join(context.tags) if context.tags else "(no tags)",
            content=chunk[:8000],  # Limit content length
            max_conclusions=self.config.max_conclusions_per_chunk,
            abductive_instruction=abductive_instruction,
        )

        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Extract conclusions from text. Respond with JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.config.temperature,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                return []

            # Parse response
            data = json.loads(content)

            # Handle both array and object with array
            if isinstance(data, dict):
                raw_conclusions = data.get("conclusions", [])
            else:
                raw_conclusions = data

            # Convert to Conclusion objects
            conclusions = []
            now = datetime.now(UTC).isoformat()

            for raw in raw_conclusions:
                # Skip if below confidence threshold
                confidence = float(raw.get("confidence", 0))
                if confidence < self.config.min_confidence:
                    continue

                # Skip empty statements
                statement = raw.get("statement", "").strip()
                if not statement:
                    continue

                # Parse conclusion type
                type_str = raw.get("type", "deductive").lower()
                try:
                    conclusion_type = ConclusionType(type_str)
                except ValueError:
                    conclusion_type = ConclusionType.DEDUCTIVE

                # Skip types we're not extracting
                is_deductive = conclusion_type == ConclusionType.DEDUCTIVE
                is_inductive = conclusion_type == ConclusionType.INDUCTIVE
                is_abductive = conclusion_type == ConclusionType.ABDUCTIVE

                if is_deductive and not self.config.extract_deductive:
                    continue
                if is_inductive and not self.config.extract_inductive:
                    continue
                if is_abductive and not self.config.extract_abductive:
                    continue

                # Generate unique ID
                conclusion_id = self._generate_id(statement, chunk_id)

                conclusions.append(
                    Conclusion(
                        id=conclusion_id,
                        type=conclusion_type,
                        statement=statement,
                        confidence=confidence,
                        evidence=raw.get("evidence", []),
                        source_chunk_id=chunk_id,
                        context=context,
                        created_at=now,
                    )
                )

            logger.debug(
                f"Extracted {len(conclusions)} conclusions from chunk {chunk_id}"
            )
            return conclusions

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse LLM response as JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Error extracting conclusions: {e}")
            return []

    def _generate_id(self, statement: str, chunk_id: str) -> str:
        """Generate a unique ID for a conclusion."""
        content = f"{statement}:{chunk_id}"
        return hashlib.sha256(content.encode()).hexdigest()[:32]

    def extract_conclusions_batch(
        self,
        chunks: list[tuple[str, str, ChunkContext]],
    ) -> dict[str, list[Conclusion]]:
        """
        Extract conclusions from multiple chunks in a single LLM call.

        Args:
            chunks: List of (content, chunk_id, context) tuples

        Returns:
            Dict mapping chunk_id to list of conclusions
        """
        if not chunks:
            return {}

        # Filter empty chunks
        valid_chunks = [(c, cid, ctx) for c, cid, ctx in chunks if c and c.strip()]
        if not valid_chunks:
            return {}

        # Build chunks JSON for prompt
        chunks_data = []
        for content, chunk_id, context in valid_chunks:
            chunks_data.append(
                {
                    "chunk_id": chunk_id,
                    "source_path": context.source_path,
                    "heading": context.heading or "(no heading)",
                    "tags": context.tags,
                    "content": content[:2000],  # Limit per chunk in batch
                }
            )

        abductive_instruction = (
            "Include abductive conclusions (best explanations) when appropriate."
            if self.config.extract_abductive
            else "Focus on deductive and inductive conclusions only."
        )

        prompt = BATCH_EXTRACTION_PROMPT.format(
            chunks_json=json.dumps(chunks_data, indent=2),
            max_conclusions=self.config.max_conclusions_per_chunk,
            abductive_instruction=abductive_instruction,
        )

        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Extract conclusions from text chunks. Respond with JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.config.temperature,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                return {}

            data = json.loads(content)
            results_raw = data.get("results", {})

            # Build context lookup
            context_lookup = {cid: ctx for _, cid, ctx in valid_chunks}

            # Convert to Conclusion objects
            results: dict[str, list[Conclusion]] = {}
            now = datetime.now(UTC).isoformat()

            for chunk_id, chunk_results in results_raw.items():
                if chunk_id not in context_lookup:
                    continue

                context = context_lookup[chunk_id]
                raw_conclusions = chunk_results.get("conclusions", [])
                conclusions = []

                for raw in raw_conclusions:
                    confidence = float(raw.get("confidence", 0))
                    if confidence < self.config.min_confidence:
                        continue

                    statement = raw.get("statement", "").strip()
                    if not statement:
                        continue

                    type_str = raw.get("type", "deductive").lower()
                    try:
                        conclusion_type = ConclusionType(type_str)
                    except ValueError:
                        conclusion_type = ConclusionType.DEDUCTIVE

                    # Filter by enabled types
                    if (
                        conclusion_type == ConclusionType.DEDUCTIVE
                        and not self.config.extract_deductive
                    ):
                        continue
                    if (
                        conclusion_type == ConclusionType.INDUCTIVE
                        and not self.config.extract_inductive
                    ):
                        continue
                    if (
                        conclusion_type == ConclusionType.ABDUCTIVE
                        and not self.config.extract_abductive
                    ):
                        continue

                    conclusion_id = self._generate_id(statement, chunk_id)
                    conclusions.append(
                        Conclusion(
                            id=conclusion_id,
                            type=conclusion_type,
                            statement=statement,
                            confidence=confidence,
                            evidence=raw.get("evidence", []),
                            source_chunk_id=chunk_id,
                            context=context,
                            created_at=now,
                        )
                    )

                results[chunk_id] = conclusions

            total = sum(len(c) for c in results.values())
            logger.debug(
                f"Batch extracted {total} conclusions from {len(valid_chunks)} chunks"
            )
            return results

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse batch LLM response as JSON: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error in batch extraction: {e}")
            return {}
