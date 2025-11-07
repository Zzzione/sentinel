from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class RoleOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

class UserOut(UserBase):
    id: int
    is_active: bool
    roles: List[RoleOut] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str
