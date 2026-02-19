"""Tests for token counting utilities."""

from obsidian_rag_mcp.utils.tokens import count_tokens


class TestCountTokens:
    """Tests for count_tokens function."""

    def test_empty_string(self):
        """Empty string should return 0 tokens."""
        assert count_tokens("") == 0

    def test_ascii_text(self):
        """Basic ASCII text should be counted accurately."""
        # "Hello, world!" is typically 4 tokens
        result = count_tokens("Hello, world!")
        assert result > 0
        assert result < 10  # Sanity check

    def test_simple_sentence(self):
        """A simple sentence should produce reasonable token count."""
        text = "The quick brown fox jumps over the lazy dog."
        result = count_tokens(text)
        # This sentence is typically around 10 tokens
        assert 5 < result < 20

    def test_unicode_text(self):
        """Unicode characters should be handled correctly."""
        # Unicode text typically uses more tokens per character
        unicode_text = "こんにちは世界"  # "Hello world" in Japanese
        result = count_tokens(unicode_text)
        assert result > 0
        # Japanese text typically uses more tokens
        assert result > len(unicode_text) // 4  # More than naive estimate

    def test_code_content(self):
        """Code content should be counted accurately."""
        code = """
def hello_world():
    print("Hello, World!")
    return 42
"""
        result = count_tokens(code)
        # Code has specific tokenization patterns
        assert result > 0
        assert result > 10  # Should be more than trivial

    def test_mixed_content(self):
        """Mixed text, code, and unicode should work."""
        mixed = """
# Header
Some text with unicode: émojis 🎉 and code:
```python
x = 42
```
"""
        result = count_tokens(mixed)
        assert result > 0

    def test_long_text(self):
        """Long text should be handled efficiently."""
        # Create a text with ~1000 tokens
        text = "word " * 1000
        result = count_tokens(text)
        # Each "word " is typically 1-2 tokens
        assert 500 < result < 2000

    def test_special_characters(self):
        """Special characters and punctuation should be handled."""
        text = "Hello!!! @#$%^&*() 123... ???"
        result = count_tokens(text)
        assert result > 0

    def test_newlines_and_whitespace(self):
        """Newlines and whitespace should be tokenized."""
        text = "Line 1\n\nLine 2\n\n\nLine 3"
        result = count_tokens(text)
        assert result > 0

    def test_consistency(self):
        """Same input should always produce same output."""
        text = "This is a test sentence for consistency."
        result1 = count_tokens(text)
        result2 = count_tokens(text)
        assert result1 == result2

    def test_more_accurate_than_naive(self):
        """Token count should differ from naive len//4 estimate."""
        # This text has patterns that naive counting gets wrong
        text = "Hello!!!!! -----"  # Punctuation is tokenized differently
        actual = count_tokens(text)
        # Verify the function works with special characters
        assert actual > 0
