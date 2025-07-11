from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.user import UserResponse, UserCreate
from src.models.user import User
from src.utils.auth import create_access_token, get_password_hash, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import get_db

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

import logging
from datetime import timedelta, datetime, timezone

# Configure logging
logger = logging.getLogger("bookmark_short_sql-api")    
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

"""Todo:
1. Check if the user already exists in the database.
2. check if the email is already registered.
3. create a new user in the database.
4. Send the response back to the client.

"""

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Registration attempt for username: {user.username}")

    result = await db.execute(select(User).filter(User.username == user.username))
    db_user_by_username = result.scalars().first()

    if db_user_by_username:
        logger.warning(f"Username already registered: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user_by_email = result.scalars().first()

    if db_user_by_email:
        logger.warning(f"Email already registered: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    logger.info(f"Creating new user: {user.username}")
    # Hash the password before storing it
    hashed_password = get_password_hash(user.password)

    db_user= User(
        email=user.email,
        username=user.username,
        hash_password=hashed_password
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    logger.info(f"User created successfully: {db_user.username}")
    return db_user

"""Todo:
 1. Check if the user exists in the database.
 2. Generate an access token for the user.
 3. Send the access token back.
"""




async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).filter(User.username == token_data.username))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """You can have some custom logic about the User.
    Here I am chcking the User is active or not."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user