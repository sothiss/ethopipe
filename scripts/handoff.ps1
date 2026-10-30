<#
.SYNOPSIS
    EthoPipe Cross-Model Agent Handoff & Code Companion Task Runner

.DESCRIPTION
    Runs the agent handoff generator, compiles telemetry, updates snapshots if needed,
    writes structured Markdown reports, and copies the catch-up prompt or companion brief
    to your clipboard. Supports interactive models (Claude, OpenAI, Cursor) and autonomous
    companions (Google Labs Jules, Copilot Workspace, Devin).

.PARAMETER Objective
    Immediate micro-objective or goal for the incoming agent.

.PARAMETER Completed
    Summary of work completed in the current session.

.PARAMETER InProgress
    Summary of in-flight or uncommitted work.

.PARAMETER NextSteps
    Immediate step-by-step actions for the incoming agent.

.PARAMETER Blockers
    Known blockers, warnings, or pitfalls to avoid.

.PARAMETER Notes
    Special instructions or directives for the incoming agent.

.PARAMETER TargetAgent
    Target model family (e.g. "Claude Code / Opus", "OpenAI o1 / GPT-4o", "Cursor", "Antigravity").

.PARAMETER Companion
    Generate a task brief specifically for an autonomous code companion (e.g. Jules).

.PARAMETER Jules
    Alias for -Companion targeting Google Labs Jules.

.PARAMETER CompanionType
    Companion task track: "bolt" (optimization), "sentinel" (security), "test", "feature", "refactor". Default: "bolt".

.PARAMETER TargetFiles
    Comma-separated list of files the companion is permitted to modify (e.g. "src/pipeline/models.py,tests/test_models.py").

.PARAMETER RunTests
    If specified, runs the pytest suite to verify real-time baseline in the telemetry.

.PARAMETER UpdateSnapshot
    If specified, re-generates docs/LLM_SNAPSHOT.md via scripts/compile_snapshot.py.

.PARAMETER NoCopy
    If specified, does not copy the prompt to the Windows clipboard.

.EXAMPLE
    .\scripts\handoff.ps1

.EXAMPLE
    .\scripts\handoff.ps1 -Jules -CompanionType bolt -Objective "Optimize Pydantic validator O(1) lookups" -TargetFiles "src/pipeline/models.py" -RunTests
#>

[CmdletBinding()]
param(
    [string]$Objective,
    [string]$Completed,
    [string]$InProgress,
    [string]$NextSteps,
    [string]$Blockers,
    [string]$Notes,
    [string]$TargetAgent = "Any (Claude / OpenAI / Cursor / Antigravity)",
    [switch]$Companion,
    [switch]$Jules,
    [ValidateSet("bolt", "sentinel", "test", "feature", "refactor")]
    [string]$CompanionType = "bolt",
    [string]$TargetFiles,
    [switch]$RunTests,
    [switch]$UpdateSnapshot,
    [switch]$NoCopy
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $root

$python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

$script = ".\scripts\generate_agent_handoff.py"

$cmdArgs = @()

if ($Objective) { $cmdArgs += "--objective", $Objective }
if ($Completed) { $cmdArgs += "--completed", $Completed }
if ($InProgress) { $cmdArgs += "--in-progress", $InProgress }
if ($NextSteps) { $cmdArgs += "--next-steps", $NextSteps }
if ($Blockers) { $cmdArgs += "--blockers", $Blockers }
if ($Notes) { $cmdArgs += "--notes", $Notes }
if ($TargetAgent) { $cmdArgs += "--target-agent", $TargetAgent }
if ($Companion -or $Jules) {
    $cmdArgs += "--companion"
    $cmdArgs += "--companion-type", $CompanionType
}
if ($TargetFiles) { $cmdArgs += "--target-files", $TargetFiles }
if ($RunTests) { $cmdArgs += "--run-tests" }
if ($UpdateSnapshot) { $cmdArgs += "--update-snapshot" }
if (-not $NoCopy) { $cmdArgs += "--copy" }

& $python $script @cmdArgs
