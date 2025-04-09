# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Backend (Python):
  - Build Docker: `make build-docker`
  - Run Docker: `make run-docker`
  - Run Locally: `make run-local`

- Frontend (React/Wasp):
  - Start app: `wasp start`
  - Migrations: `wasp db migrate-dev`

- E2E Tests:
  - Run tests: `npm run e2e:playwright`
  - Run with UI: `npm run local:e2e:playwright:ui`

## Code Style Guidelines
- TypeScript/React:
  - Use TypeScript types for all components/functions
  - Components organized by feature
  - Use tailwind-merge for class composition
  - Follow existing import order pattern

- Python:
  - Use type hints (Dict, List, Optional)
  - Organize imports: built-in, third-party, local
  - Use descriptive exception handling
  - Follow Google-style docstrings

- Common:
  - Prefer clear, descriptive variable names
  - Keep functions focused on single responsibility
  - Maintain consistent indentation and formatting