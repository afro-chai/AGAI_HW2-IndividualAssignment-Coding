#!/usr/bin/env bash
# Poll origin every 2 minutes; after a successful pull that advances HEAD, run the
# StockTrader pipeline (uses --tickers from code: DEFAULT_TICKERS after your desktop push).
#
# Run from Git Bash or WSL (not plain cmd.exe):
#   bash scripts/watch_git_and_run.sh
#
# API keys: never put them in this file. Use repo-root .env or
# secrets/alphavantage_api_key.txt (gitignored). For 10 tickers, consider
# ALPHAVANTAGE_MIN_INTERVAL_SEC in .env to reduce free-tier throttling.
#
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

INTERVAL_SEC="${WATCH_INTERVAL_SEC:-120}"
LOG_DIR="$REPO_ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/git_monitor.log"

log() {
  local line="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
  printf '%s\n' "$line" | tee -a "$LOG_FILE"
}

if [[ -f "$REPO_ROOT/.venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source "$REPO_ROOT/.venv/bin/activate"
elif [[ -f "$REPO_ROOT/.venv/Scripts/activate" ]]; then
  # shellcheck source=/dev/null
  source "$REPO_ROOT/.venv/Scripts/activate"
fi

export PYTHONPATH="$REPO_ROOT"
# Live LLM run (unset stub if present in environment)
unset STOCKTRADER_SKIP_LLM 2>/dev/null || true

PYTHON_CMD="${STOCKTRADER_PYTHON:-python}"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
REMOTE="${WATCH_REMOTE:-origin}"
LAST_HEAD="$(git rev-parse HEAD)"

log "Starting monitor: repo=$REPO_ROOT branch=$BRANCH remote=$REMOTE interval=${INTERVAL_SEC}s last_head=$LAST_HEAD"

while true; do
  git fetch "$REMOTE" 2>&1 | tee -a "$LOG_FILE"
  if [[ "${PIPESTATUS[0]}" -ne 0 ]]; then
    log "WARN: git fetch failed; retry in ${INTERVAL_SEC}s"
    sleep "$INTERVAL_SEC"
    continue
  fi

  git pull --rebase "$REMOTE" "$BRANCH" 2>&1 | tee -a "$LOG_FILE"
  if [[ "${PIPESTATUS[0]}" -ne 0 ]]; then
    log "WARN: git pull --rebase failed (local changes or conflict?); fix then retry. Sleeping ${INTERVAL_SEC}s"
    sleep "$INTERVAL_SEC"
    continue
  fi

  NOW_HEAD="$(git rev-parse HEAD)"
  if [[ "$NOW_HEAD" != "$LAST_HEAD" ]]; then
    log "HEAD advanced $LAST_HEAD -> $NOW_HEAD; running pipeline..."
    "$PYTHON_CMD" -m src.main --backtest --ticker-workers "${WATCH_TICKER_WORKERS:-2}" 2>&1 | tee -a "$LOG_FILE"
    RC=${PIPESTATUS[0]}
    if [[ "$RC" -ne 0 ]]; then
      log "WARN: python exited with $RC"
    else
      log "Pipeline finished OK"
    fi
    LAST_HEAD="$NOW_HEAD"
  else
    log "No new commits (HEAD=$NOW_HEAD)"
  fi

  sleep "$INTERVAL_SEC"
done
