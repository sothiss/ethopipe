#!/usr/bin/env pwsh
<#
.SYNOPSIS
    EthoPipe Journey, Task & Walkthrough Evolution Helper

.DESCRIPTION
    Lists, templates, archives session Task/Walkthrough snapshots into docs/walkthroughs/,
    or appends chronological AI reasoning entries to JOURNEY.md.

.EXAMPLE
    .\scripts\journey.ps1 -List
    .\scripts\journey.ps1 -Timeline
    .\scripts\journey.ps1 -Archive -Title "Solo Workflow Pruning" -Model "Gemini 4 (Medium)" -TaskFile "path\to\task.md" -WalkthroughFile "path\to\walkthrough.md"
    .\scripts\journey.ps1 -New "Solo Governance & Jules Sunset" -Model "Gemini 4 (Medium)" -WalkthroughRef "docs/walkthroughs/WALKTHROUGH_..." -Hurdle "..." -Challenge "..." -Reasoning "..." -Pivot "..." -Milestone "..." -AiNote "..."
#>

[CmdletBinding(DefaultParameterSetName = "List")]
param(
    [Parameter(ParameterSetName = "List")]
    [switch]$List,

    [Parameter(ParameterSetName = "Template")]
    [switch]$Template,

    [Parameter(ParameterSetName = "Template")]
    [Parameter(ParameterSetName = "Archive", Mandatory = $true)]
    [string]$Title = "Session Milestone",

    [Parameter(ParameterSetName = "Timeline")]
    [switch]$Timeline,

    [Parameter(ParameterSetName = "Archive", Mandatory = $true)]
    [switch]$Archive,

    [Parameter(ParameterSetName = "Archive")]
    [string]$Ide = "Google Antigravity IDE",

    [Parameter(ParameterSetName = "Archive")]
    [string]$TaskFile = "",

    [Parameter(ParameterSetName = "Archive")]
    [string]$WalkthroughFile = "",

    [Parameter(ParameterSetName = "New", Mandatory = $true)]
    [string]$New,

    [Parameter(ParameterSetName = "New")]
    [Parameter(ParameterSetName = "Template")]
    [Parameter(ParameterSetName = "Archive")]
    [string]$Model = "Gemini 4 (Medium)",

    [Parameter(ParameterSetName = "New")]
    [string]$Hurdle = "Architectural Refinement & Governance",

    [Parameter(ParameterSetName = "New")]
    [string]$Challenge = "",

    [Parameter(ParameterSetName = "New")]
    [string]$Reasoning = "",

    [Parameter(ParameterSetName = "New")]
    [string]$Pivot = "",

    [Parameter(ParameterSetName = "New")]
    [string]$Milestone = "",

    [Parameter(ParameterSetName = "New")]
    [string]$AiNote = "",

    [Parameter(ParameterSetName = "New")]
    [string]$WalkthroughRef = ""
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $root

$python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

if ($PSCmdlet.ParameterSetName -eq "Template") {
    & $python scripts/manage_journey.py template --title "$Title" --model "$Model"
} elseif ($PSCmdlet.ParameterSetName -eq "Timeline") {
    & $python scripts/manage_journey.py timeline
} elseif ($PSCmdlet.ParameterSetName -eq "Archive") {
    $cmdArgs = @("scripts/manage_journey.py", "archive", "--title", $Title, "--model", $Model, "--ide", $Ide)
    if ($TaskFile) { $cmdArgs += @("--task-file", $TaskFile) }
    if ($WalkthroughFile) { $cmdArgs += @("--walkthrough-file", $WalkthroughFile) }
    & $python @cmdArgs
} elseif ($PSCmdlet.ParameterSetName -eq "New") {
    $cmdArgs = @(
        "scripts/manage_journey.py", "new",
        "--title", $New,
        "--model", $Model,
        "--hurdle", $Hurdle,
        "--challenge", $Challenge,
        "--reasoning", $Reasoning,
        "--pivot", $Pivot,
        "--milestone", $Milestone,
        "--ai-note", $AiNote
    )
    if ($WalkthroughRef) { $cmdArgs += @("--walkthrough-ref", $WalkthroughRef) }
    & $python @cmdArgs
} else {
    & $python scripts/manage_journey.py list
}
