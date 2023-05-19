from typing import Optional

from content.db.interfaces import AsyncDB

db: Optional[AsyncDB] = None


async def get_db() -> AsyncDB:
    return db
