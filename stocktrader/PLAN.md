# StockTrader plan (execution stack)

## Decisions

- **Agents:** [AutoGen](https://microsoft.github.io/autogen/) `AssistantAgent` with **structured Pydantic outputs**, **parallel** `asyncio.gather` (no inter-strategy messaging).
- **Models:** **Ollama** locally via `OllamaChatCompletionClient`; optional **LiteLLM** OpenAI-compatible proxy via `LITELLM_BASE_URL` (see `src/llm_factory.py`).
- **Strategies:** News Sentiment Follower (`strategy_a`), Volatility Averse (`strategy_b`), extension Moral Trader (`strategy_c`).
- **Bonuses:** `outputs/backtest.json` (deterministic heuristic scorecard, documented); third agent in JSON + evaluator.
- **LangChain/LangGraph:** Optional add-on later (RAG/tools); not required for HW2.

## Remote

Push to: [https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git](https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git)

```bash
git remote add origin https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git
```
