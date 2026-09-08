"""Simple FMI-flavored model skeleton in Python (no Excel).

Takes a price history and produces:
- return series + summary stats
- a stub "one-sheet" valuation table you can extend as you learn FMI
"""

from __future__ import annotations

import pandas as pd


def add_returns(prices: pd.DataFrame) -> pd.DataFrame:
    out = prices.copy()
    out = out.sort_values("Date")
    out["DailyReturn"] = out["Close"].pct_change()
    return out


def summary_stats(prices: pd.DataFrame) -> dict:
    r = prices["DailyReturn"].dropna()
    close = prices["Close"]
    trading_days = 252
    return {
        "ticker": prices["Ticker"].iloc[0] if "Ticker" in prices.columns else "?",
        "start": str(prices["Date"].min().date()),
        "end": str(prices["Date"].max().date()),
        "n_days": int(len(prices)),
        "last_close": float(close.iloc[-1]),
        "total_return": float(close.iloc[-1] / close.iloc[0] - 1),
        "ann_vol": float(r.std() * (trading_days**0.5)),
        "ann_return_approx": float(r.mean() * trading_days),
    }


def stub_valuation_sheet(last_close: float, shares_out_m: float = 15000.0) -> pd.DataFrame:
    """Tiny comps/DCF-shaped stub — placeholders for FMI practice.

    Replace the assumption cells as you learn the real frameworks.
    shares_out_m is millions of shares (AAPL-scale placeholder).
    """
    rows = [
        ("Price (last close)", last_close, "from market data"),
        ("Shares out (m) — ASSUMPTION", shares_out_m, "replace with real share count"),
        ("Market cap ($m)", last_close * shares_out_m, "price × shares"),
        ("Revenue TTM ($m) — ASSUMPTION", 400_000.0, "placeholder"),
        ("EBIT margin — ASSUMPTION", 0.30, "placeholder"),
        ("EBIT ($m)", 400_000.0 * 0.30, "rev × margin"),
        ("Tax rate — ASSUMPTION", 0.21, "placeholder"),
        ("NOPAT ($m)", 400_000.0 * 0.30 * (1 - 0.21), "EBIT × (1-t)"),
        ("WACC — ASSUMPTION", 0.09, "placeholder"),
        ("g — ASSUMPTION", 0.03, "perpetuity growth placeholder"),
        (
            "Stub terminal value ($m)",
            (400_000.0 * 0.30 * (1 - 0.21) * (1 + 0.03)) / (0.09 - 0.03),
            "NOPAT1 / (WACC - g) — teaching stub only",
        ),
    ]
    return pd.DataFrame(rows, columns=["Line", "Value", "Note"])
