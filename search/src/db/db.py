from typing import Optional

from db.interface import IAsyncDB

db: Optional[IAsyncDB] = None


async def get_db() -> IAsyncDB:
    return db
