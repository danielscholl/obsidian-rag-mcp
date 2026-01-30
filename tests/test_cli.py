"""Tests for the CLI module."""

from click.testing import CliRunner

from src.cli.main import cli


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
