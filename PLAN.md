# StockTrader — project plan and status

## Status at a glance

### Done

- **Implementation:** [AutoGen](https://microsoft.github.io/autogen/) `AssistantAgent` with structured Pydantic outputs; parallel `asyncio.gather` (no cross-talk between strategies before evaluation). See `src/orchestration.py`, `src/strategies.py`, `src/evaluator.py`.
- **Models:** Ollama via `OllamaChatCompletionClient`; optional LiteLLM via `LITELLM_*` in `src/llm_factory.py`.
- **Strategies:** News Sentiment Follower, Volatility Averse, Moral Trader (`strategy_c`); bonus backtest in `src/backtest.py` → `outputs/backtest.json`.
- **Alpha Vantage:** Key obtained; stored only in **local** `.env` (gitignored). Integration notes: [`docs/ALPHA_VANTAGE.md`](docs/ALPHA_VANTAGE.md). Code: `src/market_data.py` (NEWS_SENTIMENT, optional env tuning in `.env.example`).
- **Docs pushed:** `README.md`, `docs/HANDOFF_NEXT_AGENT.md`, `docs/ALPHA_VANTAGE.md`, `docs/assets/README.md`, `.env.example` updates. (Welcome/key screenshot path is **gitignored** — not in repo.)
- **Report sources in repo:** `report/comparative_analysis.tex`, `report/ai_use_appendix.tex`, `report/LATEX_BUILD.md`, `report/report_checklist.md`.

### Left to do

- [ ] Replicate **`.env`** on the **laptop** (same `ALPHAVANTAGE_API_KEY` as desktop); do not commit.
- [ ] On laptop (Ollama): `git pull`, activate venv, unset `STOCKTRADER_SKIP_LLM`, run  
  `python -m src.main --tickers NVDA,TSLA,JNJ,KO --backtest`
- [ ] **Commit and push** updated `outputs/*.json` after the live run.
- [ ] **Compile** report + AI appendix PDFs per `report/LATEX_BUILD.md` and rubric; add/commit PDFs under `report/` if required for submission.
- [ ] **Pull** on the other machine so all clones match `origin/master`.

**Continuity:** [`docs/HANDOFF_NEXT_AGENT.md`](docs/HANDOFF_NEXT_AGENT.md) (desktop ↔ laptop, secrets).

---

## Execution stack (original decisions)

- **Agents:** AutoGen `AssistantAgent` with **structured Pydantic outputs**, **parallel** `asyncio.gather` (no inter-strategy messaging).
- **Models:** **Ollama** locally; optional **LiteLLM** OpenAI-compatible proxy via `LITELLM_BASE_URL`.
- **Strategies:** News Sentiment Follower (`strategy_a`), Volatility Averse (`strategy_b`), extension Moral Trader (`strategy_c`).
- **Bonuses:** `outputs/backtest.json` (deterministic heuristic scorecard); third agent in JSON + evaluator.
- **LangChain/LangGraph:** Optional later; not required for HW2.

## Remote

[https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git](https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git)

```bash
git remote add origin https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git
```
