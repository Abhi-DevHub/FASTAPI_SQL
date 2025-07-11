import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.bookmark import Bookmark

def genreate_short_code(length: int = 10) -> str:
    """Generate a random short code of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

async def create_unique_short_code(db: AsyncSession, length: int = 10) ->  str:
    """Create a unique short code for a bookmark."""
    while True:
        short_code = genreate_short_code(length)
        result = await db.execute(select(Bookmark).filter(Bookmark.short_code == short_code))
        if not result.scalars().first():
            return short_code
        # If the short code already exists, generate a new one
        continue
# Note: This function assumes that the Bookmark model has a 'short_code' field.
# If the field name is different, adjust the filter accordingly.
# This function will keep generating a new short code until it finds one that is not already in use.
