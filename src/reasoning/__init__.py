"""
Reasoning layer for semantic inference and conclusion extraction.

This module provides tools for extracting logical conclusions from indexed
content and building reasoning traces that connect related concepts.
"""

from .models import Conclusion, ConclusionType, ReasoningTrace, ChunkContext
from .extractor import ConclusionExtractor

__all__ = [
    "Conclusion",
    "ConclusionType", 
    "ReasoningTrace",
    "ChunkContext",
    "ConclusionExtractor",
]
