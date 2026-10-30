#!/usr/bin/env pwsh
<#
.SYNOPSIS
    EthoPipe Step-Gated Idea & Task Pipeline Helper

.DESCRIPTION
    Creates, lists, or audits ideas without skipping steps.

.EXAMPLE
    .\scripts\idea.ps1 -New "Vectorize DwC motor syllable parser" -Track bolt
    .\scripts\idea.ps1 -List
    .\scripts\idea.ps1 -Audit
    .\scripts\idea.ps1 -Board
#>

[CmdletBinding(DefaultParameterSetName = "List")]
param(
    [Parameter(ParameterSetName = "New", Mandatory = $true)]
    [string]$New,

    [Parameter(ParameterSetName = "New")]
    [ValidateSet("bolt", "sentinel", "feat", "refactor", "docs")]
    [string]$Track = "feat",

    [Parameter(ParameterSetName = "List")]
    [switch]$List,

    [Parameter(ParameterSetName = "Audit")]
    [switch]$Audit,

    [Parameter(ParameterSetName = "Board")]
    [switch]$Board
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $root

$python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

if ($PSCmdlet.ParameterSetName -eq "New") {
    & $python scripts/manage_ideas.py new "$New" --track $Track
} elseif ($PSCmdlet.ParameterSetName -eq "Audit") {
    & $python scripts/manage_ideas.py audit
} elseif ($PSCmdlet.ParameterSetName -eq "Board") {
    & $python scripts/manage_ideas.py board
} else {
    & $python scripts/manage_ideas.py list
}
