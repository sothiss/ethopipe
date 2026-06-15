# EthoPipe deployment automation script for GCP (PowerShell)
# Aligns with open-science reproducibility guidelines.

$ErrorActionPreference = "Stop"

$ProjectID = "gen-lang-client-0629166560"
$ServiceName = "ethopipe"
$Region = "us-central1"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "EthoPipe Windows Deployer: Deploying to Google Cloud Platform" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# Set active project
Write-Host "Setting active GCP project to: $ProjectID..."
& gcloud config set project $ProjectID

function Deploy-CloudRun {
    Write-Host "Deploying EthoPipe to Google Cloud Run..." -ForegroundColor Green
    & gcloud run deploy $ServiceName `
        --source . `
        --region $Region `
        --allow-unauthenticated `
        --set-env-vars ETL_LOADER_TYPE=firestore
}

function Deploy-CloudFunction {
    Write-Host "Deploying EthoPipe to Google Cloud Functions (Gen 2)..." -ForegroundColor Green
    & gcloud functions deploy $ServiceName `
        --gen2 `
        --runtime=python312 `
        --region=$Region `
        --entry-point=app `
        --trigger-http `
        --allow-unauthenticated
}

Write-Host "Select deployment target:"
Write-Host "1) Google Cloud Run (Recommended)"
Write-Host "2) Google Cloud Functions (Gen 2)"
$Choice = Read-Host "Enter choice [1 or 2]"

if ($Choice -eq "1") {
    Deploy-CloudRun
} elseif ($Choice -eq "2") {
    Deploy-CloudFunction
} else {
    Write-Error "Invalid selection. Exiting."
}

Write-Host "Deployment completed successfully!" -ForegroundColor Green
