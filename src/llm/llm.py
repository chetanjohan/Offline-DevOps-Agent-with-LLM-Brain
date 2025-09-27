"""LLaMA adapter using llama-cpp-python (gguf) with a small, lazy wrapper.

This module exposes a `generate_text(prompt, model_path, max_tokens)` helper
which initializes a singleton `llama_cpp.Llama` client on first use. The
import of `llama_cpp` is lazy so importing this module does not require the
native dependency to be installed.

If you prefer a class-based API, `LlamaLLM` is also provided.
"""

from typing import Optional

# Module-level singleton for the Llama client
_LLAMA_CLIENT = None


def _init_llama(model_path: str = "models/llama-2-7b-chat.Q4_K_M.gguf"):
    """Lazily import and initialize a llama_cpp.Llama instance.

    Raises ImportError if `llama_cpp` (llama-cpp-python) is not installed.
    """
    global _LLAMA_CLIENT
    if _LLAMA_CLIENT is not None:
        return _LLAMA_CLIENT

    try:
        from llama_cpp import Llama
    except Exception as e:
        raise ImportError(
            "llama_cpp (llama-cpp-python) is required for the LLaMA backend. "
            "Install it (pip install llama-cpp-python) and ensure you have a "
            "compatible GGUF model file.") from e

    # Initialize the model client. This will try to open the GGUF file; if the
    # path is invalid or the file is incompatible, the underlying library will
    # raise an informative error.
    _LLAMA_CLIENT = Llama(model_path=model_path)
    return _LLAMA_CLIENT


def generate_text(prompt: str, model_path: str = "models/llama-2-7b-chat.Q4_K_M.gguf", max_tokens: int = 200) -> str:
    """Generate text using a locally hosted LLaMA GGUF via llama-cpp-python.

    Args:
        prompt: Prompt string to send to the model.
        model_path: Path to the GGUF model file.
        max_tokens: Maximum number of tokens to generate.

    Returns:
        Generated text (string).

    Raises:
        ImportError: if llama_cpp is not available.
        Exception: propagated from the underlying llama client on failures.
    """
    client = _init_llama(model_path)

    # Call the client. llama-cpp-python accepts a callable-style usage where
    # the returned dict contains a 'choices' list with 'text'.
    out = client(prompt, max_tokens=max_tokens)
    try:
        return out["choices"][0]["text"]
    except Exception:
        # Be defensive: return a string representation if structure differs.
        return str(out)


class LlamaLLM:
    """Small object wrapper around the module-level Llama client.

    Usage:
        llm = LlamaLLM(model_path="models/...")
        text = llm.generate("Hello")
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or "models/llama-2-7b-chat.Q4_K_M.gguf"
        self._client = None

    def _ensure(self):
        if self._client is None:
            self._client = _init_llama(self.model_path)

    def generate(self, prompt: str, max_tokens: int = 200) -> str:
        self._ensure()
        out = self._client(prompt, max_tokens=max_tokens)
        try:
            return out["choices"][0]["text"]
        except Exception:
            return str(out)

