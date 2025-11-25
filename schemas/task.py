from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to_id: int


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    assigned_to_id: int
    created_by_id: int

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    assigned_to_id: Optional[int]
