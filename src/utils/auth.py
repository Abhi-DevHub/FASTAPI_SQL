from typing import Dict, Optional
from datetime import timedelta, datetime, timezone

from passlib.context import CryptContext

from src.models.user import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # 24 hours = 1440 minutes 


pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(db: AsyncSession,username:str, password: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    if not user:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return to_encode  # In a real application, you would encode this with a secret key