from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    is_active: bool

    # This replaces `Config.orm_mode = True` in Pydantic v1
    model_config = ConfigDict(from_attributes=True)
