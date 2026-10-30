#!/usr/bin/env pwsh
<#
.SYNOPSIS
    EthoPipe Project Goals & State Management Utility

.DESCRIPTION
    Inspects live state, records dated session checkpoints, and maintains
    a historical timeline of stopping points to make project resumption seamless.

.EXAMPLE
    # View current status, goals, and quick-resume step:
    .\scripts\state.ps1

    # Record a new stopping point checkpoint:
    .\scripts\state.ps1 -Checkpoint -Focus "Storage Adapter" -StoppedAt "Finished schema definition; models.py line 180" -NextStep "Implement persist_star_schema() in src/pipeline/storage.py"

    # View historical checkpoints:
    .\scripts\state.ps1 -History
#>

[CmdletBinding(DefaultParameterSetName = "Status")]
param(
    [Parameter(ParameterSetName = "Status")]
    [switch]$Status,

    [Parameter(ParameterSetName = "History")]
    [switch]$History,

    [Parameter(ParameterSetName = "Checkpoint", Mandatory = $true)]
    [switch]$Checkpoint,

    [Parameter(ParameterSetName = "Checkpoint", Mandatory = $true)]
    [string]$Focus,

    [Parameter(ParameterSetName = "Checkpoint", Mandatory = $true)]
    [string]$StoppedAt,

    [Parameter(ParameterSetName = "Checkpoint", Mandatory = $true)]
    [string]$NextStep,

    [Parameter(ParameterSetName = "Checkpoint")]
    [string]$Phase = "Phase 4 (JOSS Publication, Zenodo Minting & Architectural Hardening)",

    [Parameter(ParameterSetName = "Checkpoint")]
    [string[]]$Goals = @()
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $root

$python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

$script = "scripts/manage_project_state.py"

if ($History) {
    & $python $script history
    exit $LASTEXITCODE
}

if ($Checkpoint) {
    $cmdArgs = @($script, "checkpoint", "--focus", $Focus, "--stopped-at", $StoppedAt, "--next-step", $NextStep, "--phase", $Phase)
    foreach ($g in $Goals) {
        $cmdArgs += @("--goal", $g)
    }
    & $python $cmdArgs
    exit $LASTEXITCODE
}

# Default: Status
& $python $script status
exit $LASTEXITCODE
