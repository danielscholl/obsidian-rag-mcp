"""
Reasoning layer for extracting conclusions from documents.

This module implements the "memory as reasoning" concept - treating
indexing as a reasoning task rather than just storage. It extracts
logical conclusions from document content that can be composed and
traversed at query time.

See ADR-0004 for the architectural rationale.
"""

import json
import logging
from dataclasses import dataclass, field
from enum import Enum

from openai import OpenAI

logger = logging.getLogger(__name__)


class ConclusionType(str, Enum):
    """Types of logical conclusions."""

    DEDUCTIVE = "deductive"  # Certain, from explicit statements
    INDUCTIVE = "inductive"  # Patterns from observations
    ABDUCTIVE = "abductive"  # Best explanations


@dataclass
class Premise:
    """A supporting premise for a conclusion."""

    text: str
    source_path: str
    chunk_index: int


@dataclass
class Conclusion:
    """A reasoned conclusion extracted from document content."""

    text: str
    conclusion_type: ConclusionType
    certainty: str  # Natural language certainty, not arbitrary scores
    premises: list[Premise] = field(default_factory=list)
    source_paths: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "text": self.text,
            "conclusion_type": self.conclusion_type.value,
            "certainty": self.certainty,
            "premises": [
                {
                    "text": p.text,
                    "source_path": p.source_path,
                    "chunk_index": p.chunk_index,
                }
                for p in self.premises
            ],
            "source_paths": self.source_paths,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Conclusion":
        """Create from dictionary."""
        return cls(
            text=data["text"],
            conclusion_type=ConclusionType(data["conclusion_type"]),
            certainty=data["certainty"],
            premises=[
                Premise(
                    text=p["text"],
                    source_path=p["source_path"],
                    chunk_index=p["chunk_index"],
                )
                for p in data.get("premises", [])
            ],
            source_paths=data.get("source_paths", []),
            tags=data.get("tags", []),
        )


@dataclass
class ReasonerConfig:
    """Configuration for the reasoner."""

    model: str = "gpt-4o-mini"
    max_conclusions_per_chunk: int = 3
    enabled: bool = True  # Can be disabled to skip reasoning


REASONING_PROMPT = """You are a reasoning system that extracts logical conclusions from document content.

Given the following document chunk, extract up to {max_conclusions} conclusions. For each conclusion:

1. **Type**: Classify as one of:
   - DEDUCTIVE: Certain conclusions from explicit statements in the text
   - INDUCTIVE: General patterns or trends you observe
   - ABDUCTIVE: Best explanations for behaviors or outcomes described

2. **Certainty**: Describe confidence in natural language (e.g., "highly certain", "likely", "possible", "speculative")

3. **Premises**: Quote the specific text that supports this conclusion

Focus on conclusions that would be useful for future queries about this codebase/knowledge base.

Document path: {source_path}
Document tags: {tags}

Content:
---
{content}
---

Respond with a JSON array of conclusions. Example format:
[
  {{
    "text": "The auth-service frequently experiences token expiration issues during peak traffic",
    "conclusion_type": "inductive",
    "certainty": "likely based on 3 RCAs mentioning this pattern",
    "premises": ["RCA mentions token timeout at 2pm", "Peak traffic correlates with auth failures"]
  }}
]

If no meaningful conclusions can be drawn, return an empty array: []
"""


class Reasoner:
    """
    Extracts logical conclusions from document chunks.

    The reasoner uses an LLM to analyze document content and extract
    deductive, inductive, and abductive conclusions that can be stored
    alongside raw chunks for richer retrieval.
    """

    def __init__(self, config: ReasonerConfig | None = None, api_key: str | None = None):
        self.config = config or ReasonerConfig()
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()

    def extract_conclusions(
        self,
        content: str,
        source_path: str,
        chunk_index: int,
        tags: list[str] | None = None,
    ) -> list[Conclusion]:
        """
        Extract conclusions from a document chunk.

        Args:
            content: The chunk content to analyze
            source_path: Path to the source document
            chunk_index: Index of this chunk in the document
            tags: Tags associated with the document

        Returns:
            List of Conclusion objects
        """
        if not self.config.enabled:
            return []

        if not content.strip():
            return []

        tags = tags or []

        try:
            prompt = REASONING_PROMPT.format(
                max_conclusions=self.config.max_conclusions_per_chunk,
                source_path=source_path,
                tags=", ".join(tags) if tags else "none",
                content=content,
            )

            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise reasoning system. Always respond with valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,  # Lower temperature for more consistent reasoning
                max_tokens=1000,
            )

            result_text = response.choices[0].message.content
            if not result_text:
                return []

            # Parse JSON response
            # Handle potential markdown code blocks
            if result_text.startswith("```"):
                lines = result_text.split("\n")
                result_text = "\n".join(lines[1:-1])

            conclusions_data = json.loads(result_text)

            conclusions = []
            for data in conclusions_data:
                try:
                    conclusion = Conclusion(
                        text=data["text"],
                        conclusion_type=ConclusionType(data["conclusion_type"].lower()),
                        certainty=data.get("certainty", "uncertain"),
                        premises=[
                            Premise(
                                text=p,
                                source_path=source_path,
                                chunk_index=chunk_index,
                            )
                            for p in data.get("premises", [])
                        ],
                        source_paths=[source_path],
                        tags=tags,
                    )
                    conclusions.append(conclusion)
                except (KeyError, ValueError) as e:
                    logger.warning(f"Failed to parse conclusion: {e}")
                    continue

            return conclusions

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse reasoning response as JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Error during reasoning: {e}")
            return []

    def reason_over_chunks(
        self,
        chunks: list[dict],
    ) -> list[Conclusion]:
        """
        Extract conclusions from multiple chunks.

        Args:
            chunks: List of chunk dictionaries with 'content', 'source_path', 
                   'chunk_index', and 'tags' keys

        Returns:
            List of all Conclusion objects extracted
        """
        all_conclusions = []

        for chunk in chunks:
            conclusions = self.extract_conclusions(
                content=chunk.get("content", ""),
                source_path=chunk.get("source_path", ""),
                chunk_index=chunk.get("chunk_index", 0),
                tags=chunk.get("tags", []),
            )
            all_conclusions.extend(conclusions)

        return all_conclusions
