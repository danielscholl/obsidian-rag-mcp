"""Tests for the MCP server tool handlers."""

import json
from unittest.mock import Mock, patch

import pytest

from obsidian_rag_mcp.mcp.server import (
    handle_tool_call,
    validate_limit,
    validate_path,
    validate_query,
    validate_tags,
    validate_top_k,
)

# ---------------------------------------------------------------------------
# Validation function tests
# ---------------------------------------------------------------------------


class TestValidateTopK:
    """Test validate_top_k."""

    def test_none_returns_default(self):
        assert validate_top_k(None) == 5

    def test_valid_int(self):
        assert validate_top_k(10) == 10

    def test_string_int(self):
        assert validate_top_k("10") == 10

    def test_clamps_low(self):
        assert validate_top_k(0) == 1

    def test_clamps_high(self):
        assert validate_top_k(100) == 50

    def test_invalid_returns_default(self):
        assert validate_top_k("abc") == 5

    def test_custom_default(self):
        assert validate_top_k(None, default=10) == 10

    def test_boundary_min(self):
        assert validate_top_k(1) == 1

    def test_boundary_max(self):
        assert validate_top_k(50) == 50


class TestValidateLimit:
    """Test validate_limit."""

    def test_none_returns_default(self):
        assert validate_limit(None) == 10

    def test_valid_int(self):
        assert validate_limit(20) == 20

    def test_clamps_low(self):
        assert validate_limit(0) == 1

    def test_clamps_high(self):
        assert validate_limit(200) == 100

    def test_invalid_returns_default(self):
        assert validate_limit("abc") == 10


class TestValidateQuery:
    """Test validate_query."""

    def test_valid_query(self):
        assert validate_query("database issues") == "database issues"

    def test_strips_whitespace(self):
        assert validate_query("  query  ") == "query"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_query("")

    def test_none_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_query(None)

    def test_truncates_long_query(self):
        long_query = "x" * 20000
        result = validate_query(long_query)
        assert len(result) == 10000


class TestValidatePath:
    """Test validate_path."""

    def test_valid_path(self):
        assert validate_path("notes/test.md") == "notes/test.md"

    def test_strips_whitespace(self):
        assert validate_path("  notes/test.md  ") == "notes/test.md"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_path("")

    def test_none_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_path(None)


class TestValidateTags:
    """Test validate_tags."""

    def test_none_returns_empty(self):
        assert validate_tags(None) == []

    def test_valid_list(self):
        assert validate_tags(["rca", "p1"]) == ["rca", "p1"]

    def test_filters_empty_strings(self):
        assert validate_tags(["rca", "", "  "]) == ["rca"]

    def test_non_list_raises(self):
        with pytest.raises(ValueError, match="array"):
            validate_tags("rca")


# ---------------------------------------------------------------------------
# Tool handler tests
# ---------------------------------------------------------------------------


def _mock_search_response():
    """Create a mock search response."""
    mock = Mock()
    mock.to_dict.return_value = {
        "query": "test",
        "results": [],
        "total_chunks_searched": 100,
    }
    return mock


def _mock_stats():
    """Create a mock stats object."""
    mock = Mock()
    mock.to_dict.return_value = {
        "vault_path": "/vault",
        "total_files": 10,
        "total_chunks": 50,
    }
    return mock


