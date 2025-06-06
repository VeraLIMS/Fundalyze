import importlib
import sys
from types import SimpleNamespace

import modules.utils.openbb_utils as ou


def setup_dummy(monkeypatch, login_func):
    dummy = SimpleNamespace(account=SimpleNamespace(login=login_func))
    monkeypatch.setitem(sys.modules, "openbb", SimpleNamespace(obb=dummy))
    importlib.reload(ou)
    return dummy


def test_get_openbb_with_token(monkeypatch):
    calls = []

    def login(pat):
        calls.append(pat)

    dummy = setup_dummy(monkeypatch, login)
    monkeypatch.setenv("OPENBB_TOKEN", "tok")
    obb = ou.get_openbb()
    assert obb is dummy
    assert calls == ["tok"]
    ou.get_openbb()
    assert calls == ["tok"]


def test_get_openbb_no_token(monkeypatch, capsys):
    calls = []

    def login(pat):
        calls.append(pat)

    dummy = setup_dummy(monkeypatch, login)
    monkeypatch.delenv("OPENBB_TOKEN", raising=False)
    obb = ou.get_openbb()
    out = capsys.readouterr().out
    assert "OPENBB_TOKEN environment variable not set" in out
    assert calls == []
    assert obb is dummy
