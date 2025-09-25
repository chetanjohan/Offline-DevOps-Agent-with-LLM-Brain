import types
from src.main import main


class DummyLLM:
    def __init__(self, model_path, device='cpu'):
        self.model_path = model_path

    def generate(self, prompt, max_tokens=128, temperature=1.0):
        return f"MOCKED: {prompt}"


def test_cli_query_monkeypatch(monkeypatch, tmp_path, capsys):
    # Monkeypatch the LocalLLM class in the llm.llm module
    dummy = DummyLLM
    monkeypatch.setitem(__import__('sys').modules, 'src.llm.llm', types.SimpleNamespace(LocalLLM=dummy))

    argv = ['--model-path', str(tmp_path), '--query', 'Hello world']
    main(argv)
    captured = capsys.readouterr()
    assert 'MOCKED: Hello world' in captured.out
