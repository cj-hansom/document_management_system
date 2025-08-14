from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from app.database import database
from app.models.users_model import users
from app.schemas.users_schema import User, UserCreate
from app.core.security import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from datetime import timedelta
from app.schemas.tokens_schema import Token
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_user(username: str):
    try:
        query = users.select().where(users.c.username == username)
        return await database.fetch_one(query)
    except Exception as e:
        logger.exception(f"Database error while fetching user '{username}': {e}")
        return None


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return None
    try:
        if not verify_password(password, user["hashed_password"]):
            return None
        return user
    except Exception as e:
        logger.exception(f"Password verification error for '{username}': {e}")
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    except JWTError as e:
        logger.warning(f"JWT decode failed: {e}")
        raise credentials_exception
    except Exception as e:
        logger.exception(f"Unexpected error decoding JWT: {e}")
        raise credentials_exception

    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        access_token = create_access_token(data={"sub": user["username"]})
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during login for '{form_data.username}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.post("/register", response_model=User)
async def register(user: UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        query = users.insert().values(
            id=str(uuid.uuid4()),
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            is_active=True,
        ).returning(*users.c)

        created_user = await database.fetch_one(query)
        if not created_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        return created_user

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during registration for '{user.username}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while registering. Please try again later."
        )
