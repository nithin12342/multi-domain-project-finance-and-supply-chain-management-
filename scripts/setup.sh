#!/bin/bash

# Setup script for development environment
# Usage: ./setup.sh

set -e

echo "Setting up development environment..."

# Install system dependencies
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    echo "Installing dependencies..."
    brew install java maven node docker kubernetes-cli
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Installing dependencies..."
    sudo apt-get update
    sudo apt-get install -y openjdk-17-jdk maven nodejs docker.io kubectl
fi

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Install Python dependencies
echo "Installing Python dependencies..."
python -m pip install -r backend/ai-analytics-service/requirements.txt

# Set up Docker containers for local development
echo "Setting up Docker containers..."
docker-compose up -d

# Create development database
echo "Setting up development database..."
psql -h localhost -U postgres -f database/postgres/init.sql

# Set up Kubernetes development namespace
echo "Setting up Kubernetes namespace..."
kubectl create namespace supply-chain-dev --dry-run=client -o yaml | kubectl apply -f -

# Install development certificates
echo "Installing development certificates..."
mkdir -p ~/.supply-chain/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ~/.supply-chain/certs/dev.key \
    -out ~/.supply-chain/certs/dev.crt \
    -subj "/CN=supply-chain.local"

echo "Development environment setup completed!"
echo "Run 'make run' to start the application"
