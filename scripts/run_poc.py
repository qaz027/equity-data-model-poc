#!/usr/bin/env python3
"""One-command POC: fetch retail equity data → Python model skeleton."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fetch_prices import fetch_prices, load_sample, save_prices  # noqa: E402
from model_skeleton import add_returns, stub_valuation_sheet, summary_stats  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description="Retail equity data → Python model skeleton (no Excel)")
    p.add_argument("--ticker", default="AAPL", help="Ticker symbol (default: AAPL)")
    p.add_argument("--period", default="5y", help="yfinance period, e.g. 1y, 5y, max")
    p.add_argument("--offline", action="store_true", help="Use bundled sample CSV (no network)")
    args = p.parse_args()

    print(f"\n=== Equity data → model POC ===")
    print(f"Ticker: {args.ticker.upper()} | period: {args.period} | offline: {args.offline}\n")

    if args.offline:
        prices = load_sample()
        print(f"Loaded sample rows: {len(prices)} from data/sample/")
    else:
        try:
            prices = fetch_prices(args.ticker, period=args.period)
            path = save_prices(prices, args.ticker)
            print(f"Downloaded {len(prices)} rows → {path}")
        except Exception as e:
            print(f"Download failed ({e}). Falling back to sample data.\n")
            prices = load_sample()

    prices = add_returns(prices)
    stats = summary_stats(prices)

    print("--- Price summary ---")
    for k, v in stats.items():
        if isinstance(v, float):
            print(f"  {k}: {v:,.4f}" if abs(v) < 10 else f"  {k}: {v:,.2f}")
        else:
            print(f"  {k}: {v}")

    sheet = stub_valuation_sheet(stats["last_close"])
    out_dir = ROOT / "data" / "downloads"
    out_dir.mkdir(parents=True, exist_ok=True)
    sheet_path = out_dir / f"{stats['ticker']}_model_skeleton.csv"
    sheet.to_csv(sheet_path, index=False)

    print("\n--- Stub valuation sheet (FMI-shaped placeholders) ---")
    print(sheet.to_string(index=False))
    print(f"\nWrote {sheet_path}")
    print("\nNext: edit assumptions in model_skeleton.py as you learn FMI.")
    print("Remember: free Yahoo-backed data is for learning, not production trading.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
