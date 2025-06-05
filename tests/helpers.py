from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

@dataclass
class Dummy:
    """Simple wrapper returning a dataframe via :meth:`to_df`."""

    df: pd.DataFrame

    def to_df(self) -> pd.DataFrame:
        """Return the wrapped dataframe."""
        return self.df


def make_fake_obb(profile_df: pd.DataFrame, price_df: pd.DataFrame, stmt_df: pd.DataFrame, calls: dict | None = None):
    """Return a fake OpenBB client using the given dataframes.

    Parameters
    ----------
    profile_df : pandas.DataFrame
        Data to return from the profile API.
    price_df : pandas.DataFrame
        Data to return from the price API.
    stmt_df : pandas.DataFrame
        Data to return from fundamental APIs.
    calls : dict | None
        Optional dictionary to capture call arguments from the fake APIs.

    Returns
    -------
    object
        A fake OpenBB client instance mimicking the required API surface.
    """

    class FakeEquity:
        def __init__(self) -> None:
            class _Profile:
                def __call__(self, symbol: str) -> Dummy:
                    return Dummy(profile_df)

            class _Price:
                def historical(self, symbol: str, period: str, provider: str | None = None) -> Dummy:
                    if calls is not None:
                        calls["period"] = period
                    return Dummy(price_df)

            class _Fundamental:
                def income(self, symbol: str, period: str) -> Dummy:
                    return Dummy(stmt_df)

                def balance(self, symbol: str, period: str) -> Dummy:
                    return Dummy(stmt_df)

                def cash(self, symbol: str, period: str) -> Dummy:
                    return Dummy(stmt_df)

            self.profile = _Profile()
            self.price = _Price()
            self.fundamental = _Fundamental()

    class FakeOBB:
        def __init__(self) -> None:
            self.equity = FakeEquity()

    return FakeOBB()
