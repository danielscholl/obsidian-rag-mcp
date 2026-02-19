"""
Reasoning layer for semantic inference and conclusion extraction.

This module provides tools for extracting logical conclusions from indexed
content and building reasoning traces that connect related concepts.
"""

from .conclusion_store import ConclusionStore
from .extractor import ConclusionExtractor
from .models import ChunkContext, Conclusion, ConclusionType, ReasoningTrace

__all__ = [
    "Conclusion",
    "ConclusionType",
    "ReasoningTrace",
    "ChunkContext",
    "ConclusionExtractor",
    "ConclusionStore",
]
