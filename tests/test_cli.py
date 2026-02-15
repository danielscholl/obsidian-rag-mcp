"""Tests for the CLI module."""

import tempfile

from click.testing import CliRunner

from obsidian_rag_mcp.cli.main import cli


class TestCLI:
    """Test CLI commands."""

    def test_cli_help(self):
        """Test CLI shows help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Obsidian RAG" in result.output

    def test_cli_version(self):
        """Test CLI shows version."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestSearchValidation:
    """Test search command input validation."""

    def test_search_empty_query_error(self):
        """Test that empty query shows error message."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(cli, ["search", "", "--vault", tmpdir])
            assert result.exit_code != 0
            assert "Query cannot be empty" in result.output

    def test_search_whitespace_query_error(self):
        """Test that whitespace-only query shows error message."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(cli, ["search", "   ", "--vault", tmpdir])
            assert result.exit_code != 0
            assert "Query cannot be empty" in result.output

    def test_search_top_k_zero_error(self):
        """Test that top_k=0 shows error message."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                cli, ["search", "test", "--vault", tmpdir, "--top-k", "0"]
            )
            assert result.exit_code != 0
            assert "must be at least 1" in result.output

    def test_search_top_k_negative_error(self):
        """Test that negative top_k shows error message."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                cli, ["search", "test", "--vault", tmpdir, "--top-k", "-5"]
            )
            assert result.exit_code != 0
            assert "must be at least 1" in result.output

    def test_search_top_k_too_large_error(self):
        """Test that top_k > 50 shows error message."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                cli, ["search", "test", "--vault", tmpdir, "--top-k", "51"]
            )
            assert result.exit_code != 0
            assert "cannot exceed 50" in result.output

    def test_search_top_k_valid_boundary(self):
        """Test that top_k=1 and top_k=50 are accepted."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            # These should fail for other reasons (no API key, etc.)
            # but should not fail on the top_k validation
            result_min = runner.invoke(
                cli, ["search", "test", "--vault", tmpdir, "--top-k", "1"]
            )
            result_max = runner.invoke(
                cli, ["search", "test", "--vault", tmpdir, "--top-k", "50"]
            )
            # Should not contain top_k validation errors
            assert "must be at least 1" not in result_min.output
            assert "cannot exceed 50" not in result_max.output
