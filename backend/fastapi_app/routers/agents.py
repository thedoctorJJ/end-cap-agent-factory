from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Pydantic models
class AgentCreate(BaseModel):
    name: str
    description: str
    purpose: str
    tools: List[str] = []
    prompts: List[str] = []

class AgentResponse(BaseModel):
    id: str
    name: str
    description: str
    purpose: str
    tools: List[str]
    prompts: List[str]
    status: str
    created_at: datetime
    updated_at: datetime

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    purpose: Optional[str] = None
    tools: Optional[List[str]] = None
    prompts: Optional[List[str]] = None
    status: Optional[str] = None

# In-memory storage for demo (replace with Supabase in production)
agents_db = {}

@router.get("/agents", response_model=List[AgentResponse])
async def get_agents():
    """Get all agents"""
    return list(agents_db.values())

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get a specific agent by ID"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents_db[agent_id]

@router.post("/agents", response_model=AgentResponse)
async def create_agent(agent: AgentCreate):
    """Create a new agent"""
    agent_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    new_agent = AgentResponse(
        id=agent_id,
        name=agent.name,
        description=agent.description,
        purpose=agent.purpose,
        tools=agent.tools,
        prompts=agent.prompts,
        status="created",
        created_at=now,
        updated_at=now
    )
    
    agents_db[agent_id] = new_agent
    return new_agent

@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent_update: AgentUpdate):
    """Update an existing agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    existing_agent = agents_db[agent_id]
    update_data = agent_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing_agent, field, value)
    
    existing_agent.updated_at = datetime.utcnow()
    agents_db[agent_id] = existing_agent
    
    return existing_agent

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    del agents_db[agent_id]
    return {"message": "Agent deleted successfully"}
