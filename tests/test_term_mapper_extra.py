import importlib
from modules.data import term_mapper


def test_suggest_with_openai_no_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = term_mapper._suggest_with_openai("tech", ["Technology"])
    assert result is None


def test_suggest_with_openai_no_module(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    monkeypatch.setattr(term_mapper, "openai", None)
    importlib.reload(term_mapper)  # ensure openai None used
    result = term_mapper._suggest_with_openai("tech", ["Technology"])
    assert result is None
