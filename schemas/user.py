from pydantic import BaseModel
from models.user import RoleEnum


class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum


class UserRead(BaseModel):
    id: int
    username: str
    role: RoleEnum

    class Config:
        from_attributes = True
