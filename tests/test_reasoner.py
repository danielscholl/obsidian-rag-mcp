"""Tests for the reasoning layer."""

import pytest

from src.rag.reasoner import (
    Conclusion,
    ConclusionType,
    Premise,
    Reasoner,
    ReasonerConfig,
)


class TestConclusion:
    """Test Conclusion dataclass."""

    def test_to_dict(self):
        """Test conclusion serialization."""
        conclusion = Conclusion(
            text="The auth-service has recurring token issues",
            conclusion_type=ConclusionType.INDUCTIVE,
            certainty="likely based on multiple RCAs",
            premises=[
                Premise(
                    text="Token expired at peak time",
                    source_path="RCAs/rca-001.md",
                    chunk_index=2,
                )
            ],
            source_paths=["RCAs/rca-001.md"],
            tags=["auth", "rca"],
        )

        data = conclusion.to_dict()

        assert data["text"] == "The auth-service has recurring token issues"
        assert data["conclusion_type"] == "inductive"
        assert data["certainty"] == "likely based on multiple RCAs"
        assert len(data["premises"]) == 1
        assert data["premises"][0]["text"] == "Token expired at peak time"

    def test_from_dict(self):
        """Test conclusion deserialization."""
        data = {
            "text": "Test conclusion",
            "conclusion_type": "deductive",
            "certainty": "highly certain",
            "premises": [
                {
                    "text": "Premise text",
                    "source_path": "test.md",
                    "chunk_index": 0,
                }
            ],
            "source_paths": ["test.md"],
            "tags": ["test"],
        }

        conclusion = Conclusion.from_dict(data)

        assert conclusion.text == "Test conclusion"
        assert conclusion.conclusion_type == ConclusionType.DEDUCTIVE
        assert len(conclusion.premises) == 1


class TestConclusionType:
    """Test conclusion type enum."""

    def test_types(self):
        """Test all conclusion types exist."""
        assert ConclusionType.DEDUCTIVE.value == "deductive"
        assert ConclusionType.INDUCTIVE.value == "inductive"
        assert ConclusionType.ABDUCTIVE.value == "abductive"


class TestReasonerConfig:
    """Test reasoner configuration."""

    def test_defaults(self):
        """Test default configuration."""
        config = ReasonerConfig()
        assert config.model == "gpt-4o-mini"
        assert config.max_conclusions_per_chunk == 3
        assert config.enabled is True

    def test_disabled(self):
        """Test disabled configuration."""
        config = ReasonerConfig(enabled=False)
        assert config.enabled is False


class TestReasoner:
    """Test reasoner functionality."""

    def test_init_with_config(self):
        """Test reasoner initialization."""
        config = ReasonerConfig(enabled=False)
        reasoner = Reasoner(config=config)
        assert reasoner.config.enabled is False

    def test_disabled_returns_empty(self):
        """Test that disabled reasoner returns empty list."""
        config = ReasonerConfig(enabled=False)
        reasoner = Reasoner(config=config)

        conclusions = reasoner.extract_conclusions(
            content="Some test content",
            source_path="test.md",
            chunk_index=0,
        )

        assert conclusions == []

    def test_empty_content_returns_empty(self):
        """Test that empty content returns empty list."""
        reasoner = Reasoner(config=ReasonerConfig(enabled=True))

        conclusions = reasoner.extract_conclusions(
            content="",
            source_path="test.md",
            chunk_index=0,
        )

        assert conclusions == []

    def test_whitespace_only_returns_empty(self):
        """Test that whitespace-only content returns empty list."""
        reasoner = Reasoner(config=ReasonerConfig(enabled=True))

        conclusions = reasoner.extract_conclusions(
            content="   \n\t  ",
            source_path="test.md",
            chunk_index=0,
        )

        assert conclusions == []