class TestToolHandlers:
    """Test MCP tool handlers via handle_tool_call."""

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_search_vault(self, mock_engine):
        mock_engine.search.return_value = _mock_search_response()

        result = await handle_tool_call("search_vault", {"query": "database issues"})

        assert not result.isError
        mock_engine.search.assert_called_once()
        data = json.loads(result.content[0].text)
        assert "results" in data

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_search_vault_with_tags(self, mock_engine):
        mock_engine.search.return_value = _mock_search_response()

        result = await handle_tool_call(
            "search_vault", {"query": "issues", "top_k": 3, "tags": ["rca"]}
        )

        assert not result.isError
        call_kwargs = mock_engine.search.call_args
        assert call_kwargs.kwargs["tags"] == ["rca"]
        assert call_kwargs.kwargs["top_k"] == 3

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_search_by_tag(self, mock_engine):
        mock_engine.search.return_value = _mock_search_response()

        result = await handle_tool_call("search_by_tag", {"tags": ["rca", "p1"]})

        assert not result.isError
        mock_engine.search.assert_called_once()

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_search_by_tag_empty_tags(self, mock_engine):
        result = await handle_tool_call("search_by_tag", {"tags": []})

        assert result.isError
        assert "tag is required" in result.content[0].text

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_search_by_tag_with_query(self, mock_engine):
        mock_engine.search.return_value = _mock_search_response()

        result = await handle_tool_call(
            "search_by_tag", {"tags": ["rca"], "query": "database"}
        )

        assert not result.isError
        call_kwargs = mock_engine.search.call_args
        assert call_kwargs.kwargs["query"] == "database"

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_get_note_found(self, mock_engine):
        mock_engine.get_note.return_value = "# My Note\n\nContent here."

        result = await handle_tool_call("get_note", {"path": "notes/test.md"})

        assert not result.isError
        assert "My Note" in result.content[0].text

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_get_note_not_found(self, mock_engine):
        mock_engine.get_note.return_value = None

        result = await handle_tool_call("get_note", {"path": "missing.md"})

        assert result.isError
        assert "not found" in result.content[0].text

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_get_related(self, mock_engine):
        mock_engine.get_related.return_value = _mock_search_response()

        result = await handle_tool_call("get_related", {"path": "notes/test.md"})

        assert not result.isError
        mock_engine.get_related.assert_called_once()

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_list_recent(self, mock_engine):
        mock_engine.list_recent.return_value = [
            {"path": "note1.md", "modified": "2025-01-01"}
        ]

        result = await handle_tool_call("list_recent", {"limit": 5})

        assert not result.isError
        data = json.loads(result.content[0].text)
        assert len(data) == 1

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_list_recent_default_limit(self, mock_engine):
        mock_engine.list_recent.return_value = []

        result = await handle_tool_call("list_recent", {})

        assert not result.isError
        call_kwargs = mock_engine.list_recent.call_args
        assert call_kwargs.kwargs["limit"] == 10

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_index_status(self, mock_engine):
        mock_engine.get_stats.return_value = _mock_stats()

        result = await handle_tool_call("index_status", {})

        assert not result.isError
        data = json.loads(result.content[0].text)
        assert data["total_files"] == 10

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_search_with_reasoning(self, mock_engine):
        mock_response = Mock()
        mock_response.to_dict.return_value = {
            "query": "test",
            "results": [],
            "conclusions": [],
        }
        mock_engine.search_with_reasoning.return_value = mock_response

        result = await handle_tool_call(
            "search_with_reasoning", {"query": "auth failures"}
        )

        assert not result.isError
        mock_engine.search_with_reasoning.assert_called_once()

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_search_with_reasoning_filters(self, mock_engine):
        mock_response = Mock()
        mock_response.to_dict.return_value = {"results": [], "conclusions": []}
        mock_engine.search_with_reasoning.return_value = mock_response

        result = await handle_tool_call(
            "search_with_reasoning",
            {
                "query": "test",
                "conclusion_types": ["deductive", "inductive"],
                "min_confidence": 0.8,
                "tags": ["rca"],
            },
        )

        assert not result.isError
        call_kwargs = mock_engine.search_with_reasoning.call_args
        assert call_kwargs.kwargs["conclusion_types"] == ["deductive", "inductive"]
        assert call_kwargs.kwargs["min_confidence"] == 0.8

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_get_conclusion_trace_found(self, mock_engine):
        mock_engine.get_conclusion_trace.return_value = {
            "conclusion": {"id": "abc", "statement": "test"},
            "source_chunk": "some content",
        }

        result = await handle_tool_call(
            "get_conclusion_trace", {"conclusion_id": "abc123def456"}
        )

        assert not result.isError
        data = json.loads(result.content[0].text)
        assert "conclusion" in data

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_get_conclusion_trace_not_found(self, mock_engine):
        mock_engine.get_conclusion_trace.return_value = None

        result = await handle_tool_call(
            "get_conclusion_trace", {"conclusion_id": "nonexistent0000000000"}
        )

        assert result.isError
        assert "not found" in result.content[0].text

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_get_conclusion_trace_missing_id(self, mock_engine):
        result = await handle_tool_call("get_conclusion_trace", {})

        assert result.isError
        assert "required" in result.content[0].text

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_explore_connected_by_query(self, mock_engine):
        mock_engine.explore_connected_conclusions.return_value = {
            "conclusions": [],
        }

        result = await handle_tool_call(
            "explore_connected_conclusions", {"query": "auth patterns"}
        )

        assert not result.isError

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_explore_connected_by_id(self, mock_engine):
        mock_engine.explore_connected_conclusions.return_value = {"conclusions": []}

        result = await handle_tool_call(
            "explore_connected_conclusions",
            {"conclusion_id": "abc123def456789012345678"},
        )

        assert not result.isError

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_explore_connected_missing_both(self, mock_engine):
        result = await handle_tool_call("explore_connected_conclusions", {})

        assert result.isError
        assert "required" in result.content[0].text

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_unknown_tool(self, mock_engine):
        result = await handle_tool_call("nonexistent_tool", {})

        assert result.isError
        assert "Unknown tool" in result.content[0].text

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_validation_error_propagates(self, mock_engine):
        """Test that invalid query raises validation error."""
        result = await handle_tool_call("search_vault", {"query": ""})

        assert result.isError
        assert "Validation error" in result.content[0].text

    @pytest.mark.asyncio
    @patch("obsidian_rag_mcp.mcp.server._engine")
    async def test_engine_exception_handled(self, mock_engine):
        """Test that engine exceptions are caught and returned as errors."""
        mock_engine.search.side_effect = RuntimeError("ChromaDB connection lost")

        result = await handle_tool_call("search_vault", {"query": "test"})

        assert result.isError
        assert "ChromaDB connection lost" in result.content[0].text
