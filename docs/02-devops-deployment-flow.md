# DevOps & Deployment Flow

## Overview
This document describes the deployment pipeline and CI/CD workflow for the Modular AI Agent Platform.

## Local Development
- Backend: `uvicorn main:app --reload`
- Frontend: `npm run dev` inside `next-app`

## CI/CD
- Use GitHub Actions to automate:
  - Running tests on backend and frontend
  - Linting and formatting
  - Deploying to Google Cloud Run for both backend and frontend
  - Supabase migrations
- Automatic rollback if deployment fails

## Monitoring & Logging
- Use Google Cloud Logging for backend + MCP service
- Supabase Edge Functions logs for PRD triggers
- Alerts via Slack/email
