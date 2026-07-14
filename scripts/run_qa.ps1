#!/usr/bin/env pwsh
# EthoPipe Automated Quality Assurance Runner
# Run from the project root: .\scripts\run_qa.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $root

$venv = ".\.venv\Scripts"
$failures = @()

function Step($n, $title) {
    Write-Host ""
    Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  Step $n — $title" -ForegroundColor Cyan
    Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan
}

function Run($cmd) {
    Write-Host "> $cmd" -ForegroundColor DarkGray
    Invoke-Expression $cmd
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE"
    }
}

# Step 1: Environment Audit
Step 1 "Pre-Execution Environment Audits"
try {
    Run "uv pip list"
    Run "uv audit"
} catch {
    Write-Warning "Step 1 failed: $_"
    $failures += "Step 1: Environment Audit"
}

# Step 2: Format & Style Gates
Step 2 "Format & Style Gates"
try {
    Run "$venv\ruff.exe format --check src tests"
    Run "$venv\ruff.exe check src tests"
} catch {
    Write-Warning "Step 2 failed: $_"
    $failures += "Step 2: Format & Style"
}

# Step 3: Type Safety (Mypy)
Step 3 "Type Safety Checks (Mypy)"
try {
    Run "$venv\mypy.exe src"
} catch {
    Write-Warning "Step 3 failed (mypy may need installing: uv pip install mypy pandas-stubs): $_"
    $failures += "Step 3: Type Safety"
}

# Step 4: Full Test Suite
Step 4 "Full Test Suite with Coverage"
try {
    Run "$venv\pytest.exe tests/ --cov=src --cov-report=term-missing"
} catch {
    Write-Warning "Step 4 failed: $_"
    $failures += "Step 4: Test Suite"
}

# Step 5: Adversarial Boundary Audit
Step 5 "Adversarial Boundary Audit (Hypothesis)"
try {
    Run "$venv\pytest.exe tests/test_adversarial_boundaries.py -v"
} catch {
    Write-Warning "Step 5 failed: $_"
    $failures += "Step 5: Adversarial Boundaries"
}

# Step 6: Pre-Commit Hook Enforcement
Step 6 "Git Hook Enforcement (pre-commit)"
try {
    $gitCheck = & git --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "git not found on PATH. Run pre-commit from a terminal where 'git --version' works."
    }
    Run "$venv\pre-commit.exe run --all-files"
} catch {
    Write-Warning "Step 6 failed: $_"
    $failures += "Step 6: Pre-Commit Hooks"
}

# Summary
Write-Host ""
Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  QA Summary" -ForegroundColor Cyan
Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan

if ($failures.Count -eq 0) {
    Write-Host "  All 6 steps passed." -ForegroundColor Green
    exit 0
} else {
    Write-Host "  Failed steps:" -ForegroundColor Red
    $failures | ForEach-Object { Write-Host "    x $_" -ForegroundColor Red }
    exit 1
}
