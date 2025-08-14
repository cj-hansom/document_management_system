from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from ..schemas.users_schema import UserCreate, User
from ..schemas.tokens_schema import Token, TokenData
from ..database import database
from app.models.users_model import users 
from .auth import (
    get_current_user,
)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["users"])


# Get current user
@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


