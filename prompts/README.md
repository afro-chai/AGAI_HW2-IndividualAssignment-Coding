# Prompts (grading)

**Canonical files** (loaded by `src/orchestration.py`):

| File | Agent |
|------|--------|
| `strategy_news_sentiment.txt` | News Sentiment Follower |
| `strategy_volatility_averse.txt` | Volatility Averse |
| `strategy_moral_trader.txt` | Moral Trader (extension) |
| `evaluator.txt` | Evaluator (compares structured outputs; see `src/evaluator.py` for agreement branching and deterministic `pattern_note`) |

Legacy duplicate filenames (`strategy_a.txt`, `strategy_b.txt`) were removed; JSON keys in outputs remain `strategy_a` / `strategy_b` for the graded pair.
