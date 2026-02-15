"""Token counting utilities using tiktoken.

Provides accurate token counting for OpenAI models, with lazy-loading
of the encoder to avoid import-time overhead.
"""

import tiktoken

# Lazy-loaded encoder instance
_encoder: tiktoken.Encoding | None = None


def _get_encoder() -> tiktoken.Encoding:
    """Get or create the tiktoken encoder (lazy-loaded)."""
    global _encoder
    if _encoder is None:
        # Use cl100k_base which is used by gpt-4, gpt-3.5-turbo, text-embedding-ada-002
        _encoder = tiktoken.get_encoding("cl100k_base")
    return _encoder


def count_tokens(text: str) -> int:
    """
    Count the number of tokens in a text string.

    Uses tiktoken with cl100k_base encoding (compatible with GPT-4,
    GPT-3.5-turbo, and text-embedding models).

    Args:
        text: The text to count tokens for.

    Returns:
        The number of tokens in the text.
    """
    if not text:
        return 0
    encoder = _get_encoder()
    return len(encoder.encode(text))
