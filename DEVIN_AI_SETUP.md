# Devin AI Setup Guide for END_CAP Agent Factory

## 🚀 Quick Setup Instructions

### 1. Environment Variables Setup
Devin AI needs the following environment variables to work with the END_CAP Agent Factory. You can either:

**Option A: Use the .envrc file (Recommended)**
- The `.envrc` file is already created with placeholder values
- Replace the placeholder values with your actual API keys

**Option B: Set environment variables manually**
- Use the values below to set up your environment

### 2. Required API Keys

#### OpenAI API Key
```
OPENAI_API_KEY=your-openai-api-key-here
```

#### GitHub Personal Access Token
```
GITHUB_TOKEN=your-github-personal-access-token-here
```

#### Supabase Configuration (Already Set)
```
SUPABASE_URL=https://ssdcbhxctakgysnayzeq.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNzZGNiaHhjdGFrZ3lzbmF5emVxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2MjE0MzksImV4cCI6MjA3NTE5NzQzOX0.vVzLvTyxtdn3NNKUK6Vrx-NQ7njyge_f8wWf9QyyhU4
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNzZGNiaHhjdGFrZ3lzbmF5emVxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImiYXQiOjE3NTk2MjE0MzksImV4cCI6MjA3NTE5NzQzOX0.cVmNis52-9P-EFkEwqqUSojh75B7tpFjuq8bkVG2kAA
```

### 3. MCP Server Configuration

The MCP server is located at: `scripts/mcp-server.py`

**Required Secrets for MCP Server:**
1. `OPENAI_API_KEY` - Your OpenAI API key
2. `ENDCAP_API_URL` - Set to `http://localhost:8000`
3. `GITHUB_TOKEN` - Your GitHub Personal Access Token
4. `SUPABASE_SERVICE_ROLE_KEY` - Already provided above
5. `GCP_SERVICE_ACCOUNT_KEY` - Your Google Cloud service account JSON

### 4. Testing the Setup

Once environment variables are set, you can test:

```bash
# Test the MCP server
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | python3 scripts/mcp-server.py

# Test the FastAPI server
curl http://localhost:8000/api/v1/health
```

### 5. Next Steps

1. **Set up the repository** in Devin AI (click "Set up repo" button)
2. **Configure the MCP server** with the required secrets
3. **Test the MCP server** to ensure all 9 tools are available
4. **Start using the voice-to-agent workflow**

## 🎯 Available MCP Tools

The MCP server provides 9 tools:
- `create_agent` - Create new AI agents
- `deploy_agent` - Deploy to production
- `setup_database` - Set up Supabase database
- `create_repository` - Create GitHub repositories
- `get_repository_info` - Get repo information
- `create_prd_from_conversation` - Extract PRDs from ChatGPT
- `deliver_prd_to_endcap` - Send PRDs to your platform
- `trigger_devin_workflow` - Start Devin AI workflow
- `get_endcap_status` - Check platform health

## 🔧 Troubleshooting

If you encounter issues:
1. Check that all environment variables are set correctly
2. Verify the MCP server can connect to the FastAPI server
3. Ensure all API keys are valid and have proper permissions
4. Check the logs for any error messages

## 📞 Support

For issues or questions, refer to the documentation in the `docs/` folder or check the project README.
