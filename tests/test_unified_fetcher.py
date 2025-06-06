import pandas as pd
import pytest
from modules.data import unified_fetcher as uf


def test_openbb_success(monkeypatch):
    sample = {
        "Ticker": "AAA",
        "Name": "Acme",
        "Sector": "Tech",
        "Industry": "Software",
        "Current Price": 1.0,
        "Market Cap": 2.0,
        "PE Ratio": pd.NA,
        "Dividend Yield": 0.0,
    }
    monkeypatch.setattr(uf, "_from_openbb", lambda t: sample)
    monkeypatch.setattr(uf, "fetch_basic_stock_data", lambda t: sample)
    monkeypatch.setattr(uf, "resolve_term", lambda x: x)
    result = uf.fetch_company_data("AAA")
    assert result == sample


def test_openbb_partial(monkeypatch):
    openbb = {
        "Ticker": "AAA",
        "Name": "Acme",
        "Sector": "",
        "Industry": "Software",
        "Current Price": pd.NA,
        "Market Cap": pd.NA,
        "PE Ratio": pd.NA,
        "Dividend Yield": pd.NA,
    }
    yf = {
        "Ticker": "AAA",
        "Name": "Acme",
        "Sector": "Tech",
        "Industry": "Software",
        "Current Price": 1.0,
        "Market Cap": 2.0,
        "PE Ratio": 10.0,
        "Dividend Yield": 0.1,
    }
    monkeypatch.setattr(uf, "_from_openbb", lambda t: openbb)
    monkeypatch.setattr(uf, "fetch_basic_stock_data", lambda t: yf)
    monkeypatch.setattr(uf, "resolve_term", lambda x: x)
    result = uf.fetch_company_data("AAA")
    assert result["Sector"] == "Tech"
    assert result["Current Price"] == 1.0


def test_yf_fallback(monkeypatch):
    data = {"Ticker": "AAA"}
    monkeypatch.setattr(uf, "_from_openbb", lambda t: None)
    monkeypatch.setattr(uf, "fetch_basic_stock_data", lambda t: data)
    monkeypatch.setattr(uf, "resolve_term", lambda x: x)
    assert uf.fetch_company_data("AAA") == data


def test_all_fail(monkeypatch):
    monkeypatch.setattr(uf, "_from_openbb", lambda t: None)
    monkeypatch.setattr(uf, "fetch_basic_stock_data", lambda t: (_ for _ in ()).throw(Exception("bad")))
    monkeypatch.setattr(uf, "resolve_term", lambda x: x)
    assert uf.fetch_company_data("AAA") is None


def test_no_openbb(monkeypatch):
    data = {"Ticker": "AAA"}
    def boom(t):
        raise AssertionError("should not call openbb")
    monkeypatch.setattr(uf, "_from_openbb", boom)
    monkeypatch.setattr(uf, "fetch_basic_stock_data", lambda t: data)
    monkeypatch.setattr(uf, "resolve_term", lambda x: x)
    assert uf.fetch_company_data("AAA", use_openbb=False) == data
