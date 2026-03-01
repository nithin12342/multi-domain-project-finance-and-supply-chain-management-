#!/bin/bash

# Deploy script for supply chain finance platform
# Usage: ./deploy.sh [environment]

set -e

ENVIRONMENT=$1
NAMESPACE="supply-chain"
SERVICES=("auth" "finance" "supplychain" "blockchain" "ai-analytics")

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(dev|staging|prod)$ ]]; then
    echo "Error: Environment must be dev, staging, or prod"
    exit 1
fi

# Load environment variables
source .env.$ENVIRONMENT

# Build and push Docker images
for service in "${SERVICES[@]}"; do
    echo "Building $service service..."
    docker build -t "supply-chain/$service-service:latest" \
        -f "devops/docker/$service.Dockerfile" \
        "backend/$service-service/"
    
    echo "Pushing $service service image..."
    docker push "supply-chain/$service-service:latest"
done

# Apply Kubernetes configurations
echo "Applying Kubernetes configurations..."

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply ConfigMaps and Secrets
kubectl apply -f "devops/k8s/config/$ENVIRONMENT/" -n $NAMESPACE

# Apply deployments
for service in "${SERVICES[@]}"; do
    kubectl apply -f "devops/k8s/deployments/$service-deploy.yaml" -n $NAMESPACE
    kubectl apply -f "devops/k8s/services/$service-svc.yaml" -n $NAMESPACE
done

# Apply ingress
kubectl apply -f "devops/k8s/ingress/ingress.yaml" -n $NAMESPACE

# Wait for deployments to be ready
for service in "${SERVICES[@]}"; do
    echo "Waiting for $service deployment to be ready..."
    kubectl rollout status deployment/$service-service -n $NAMESPACE
done

echo "Deployment to $ENVIRONMENT completed successfully!"
