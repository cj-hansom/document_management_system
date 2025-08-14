from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from .database import database
from .models.users_model import users  # Your users table
from .schemas.users_schema import User  # Pydantic User schema for response/validation
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class TokenData(BaseModel):
    username: Optional[str] = None

async def get_user_by_username(username: str) -> Optional[User]:
    query = users.select().where(users.c.username == username)
    user_record = await database.fetch_one(query)
    if user_record:
        return User(**user_record)
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user
