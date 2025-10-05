from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Pydantic models
class PRDCreate(BaseModel):
    title: str
    description: str
    requirements: List[str]
    voice_input: Optional[str] = None
    text_input: Optional[str] = None

class PRDResponse(BaseModel):
    id: str
    title: str
    description: str
    requirements: List[str]
    voice_input: Optional[str]
    text_input: Optional[str]
    status: str
    github_repo_url: Optional[str]
    created_at: datetime
    updated_at: datetime

class PRDUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    status: Optional[str] = None
    github_repo_url: Optional[str] = None

# In-memory storage for demo (replace with Supabase in production)
prds_db = {}

@router.get("/prds", response_model=List[PRDResponse])
async def get_prds():
    """Get all PRDs"""
    return list(prds_db.values())

@router.get("/prds/{prd_id}", response_model=PRDResponse)
async def get_prd(prd_id: str):
    """Get a specific PRD by ID"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    return prds_db[prd_id]

@router.post("/prds", response_model=PRDResponse)
async def create_prd(prd: PRDCreate):
    """Create a new PRD"""
    prd_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    new_prd = PRDResponse(
        id=prd_id,
        title=prd.title,
        description=prd.description,
        requirements=prd.requirements,
        voice_input=prd.voice_input,
        text_input=prd.text_input,
        status="submitted",
        github_repo_url=None,
        created_at=now,
        updated_at=now
    )
    
    prds_db[prd_id] = new_prd
    
    # TODO: Trigger MCP service to create GitHub repo
    # TODO: Trigger Devin AI orchestration
    
    return new_prd

@router.put("/prds/{prd_id}", response_model=PRDResponse)
async def update_prd(prd_id: str, prd_update: PRDUpdate):
    """Update an existing PRD"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    
    existing_prd = prds_db[prd_id]
    update_data = prd_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing_prd, field, value)
    
    existing_prd.updated_at = datetime.utcnow()
    prds_db[prd_id] = existing_prd
    
    return existing_prd

@router.delete("/prds/{prd_id}")
async def delete_prd(prd_id: str):
    """Delete a PRD"""
    if prd_id not in prds_db:
        raise HTTPException(status_code=404, detail="PRD not found")
    
    del prds_db[prd_id]
    return {"message": "PRD deleted successfully"}
