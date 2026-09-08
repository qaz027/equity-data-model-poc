# equity-data-model-poc

Small proof of concept: **pull free retail equity data into Python** and run a simple FMI-shaped model skeleton — **no Excel**.

Built for learning (boot.dev + FMI chops). Not a trading system.

## What it does

1. Downloads price history with [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo-backed, unofficial, free).
2. Saves a clean CSV under `data/downloads/`.
3. Prints return/vol summary stats.
4. Writes a stub valuation “one-sheet” (`*_model_skeleton.csv`) with labeled assumptions you can replace as you learn.

## Quick start

```bash
cd equity-data-model-poc
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Live download (needs network)
python scripts/run_poc.py --ticker AAPL --period 5y

# Offline demo (bundled sample)
python scripts/run_poc.py --offline
```

## Layout

- `scripts/run_poc.py` — one-command entry point
- `src/fetch_prices.py` — download / save / sample load
- `src/model_skeleton.py` — returns + stub valuation sheet
- `data/sample/` — tiny CSV so it runs without network
- `data/downloads/` — generated outputs (gitignored)

## Honest limits

- Free Yahoo data can be delayed, incomplete, or rate-limited.
- Fine for learning models; bad for live trading or anything compliance-sensitive.
- Institutional terminals exist because retail data is still painful — that’s the point of this POC.

## Next ideas

- Add fundamentals (free sources are messier than prices).
- Wire a second ticker for simple comps.
- Swap the stub sheet for a real FMI template as you learn it.
