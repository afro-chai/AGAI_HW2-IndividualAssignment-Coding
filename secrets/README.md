# Local secrets (never committed)

Put your Alpha Vantage API key **only on your machine**:

1. Create a file named **`alphavantage_api_key.txt`** in this folder (`secrets/`).
2. Put **nothing** in the file except the key on **one line** (no `KEY=` prefix, no quotes).
3. Save. The file is listed in `.gitignore` — do not commit it.

Alternatively, use repo-root **`.env`** with `ALPHAVANTAGE_API_KEY=...` (also gitignored).

Optional override: set environment variable **`ALPHAVANTAGE_KEY_FILE`** to a full or repo-relative path if you use a different filename.

**If this key was ever pasted into chat or a ticket, regenerate it** at [Alpha Vantage](https://www.alphavantage.co/support/#api-key).
