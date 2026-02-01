"""
Core data models for the reasoning layer.

These types represent conclusions extracted from content and the
reasoning traces that connect them.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConclusionType(Enum):
    """Types of logical conclusions that can be extracted.
    
    Based on ADR-0004 Memory as Reasoning:
    - DEDUCTIVE: Logically certain given premises (if A→B and A, then B)
    - INDUCTIVE: Probable generalization from examples (pattern recognition)
    - ABDUCTIVE: Best explanation for observations (hypothesis generation)
    """
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"


@dataclass
class ChunkContext:
    """Context information about a source chunk.
    
    Provides metadata needed for conclusion extraction and tracing.
    """
    source_path: str
    title: str
    heading: str | None
    tags: list[str]
    chunk_index: int
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "title": self.title,
            "heading": self.heading,
            "tags": self.tags,
            "chunk_index": self.chunk_index,
        }


@dataclass
class Conclusion:
    """A logical conclusion extracted from content.
    
    Conclusions are the atomic units of reasoning - statements that
    can be derived from the source material with varying degrees
    of certainty.
    """
    id: str  # Unique identifier (hash of statement + source)
    type: ConclusionType
    statement: str  # The conclusion itself
    confidence: float  # 0.0 to 1.0
    evidence: list[str]  # Supporting text snippets from source
    source_chunk_id: str  # ID of the chunk this was extracted from
    context: ChunkContext
    
    # Optional metadata
    related_conclusions: list[str] = field(default_factory=list)  # IDs
    created_at: str | None = None
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "statement": self.statement,
            "confidence": round(self.confidence, 4),
            "evidence": self.evidence,
            "source_chunk_id": self.source_chunk_id,
            "context": self.context.to_dict(),
            "related_conclusions": self.related_conclusions,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Conclusion":
        """Reconstruct a Conclusion from a dictionary."""
        return cls(
            id=data["id"],
            type=ConclusionType(data["type"]),
            statement=data["statement"],
            confidence=data["confidence"],
            evidence=data["evidence"],
            source_chunk_id=data["source_chunk_id"],
            context=ChunkContext(**data["context"]),
            related_conclusions=data.get("related_conclusions", []),
            created_at=data.get("created_at"),
        )


@dataclass
class EvidenceChunk:
    """A chunk of text that serves as evidence for a conclusion."""
    chunk_id: str
    content: str
    relevance_score: float  # How relevant this evidence is (0-1)
    context: ChunkContext
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "content": self.content,
            "relevance_score": round(self.relevance_score, 4),
            "context": self.context.to_dict(),
        }


@dataclass
class ReasoningTrace:
    """A trace showing how conclusions connect and support each other.
    
    Traces provide explainability by showing the logical path
    from source evidence to derived conclusions.
    """
    conclusion: Conclusion
    supporting_evidence: list[EvidenceChunk]
    parent_conclusions: list[Conclusion]  # Conclusions this builds on
    child_conclusions: list[Conclusion]   # Conclusions derived from this
    confidence_path: float  # Combined confidence through the chain
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "conclusion": self.conclusion.to_dict(),
            "supporting_evidence": [e.to_dict() for e in self.supporting_evidence],
            "parent_conclusions": [c.to_dict() for c in self.parent_conclusions],
            "child_conclusions": [c.to_dict() for c in self.child_conclusions],
            "confidence_path": round(self.confidence_path, 4),
        }


@dataclass
class ConnectedConclusion:
    """A conclusion with its relationship to another conclusion or query."""
    conclusion: Conclusion
    relationship: str  # 'supports', 'contradicts', 'extends', 'similar'
    strength: float    # 0-1 relationship strength
    shared_evidence: list[str]  # Common source chunk IDs
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "conclusion": self.conclusion.to_dict(),
            "relationship": self.relationship,
            "strength": round(self.strength, 4),
            "shared_evidence": self.shared_evidence,
        }
