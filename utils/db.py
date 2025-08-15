import logging
from typing import Optional

import asyncpg

from utils.db_config import get_database_url

logger = logging.getLogger(__name__)

_pool: Optional[asyncpg.pool.Pool] = None


async def init_db_pool() -> Optional[asyncpg.pool.Pool]:
    global _pool
    if _pool is not None:
        return _pool

    dsn = get_database_url()
    if not dsn:
        logger.info("DATABASE_URL not set; DB pool not initialized")
        return None

    _pool = await asyncpg.create_pool(dsn, min_size=1, max_size=5)
    logger.info("Database pool initialized")
    return _pool


async def get_pool() -> Optional[asyncpg.pool.Pool]:
    return _pool


async def close_db_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
        logger.info("Database pool closed")