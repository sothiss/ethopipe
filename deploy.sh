#!/usr/bin/env bash
# EthoPipe deployment automation script for GCP.
# Aligns with open-science reproducibility guidelines.

set -euo pipefail

# Configuration
PROJECT_ID="gen-lang-client-0629166560"
SERVICE_NAME="ethopipe"
REGION="us-central1"

echo "================================================================="
echo "EthoPipe Deployer: Deploying to Google Cloud Platform"
echo "================================================================="

# Set active project
echo "Setting active GCP project to: ${PROJECT_ID}..."
gcloud config set project "${PROJECT_ID}"

# Option for Cloud Run deployment (Recommended)
deploy_cloud_run() {
    echo "Deploying EthoPipe to Google Cloud Run..."
    gcloud run deploy "${SERVICE_NAME}" \
        --source . \
        --region "${REGION}" \
        --allow-unauthenticated \
        --set-env-vars ETL_LOADER_TYPE=firestore
}

# Option for Cloud Functions deployment
deploy_cloud_function() {
    echo "Deploying EthoPipe to Google Cloud Functions (Gen 2)..."
    gcloud functions deploy "${SERVICE_NAME}" \
        --gen2 \
        --runtime=python312 \
        --region="${REGION}" \
        --entry-point=app \
        --trigger-http \
        --allow-unauthenticated
}

# Main routing
echo "Select deployment target:"
echo "1) Google Cloud Run (Recommended)"
echo "2) Google Cloud Functions (Gen 2)"
read -r -p "Enter choice [1 or 2]: " choice

case $choice in
    1)
        deploy_cloud_run
        ;;
    2)
        deploy_cloud_function
        ;;
    *)
        echo "Invalid selection. Exiting."
        exit 1
        ;;
esac

echo "Deployment completed successfully!"
