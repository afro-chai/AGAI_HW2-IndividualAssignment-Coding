# Run transcripts (`logs/`)

- **`full_run_<timestamp>.txt`** — produced by `scripts/run_full_with_log.ps1` (PowerShell `Start-Transcript`).
- **`full_run_latest.txt`** — copy of the most recent run (optional; may be updated each run).

**Security:** Before committing, confirm the transcript does **not** contain `ALPHAVANTAGE_API_KEY` or other secrets (avoid `echo`/`Get-Content .env` while transcribing).

**Sanitized placeholder:** If no machine-local transcript exists yet, `full_run_latest.txt` in git may be a short **sanitized summary** so other clones see run metadata; replace with a real transcript after you run locally.
