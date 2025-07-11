from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.user import UserResponse, UserCreate, Token
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


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Login attempt for username: {form_data.username}")
    
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    logger.info(f"User authenticated successfully: {form_data.username}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires # type: ignore
    )
    
    logger.debug(f"Access token generated for user: {form_data.username}")
    return Token(
        access_token=access_token,
        token_type="Bearer"
    )