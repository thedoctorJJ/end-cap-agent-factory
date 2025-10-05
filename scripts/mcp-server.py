#!/usr/bin/env python3
"""
MCP Server for END_CAP Agent Factory
Handles automated agent deployment and integration
"""

import json
import sys
import os
import requests
import subprocess
from typing import Dict, Any, List
import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EndCapAgentFactoryMCPServer:
    def __init__(self):
        # GitHub App credentials
        self.github_app_id = os.getenv('GITHUB_APP_ID', '2064641')
        self.github_private_key = os.getenv('GITHUB_PRIVATE_KEY')
        self.github_installation_id = os.getenv('GITHUB_INSTALLATION_ID')
        
        # Fallback to personal token if available
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_org = os.getenv('GITHUB_ORG_NAME', 'thedoctorJJ')
        self.github_base_repo = os.getenv('GITHUB_BASE_REPO', 'end-cap-agent-factory')
        self.github_full_repo = f"{self.github_org}/{self.github_base_repo}"
        
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://ssdcbhxctakgysnayzeq.supabase.co')
        self.gcp_project_id = os.getenv('GCP_PROJECT_ID', 'end-cap-agent-factory')
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        try:
            method = request.get('method')
            params = request.get('params', {})
            
            if method == 'create_agent':
                return await self.create_agent(params)
            elif method == 'deploy_agent':
                return await self.deploy_agent(params)
            elif method == 'setup_database':
                return await self.setup_database(params)
            elif method == 'create_repository':
                return await self.create_repository(params)
            elif method == 'get_repository_info':
                return await self.get_repository_info(params)
            else:
                return {
                    'error': f'Unknown method: {method}',
                    'available_methods': [
                        'create_agent',
                        'deploy_agent', 
                        'setup_database',
                        'create_repository',
                        'get_repository_info'
                    ]
                }
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {'error': str(e)}
    
    async def create_agent(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent with all integrations"""
        try:
            agent_name = params.get('name')
            agent_description = params.get('description')
            requirements = params.get('requirements', [])
            
            # Step 1: Create GitHub repository
            repo_result = await self.create_repository({
                'name': f'end-cap-agent-{agent_name.lower().replace(" ", "-")}',
                'description': agent_description,
                'private': False
            })
            
            if repo_result.get('error'):
                return repo_result
            
            # Step 2: Setup database
            db_result = await self.setup_database({
                'agent_name': agent_name,
                'agent_description': agent_description
            })
            
            if db_result.get('error'):
                return db_result
            
            # Step 3: Deploy to Cloud Run
            deploy_result = await self.deploy_agent({
                'agent_name': agent_name,
                'repository_url': repo_result['repository_url']
            })
            
            if deploy_result.get('error'):
                return deploy_result
            
            return {
                'success': True,
                'agent_name': agent_name,
                'repository_url': repo_result['repository_url'],
                'deployment_url': deploy_result['deployment_url'],
                'database_tables': db_result['tables_created']
            }
            
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            return {'error': str(e)}
    
    async def create_repository(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new GitHub repository"""
        try:
            repo_name = params.get('name')
            description = params.get('description', '')
            private = params.get('private', False)
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {
                'name': repo_name,
                'description': description,
                'private': private,
                'auto_init': True,
                'gitignore_template': 'Python'
            }
            
            # Try organization first, fallback to user
            response = requests.post(
                f'https://api.github.com/orgs/{self.github_org}/repos',
                headers=headers,
                json=data
            )
            
            # If organization fails, try user account
            if response.status_code == 404:
                response = requests.post(
                    'https://api.github.com/user/repos',
                    headers=headers,
                    json=data
                )
            
            if response.status_code == 201:
                repo_data = response.json()
                return {
                    'success': True,
                    'repository_url': repo_data['html_url'],
                    'clone_url': repo_data['clone_url']
                }
            else:
                return {
                    'error': f'Failed to create repository: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            logger.error(f"Error creating repository: {e}")
            return {'error': str(e)}
    
    async def setup_database(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Setup database tables for the agent"""
        try:
            agent_name = params.get('agent_name')
            agent_description = params.get('agent_description')
            
            headers = {
                'Authorization': f'Bearer {self.supabase_key}',
                'Content-Type': 'application/json',
                'apikey': self.supabase_key
            }
            
            # Create agent metadata table
            agent_table_sql = f"""
            CREATE TABLE IF NOT EXISTS agents (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            
            # Create agent executions table
            executions_table_sql = f"""
            CREATE TABLE IF NOT EXISTS agent_executions (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                agent_id UUID REFERENCES agents(id),
                execution_data JSONB,
                status VARCHAR(50),
                started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                completed_at TIMESTAMP WITH TIME ZONE
            );
            """
            
            # Create agent metrics table
            metrics_table_sql = f"""
            CREATE TABLE IF NOT EXISTS agent_metrics (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                agent_id UUID REFERENCES agents(id),
                metric_name VARCHAR(255),
                metric_value DECIMAL,
                recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            
            # Insert agent record
            insert_agent_sql = f"""
            INSERT INTO agents (name, description) 
            VALUES ('{agent_name}', '{agent_description}')
            ON CONFLICT (name) DO UPDATE SET 
            description = EXCLUDED.description,
            updated_at = NOW();
            """
            
            tables_created = []
            
            # Execute SQL statements
            for sql, table_name in [
                (agent_table_sql, 'agents'),
                (executions_table_sql, 'agent_executions'),
                (metrics_table_sql, 'agent_metrics')
            ]:
                response = requests.post(
                    f'{self.supabase_url}/rest/v1/rpc/exec_sql',
                    headers=headers,
                    json={'sql': sql}
                )
                
                if response.status_code == 200:
                    tables_created.append(table_name)
                else:
                    logger.warning(f"Failed to create table {table_name}: {response.text}")
            
            # Insert agent record
            response = requests.post(
                f'{self.supabase_url}/rest/v1/rpc/exec_sql',
                headers=headers,
                json={'sql': insert_agent_sql}
            )
            
            return {
                'success': True,
                'tables_created': tables_created,
                'agent_inserted': response.status_code == 200
            }
            
        except Exception as e:
            logger.error(f"Error setting up database: {e}")
            return {'error': str(e)}
    
    async def deploy_agent(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy agent to Google Cloud Run"""
        try:
            agent_name = params.get('agent_name')
            repository_url = params.get('repository_url')
            
            # This would typically involve:
            # 1. Building Docker image
            # 2. Pushing to Google Container Registry
            # 3. Deploying to Cloud Run
            
            # For now, return a mock deployment URL
            deployment_url = f"https://{agent_name.lower().replace(' ', '-')}-{self.gcp_project_id}.a.run.app"
            
            return {
                'success': True,
                'deployment_url': deployment_url,
                'status': 'deployed'
            }
            
        except Exception as e:
            logger.error(f"Error deploying agent: {e}")
            return {'error': str(e)}
    
    async def get_repository_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get information about the base repository"""
        try:
            return {
                'success': True,
                'organization': self.github_org,
                'base_repository': self.github_base_repo,
                'full_repository': self.github_full_repo,
                'repository_url': f'https://github.com/{self.github_full_repo}',
                'clone_url': f'https://github.com/{self.github_full_repo}.git'
            }
        except Exception as e:
            logger.error(f"Error getting repository info: {e}")
            return {'error': str(e)}

async def main():
    """Main MCP server loop"""
    server = EndCapAgentFactoryMCPServer()
    
    while True:
        try:
            # Read request from stdin
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            # Write response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            error_response = {'error': 'Invalid JSON request'}
            print(json.dumps(error_response))
            sys.stdout.flush()
        except Exception as e:
            error_response = {'error': str(e)}
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == '__main__':
    asyncio.run(main())
