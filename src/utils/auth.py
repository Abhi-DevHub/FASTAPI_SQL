from typing import Dict, Optional
from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from passlib.context import CryptContext

from jose import JWTError, jwt

from src.models.user import User
from src import config
from src.database import get_db
from src.schemas.user import TokenData

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # 24 hours = 1440 minutes 


pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(db: AsyncSession,username:str, password: str) -> bool | User:
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    if not user:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentail_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )


    try:
        payload = jwt.decode(token,config.SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        username: str = payload.get("sub") # type: ignore
        if username is None:
            raise credentail_exceptions
        token_data = TokenData(username=username)       
    except JWTError:
        raise credentail_exceptions
    result = await db.execute(select(User).filter(User.username == token_data.username))