#!/bin/bash

# Set script to exit immediately if a command fails
set -e

echo "🚀 Starting ShowBuddy application with Docker..."

# Check if .env file exists, create it if not
if [ ! -f .env ]; then
  echo "Creating .env file..."
  cat > .env << EOL
# API Keys for services (replace with your actual keys)
ASSEMBLYAI_API_KEY=
SPREADLY_API_KEY=
ANTHROPIC_API_KEY=

# Other configuration
SPREADLY_MOCK_TEST=true
USE_MOCK_SERVICES=false
EOL

  echo "⚠️  Created .env file. Please edit it to add your API keys before continuing."
  exit 1
fi

# Ensure data directory exists
if [ ! -d "./showbuddy-data" ]; then
  echo "Creating data directory..."
  mkdir -p ./showbuddy-data
fi

# Start all containers in detached mode
echo "Starting containers..."
docker compose up --build -d

echo "✅ Services are starting:"
echo "   - Python Backend: http://localhost:8000"
echo "   - React Frontend: http://localhost:3000"
echo ""
echo "Use 'docker compose logs -f' to view logs"
echo "Use 'docker compose down' to stop all services"