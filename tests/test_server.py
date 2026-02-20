"""Tests for the MCP server layer."""

import json
from unittest.mock import Mock, patch

import pytest

from obsidian_rag_mcp.mcp.server import (
    MAX_LIMIT,
    MAX_QUERY_LENGTH,
    MAX_TOP_K,
    MIN_LIMIT,
    MIN_TOP_K,
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
    """Test validate_top_k boundary conditions."""

    def test_none_returns_default(self):
        assert validate_top_k(None) == 5

    def test_none_returns_custom_default(self):
        assert validate_top_k(None, default=10) == 10

    def test_valid_int(self):
        assert validate_top_k(3) == 3

    def test_valid_string_int(self):
        assert validate_top_k("7") == 7

    def test_clamps_below_min(self):
        assert validate_top_k(0) == MIN_TOP_K
        assert validate_top_k(-5) == MIN_TOP_K

    def test_clamps_above_max(self):
        assert validate_top_k(100) == MAX_TOP_K
        assert validate_top_k(999) == MAX_TOP_K

    def test_boundary_values(self):
        assert validate_top_k(MIN_TOP_K) == MIN_TOP_K
        assert validate_top_k(MAX_TOP_K) == MAX_TOP_K

    def test_invalid_type_returns_default(self):
        assert validate_top_k("abc") == 5
        assert validate_top_k([1, 2]) == 5


class TestValidateLimit:
    """Test validate_limit boundary conditions."""

    def test_none_returns_default(self):
        assert validate_limit(None) == 10

    def test_none_returns_custom_default(self):
        assert validate_limit(None, default=20) == 20

    def test_valid_int(self):
        assert validate_limit(15) == 15

    def test_clamps_below_min(self):
        assert validate_limit(0) == MIN_LIMIT
        assert validate_limit(-1) == MIN_LIMIT

    def test_clamps_above_max(self):
        assert validate_limit(200) == MAX_LIMIT

    def test_boundary_values(self):
        assert validate_limit(MIN_LIMIT) == MIN_LIMIT
        assert validate_limit(MAX_LIMIT) == MAX_LIMIT

    def test_invalid_type_returns_default(self):
        assert validate_limit("abc") == 10


class TestValidateQuery:
    """Test validate_query validation."""

    def test_valid_query(self):
        assert validate_query("test query") == "test query"

    def test_strips_whitespace(self):
        assert validate_query("  test  ") == "test"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_query("")

    def test_none_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_query(None)

    def test_truncates_long_query(self):
        long_query = "x" * (MAX_QUERY_LENGTH + 100)
        result = validate_query(long_query)
        assert len(result) == MAX_QUERY_LENGTH

    def test_non_string_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_query(123)


class TestValidatePath:
    """Test validate_path validation."""

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
    """Test validate_tags validation."""

    def test_none_returns_empty(self):
        assert validate_tags(None) == []

    def test_valid_list(self):
        assert validate_tags(["rca", "p1"]) == ["rca", "p1"]

    def test_strips_tag_whitespace(self):
        assert validate_tags(["  rca  ", " p1 "]) == ["rca", "p1"]

    def test_filters_empty_tags(self):
        assert validate_tags(["rca", "", "  ", "p1"]) == ["rca", "p1"]

    def test_non_list_raises(self):
        with pytest.raises(ValueError, match="array"):
            validate_tags("rca")

    def test_converts_non_string_items(self):
        assert validate_tags([1, 2]) == ["1", "2"]


# ---------------------------------------------------------------------------
# Tool handler tests
# ---------------------------------------------------------------------------


def _mock_search_response():
    """Create a mock SearchResponse."""
    mock_resp = Mock()
    mock_resp.to_dict.return_value = {
        "query": "test",
        "results": [],
        "total_chunks_searched": 0,
    }
    return mock_resp


def _mock_stats():
    """Create a mock stats object."""
    mock_stats = Mock()
    mock_stats.to_dict.return_value = {"total_files": 5, "total_chunks": 100}
    return mock_stats


class TestSearchVault:
    """Test search_vault tool handler."""

    @pytest.mark.asyncio
    async def test_basic_search(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.search.return_value = _mock_search_response()

            result = await handle_tool_call("search_vault", {"query": "test"})

            assert not result.isError
            data = json.loads(result.content[0].text)
            assert "results" in data
            mock_engine.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_tags(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.search.return_value = _mock_search_response()

            result = await handle_tool_call(
                "search_vault", {"query": "test", "tags": ["rca"], "top_k": 3}
            )

            assert not result.isError
            mock_engine.search.assert_called_once_with(
                query="test", top_k=3, tags=["rca"]
            )

    @pytest.mark.asyncio
    async def test_empty_query_returns_error(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_get.return_value = Mock()

            result = await handle_tool_call("search_vault", {"query": ""})

            assert result.isError
            assert "Validation error" in result.content[0].text


class TestSearchByTag:
    """Test search_by_tag tool handler."""

    @pytest.mark.asyncio
    async def test_search_by_tag(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.search.return_value = _mock_search_response()

            result = await handle_tool_call("search_by_tag", {"tags": ["rca", "p1"]})

            assert not result.isError
            mock_engine.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_empty_tags_returns_error(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_get.return_value = Mock()

            result = await handle_tool_call("search_by_tag", {"tags": []})

            assert result.isError
            assert "At least one tag" in result.content[0].text

    @pytest.mark.asyncio
    async def test_tags_used_as_query_when_no_query(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.search.return_value = _mock_search_response()

            await handle_tool_call("search_by_tag", {"tags": ["rca", "p1"]})

            call_kwargs = mock_engine.search.call_args
            assert call_kwargs[1]["query"] == "rca p1"


class TestGetNote:
    """Test get_note tool handler."""

    @pytest.mark.asyncio
    async def test_note_found(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.get_note.return_value = "# Test Note\nContent here"

            result = await handle_tool_call("get_note", {"path": "test.md"})

            assert not result.isError
            assert "Test Note" in result.content[0].text

    @pytest.mark.asyncio
    async def test_note_not_found(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.get_note.return_value = None

            result = await handle_tool_call("get_note", {"path": "missing.md"})

            assert result.isError
            assert "not found" in result.content[0].text


class TestGetRelated:
    """Test get_related tool handler."""

    @pytest.mark.asyncio
    async def test_get_related(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.get_related.return_value = _mock_search_response()

            result = await handle_tool_call("get_related", {"path": "test.md"})

            assert not result.isError
            mock_engine.get_related.assert_called_once_with(path="test.md", top_k=5)


class TestListRecent:
    """Test list_recent tool handler."""

    @pytest.mark.asyncio
    async def test_list_recent_default(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.list_recent.return_value = [{"path": "a.md", "modified": 1234}]

            result = await handle_tool_call("list_recent", {})

            assert not result.isError
            data = json.loads(result.content[0].text)
            assert len(data) == 1
            mock_engine.list_recent.assert_called_once_with(limit=10)

    @pytest.mark.asyncio
    async def test_list_recent_custom_limit(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.list_recent.return_value = []

            await handle_tool_call("list_recent", {"limit": 25})

            mock_engine.list_recent.assert_called_once_with(limit=25)


class TestIndexStatus:
    """Test index_status tool handler."""

    @pytest.mark.asyncio
    async def test_index_status(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.get_stats.return_value = _mock_stats()

            result = await handle_tool_call("index_status", {})

            assert not result.isError
            data = json.loads(result.content[0].text)
            assert data["total_files"] == 5


class TestSearchWithReasoning:
    """Test search_with_reasoning tool handler."""

    @pytest.mark.asyncio
    async def test_basic_reasoning_search(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_resp = Mock()
            mock_resp.to_dict.return_value = {
                "query": "test",
                "results": [],
                "conclusions": [],
                "total_chunks_searched": 0,
                "total_conclusions_searched": 0,
            }
            mock_engine.search_with_reasoning.return_value = mock_resp

            result = await handle_tool_call("search_with_reasoning", {"query": "test"})

            assert not result.isError
            data = json.loads(result.content[0].text)
            assert "conclusions" in data

    @pytest.mark.asyncio
    async def test_reasoning_with_type_filter(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_resp = Mock()
            mock_resp.to_dict.return_value = {
                "query": "test",
                "results": [],
                "conclusions": [],
                "total_chunks_searched": 0,
                "total_conclusions_searched": 0,
            }
            mock_engine.search_with_reasoning.return_value = mock_resp

            await handle_tool_call(
                "search_with_reasoning",
                {
                    "query": "test",
                    "conclusion_types": ["deductive"],
                    "min_confidence": 0.5,
                },
            )

            call_kwargs = mock_engine.search_with_reasoning.call_args[1]
            assert call_kwargs["conclusion_types"] == ["deductive"]
            assert call_kwargs["min_confidence"] == 0.5


class TestGetConclusionTrace:
    """Test get_conclusion_trace tool handler."""

    @pytest.mark.asyncio
    async def test_trace_found(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.get_conclusion_trace.return_value = {
                "conclusion": {"id": "abc"},
                "supporting_evidence": [],
            }

            result = await handle_tool_call(
                "get_conclusion_trace", {"conclusion_id": "abc123"}
            )

            assert not result.isError

    @pytest.mark.asyncio
    async def test_trace_not_found(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.get_conclusion_trace.return_value = None

            result = await handle_tool_call(
                "get_conclusion_trace", {"conclusion_id": "missing"}
            )

            assert result.isError
            assert "not found" in result.content[0].text

    @pytest.mark.asyncio
    async def test_missing_conclusion_id(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_get.return_value = Mock()

            result = await handle_tool_call("get_conclusion_trace", {})

            assert result.isError
            assert "conclusion_id is required" in result.content[0].text


class TestExploreConnectedConclusions:
    """Test explore_connected_conclusions tool handler."""

    @pytest.mark.asyncio
    async def test_explore_with_query(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.explore_connected_conclusions.return_value = []

            result = await handle_tool_call(
                "explore_connected_conclusions", {"query": "test"}
            )

            assert not result.isError

    @pytest.mark.asyncio
    async def test_explore_with_conclusion_id(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.explore_connected_conclusions.return_value = []

            result = await handle_tool_call(
                "explore_connected_conclusions", {"conclusion_id": "abc"}
            )

            assert not result.isError

    @pytest.mark.asyncio
    async def test_explore_missing_both_params(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_get.return_value = Mock()

            result = await handle_tool_call("explore_connected_conclusions", {})

            assert result.isError
            assert "Either query or conclusion_id" in result.content[0].text


# ---------------------------------------------------------------------------
# Error handling and edge cases
# ---------------------------------------------------------------------------


class TestErrorHandling:
    """Test error handling in tool handlers."""

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_get.return_value = Mock()

            result = await handle_tool_call("nonexistent_tool", {})

            assert result.isError
            assert "Unknown tool" in result.content[0].text

    @pytest.mark.asyncio
    async def test_engine_exception_returns_error(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_engine = Mock()
            mock_get.return_value = mock_engine
            mock_engine.search.side_effect = RuntimeError("Database error")

            result = await handle_tool_call("search_vault", {"query": "test"})

            assert result.isError
            assert "Database error" in result.content[0].text

    @pytest.mark.asyncio
    async def test_engine_not_initialized(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_get.side_effect = RuntimeError("RAG engine not initialized")

            with pytest.raises(RuntimeError, match="not initialized"):
                await handle_tool_call("search_vault", {"query": "test"})

    @pytest.mark.asyncio
    async def test_missing_required_param(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_get.return_value = Mock()

            result = await handle_tool_call("search_vault", {})

            assert result.isError

    @pytest.mark.asyncio
    async def test_get_note_empty_path_returns_error(self):
        with patch("obsidian_rag_mcp.mcp.server.get_engine") as mock_get:
            mock_get.return_value = Mock()

            result = await handle_tool_call("get_note", {"path": ""})

            assert result.isError
            assert "Validation error" in result.content[0].text
