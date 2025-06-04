import pandas as pd
import modules.data.compare as cmp


def test_interactive_profile_choose_yf(monkeypatch):
    obb_df = pd.DataFrame([{"longName": "Alpha", "sector": "Tech", "industry": "Soft", "marketCap": 1, "website": "a"}])
    yf_df = pd.DataFrame([{"longName": "Alpha", "sector": "Finance", "industry": "Bank", "marketCap": 2, "website": "b"}])
    monkeypatch.setattr(cmp, "fetch_profile_openbb", lambda s: obb_df)
    monkeypatch.setattr(cmp, "fetch_profile_yf", lambda s: yf_df)
    monkeypatch.setattr("builtins.input", lambda *_: "y")
    result = cmp.interactive_profile("AAA")
    assert result.iloc[0]["sector"] == "Finance"

