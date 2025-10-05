#!/bin/bash

# Test script for MCP server debugging
echo "🔍 Testing MCP Server..."

# Check if the script exists
if [ ! -f "scripts/mcp-server.py" ]; then
    echo "❌ MCP server script not found at scripts/mcp-server.py"
    exit 1
fi

echo "✅ MCP server script found"

# Check if Python can run the script
if ! python3 scripts/mcp-server.py --help 2>/dev/null; then
    echo "⚠️  MCP server script doesn't support --help, but that's expected"
fi

# Test the tools/list method
echo "🧪 Testing tools/list method..."
response=$(echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | python3 scripts/mcp-server.py)

if echo "$response" | grep -q "jsonrpc"; then
    echo "✅ MCP server responds correctly to tools/list"
    echo "📋 Available tools:"
    echo "$response" | python3 -m json.tool | grep '"name"' | sed 's/.*"name": "\([^"]*\)".*/- \1/'
else
    echo "❌ MCP server failed to respond to tools/list"
    echo "Response: $response"
    exit 1
fi

# Test environment variables
echo "🔧 Testing environment variables..."
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GITHUB_TOKEN not set"
else
    echo "✅ GITHUB_TOKEN is set"
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
else
    echo "✅ OPENAI_API_KEY is set"
fi

echo "🎉 MCP server test completed successfully!"
