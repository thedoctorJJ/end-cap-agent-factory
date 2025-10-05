# GitHub MCP Service Template

This is a template for the GitHub MCP (Model Context Protocol) service that will handle automated repository creation for PRDs.

## Overview

The MCP service acts as a bridge between your platform and GitHub, automatically creating repositories when PRDs are submitted.

## Features

- **Webhook handling** for PRD triggers
- **GitHub repository creation** from templates
- **PRD.md file generation** and commit
- **Integration with Supabase** for status updates
- **Error handling and logging**

## Setup

1. **Deploy to Google Cloud Run** or similar service
2. **Configure webhook URL** in your GitHub App
3. **Set environment variables** for GitHub App credentials
4. **Test webhook integration**

## Environment Variables

```env
GITHUB_APP_ID=your-github-app-id
GITHUB_PRIVATE_KEY=your-github-private-key
GITHUB_WEBHOOK_SECRET=your-webhook-secret
GITHUB_ORG_NAME=your-org-name
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-service-key
```

## API Endpoints

- `POST /webhook` - GitHub webhook handler
- `POST /create-repo` - Manual repository creation
- `GET /health` - Health check endpoint

## Next Steps

1. Create a new repository for the MCP service
2. Copy this template and customize for your needs
3. Deploy to your hosting platform
4. Configure webhook URL in GitHub App settings
5. Test the integration with your platform
