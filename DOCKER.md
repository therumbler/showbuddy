# Running ShowBuddy with Docker

This document explains how to run the ShowBuddy application using Docker.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine
- API keys for required services:
  - AssemblyAI API key for audio transcription
  - Spreadly API key for business card scanning
  - Anthropic API key for report generation

## Quick Start

1. Set up your environment variables in a `.env` file at the root of the project:

```
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
SPREADLY_API_KEY=your_spreadly_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

2. Run the application using the provided script:

```bash
./scripts/run-docker.sh
```

This script will:
- Create a `.env` file template if one doesn't exist
- Create a data directory for persistent storage
- Build and start the Docker containers

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Manual Setup

If you prefer to run commands manually:

1. Build and start the services:

```bash
docker compose up --build
```

2. To run in detached mode:

```bash
docker compose up --build -d
```

3. To stop the services:

```bash
docker compose down
```

## Architecture

The application consists of two main services:

1. **showbuddy-python**: Backend API service that handles:
   - Business card processing
   - Audio transcription
   - Report generation

2. **showbuddy-frontend**: React frontend built with Wasp framework that provides:
   - User interface for uploading business cards
   - Audio recording functionality
   - Displaying transcripts and reports

These services communicate over a Docker network, allowing the frontend to make API calls to the backend.

## Volumes

- `./showbuddy-data:/app/showbuddy-data`: Persistent storage for the backend service
- `./showbuddy/app:/app`: Mounts the frontend code for development hot-reloading

## Troubleshooting

- If you encounter permission issues with the Docker volume, try running:
  ```bash
  chmod -R 777 ./showbuddy-data
  ```

- To view logs:
  ```bash
  docker compose logs -f
  ```

- To view logs for a specific service:
  ```bash
  docker compose logs -f showbuddy-python
  ```
  or
  ```bash
  docker compose logs -f showbuddy-frontend
  ```