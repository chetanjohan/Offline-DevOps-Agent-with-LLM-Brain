"""Local LLM adapter using Hugging Face Transformers (local-only).

This module provides LocalLLM with a simple generate(prompt, ...) API. It
only imports heavy dependencies when used; if `transformers` is not
installed, it raises a helpful ImportError.
"""

from typing import Optional, Dict, Any


class LocalLLM:
    """Minimal adapter for a locally stored HF causal LM.

    Usage:
        llm = LocalLLM(model_path)
        text = llm.generate("Hello")
    """

    def __init__(self, model_path: str, device: str = "cpu"):
        self.model_path = model_path
        self.device = device
        self._loaded = False
        self._tokenizer = None
        self._model = None

    def load(self) -> None:
        """Load tokenizer and model from `model_path` using transformers.

        This method imports transformers lazily so projects that never call
        the LLM won't need the dependency installed.
        """
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
        except Exception as e:
            raise ImportError("transformers and torch are required to use the Transformers backend. Install them and try again.") from e

        # Use local_files_only to avoid network access
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        self._model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True)
        # Move to device if possible
        try:
            self._model.to(self.device)
        except Exception:
            pass

        self._loaded = True

    def generate(self, prompt: str, max_tokens: int = 128, temperature: float = 1.0, **kwargs) -> str:
        """Generate text from prompt.

        Args:
            prompt: Prompt text
            max_tokens: Maximum number of generated tokens
            temperature: Sampling temperature
        """
        if not self._loaded:
            self.load()

        # Local imports (we already validated in load)
        from transformers import logging
        import torch

        tokenizer = self._tokenizer
        model = self._model

        inputs = tokenizer(prompt, return_tensors="pt")
        # Move inputs to model device
        try:
            device = next(model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
        except Exception:
            pass

        # Generate
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=max_tokens, do_sample=temperature != 0.0, temperature=temperature)
        text = tokenizer.decode(out[0], skip_special_tokens=True)
        return text
