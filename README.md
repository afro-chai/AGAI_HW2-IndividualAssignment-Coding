# AGAI HW2 — Individual Assignment (Coding): StockTrader

Course project: **competing LLM strategy agents** on shared market data, plus an **evaluator**, JSON outputs, and a comparative report. This is not a production trading system; the focus is **agent behavior**, disagreement, and clear orchestration.

## What’s in this repo

| Path | Purpose |
|------|---------|
| [`stocktrader/`](stocktrader/) | Application code, prompts, `requirements.txt`, generated `outputs/`, `report/` (PDFs) |
| [`Instructions/`](Instructions/) | Assignment brief and personal planning notes |

## Stack (high level)

- **Python**, **yfinance** (prices), optional **Alpha Vantage** (news sentiment)
- **Microsoft AutoGen** — parallel `AssistantAgent` runs with structured (Pydantic) outputs
- **Ollama** — local models; optional **LiteLLM** OpenAI-compatible proxy for multi-provider / capstone work

**Strategies:** News Sentiment Follower, Volatility Averse, and an extension agent (**Moral Trader**). **Bonuses:** historical `backtest.json`, third-agent analysis.

## Quick start

```powershell
git clone https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git
cd AGAI_HW2-IndividualAssignment-Coding
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r stocktrader\requirements.txt
```

Copy [`stocktrader/.env.example`](stocktrader/.env.example) to `.env`, set `ALPHAVANTAGE_API_KEY` if you use news, start **Ollama**, pull a model (e.g. `llama3.2`), then:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m stocktrader.src.main --tickers NVDA,TSLA,JNJ,KO --backtest
```

Pre-generated JSON may be included under `stocktrader/outputs/` for grading without API keys; re-run locally for fresh results.

## Full documentation

→ **[`stocktrader/README.md`](stocktrader/README.md)** — setup checklist, env vars, checkpoints, architecture, and honest scope notes (backtest heuristics vs live LLM).

## Author

**afro-chai** — [Individual Assignment — Coding](https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding)
