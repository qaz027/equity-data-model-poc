"""Fetch free equity prices into a clean DataFrame / CSV.

Uses yfinance (Yahoo Finance unofficial API). Fine for learning and FMI-style
practice models — not for live trading or compliance-sensitive work.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf

DOWNLOAD_DIR = Path(__file__).resolve().parents[1] / "data" / "downloads"
SAMPLE_PATH = Path(__file__).resolve().parents[1] / "data" / "sample" / "AAPL_sample.csv"


def fetch_prices(ticker: str, period: str = "5y") -> pd.DataFrame:
    """Download OHLCV history for one ticker."""
    ticker = ticker.upper().strip()
    raw = yf.download(ticker, period=period, auto_adjust=True, progress=False)

    if raw.empty:
        raise ValueError(f"No data returned for {ticker}. Check the symbol or try again later.")

    # yfinance sometimes returns MultiIndex columns; flatten to simple names.
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = [c[0] for c in raw.columns]

    df = raw.rename(columns=str.title)
    df = df.reset_index()
    # Date column name varies slightly across versions
    if "Date" not in df.columns and "Datetime" in df.columns:
        df = df.rename(columns={"Datetime": "Date"})
    df["Ticker"] = ticker
    cols = [c for c in ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"] if c in df.columns]
    return df[cols]


def save_prices(df: pd.DataFrame, ticker: str) -> Path:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = DOWNLOAD_DIR / f"{ticker.upper()}_prices.csv"
    df.to_csv(path, index=False)
    return path


def load_sample() -> pd.DataFrame:
    """Offline fallback so the project still demos without network."""
    return pd.read_csv(SAMPLE_PATH, parse_dates=["Date"])
