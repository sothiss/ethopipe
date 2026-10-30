#!/usr/bin/env pwsh
<#
.SYNOPSIS
    EthoPipe Journey & AI Evolution Helper

.DESCRIPTION
    Lists, templates, or records session closing logs and AI reasoning evolution in JOURNEY.md.

.EXAMPLE
    .\scripts\journey.ps1 -Template
    .\scripts\journey.ps1 -List
    .\scripts\journey.ps1 -Timeline
    .\scripts\journey.ps1 -New "Institutional Task & Walkthrough Protocol" -Model "Gemini 3.8 Flash" -Hurdle "AI Governance" -Challenge "..." -Reasoning "..." -Pivot "..." -Milestone "..." -AiNote "..."
#>

[CmdletBinding(DefaultParameterSetName = "List")]
param(
    [Parameter(ParameterSetName = "List")]
    [switch]$List,

    [Parameter(ParameterSetName = "Template")]
    [switch]$Template,

    [Parameter(ParameterSetName = "Template")]
    [string]$Title = "Session Milestone",

    [Parameter(ParameterSetName = "Timeline")]
    [switch]$Timeline,

    [Parameter(ParameterSetName = "New", Mandatory = $true)]
    [string]$New,

    [Parameter(ParameterSetName = "New")]
    [string]$Model = "Gemini 3.8 Flash",

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
    [string]$AiNote = ""
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
} elseif ($PSCmdlet.ParameterSetName -eq "New") {
    & $python scripts/manage_journey.py new `
        --title "$New" `
        --model "$Model" `
        --hurdle "$Hurdle" `
        --challenge "$Challenge" `
        --reasoning "$Reasoning" `
        --pivot "$Pivot" `
        --milestone "$Milestone" `
        --ai-note "$AiNote"
} else {
    & $python scripts/manage_journey.py list
}
