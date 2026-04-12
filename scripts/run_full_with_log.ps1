# Full live run (no STOCKTRADER_SKIP_LLM) with transcript log.
# Usage (from repo root):
#   .\scripts\run_full_with_log.ps1
#   .\scripts\run_full_with_log.ps1 -Tickers "PLTR,TTE,GOLD"
#
# Time: ~15–35 min typical for default five tickers (20 Ollama calls + yfinance + Alpha Vantage).
# Requires: repo-root .env with ALPHAVANTAGE_API_KEY for news (optional but recommended).

param(
    [string]$Tickers = "PLTR,TTE,GOLD,LMT,FRO"
)

$ErrorActionPreference = "Continue"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDir = Join-Path $RepoRoot "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir "full_run_$stamp.txt"
$latest = Join-Path $logDir "full_run_latest.txt"

Write-Host "Repo: $RepoRoot"
Write-Host "Log:  $logFile"
Write-Host "Estimate: ~15–35 min for 5 tickers (hardware dependent)."
if (-not (Test-Path (Join-Path $RepoRoot ".env"))) {
    Write-Warning "No .env at repo root — Alpha Vantage key may be missing. Copy .env.example to .env"
}

Remove-Item Env:STOCKTRADER_SKIP_LLM -ErrorAction SilentlyContinue
$env:PYTHONPATH = $RepoRoot

$py = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    throw "Python venv not found at $py — run: python -m venv .venv ; pip install -r requirements.txt"
}

Start-Transcript -Path $logFile -Force
try {
    Write-Host "Started: $(Get-Date -Format o)"
    & $py -m src.main --tickers $Tickers --backtest --ticker-workers 2
    $code = $LASTEXITCODE
    Write-Host "Exit code: $code"
    Write-Host "Finished: $(Get-Date -Format o)"
    exit $code
}
finally {
    Stop-Transcript | Out-Null
    Copy-Item -Path $logFile -Destination $latest -Force
    Write-Host "Latest log copy: $latest"
}
