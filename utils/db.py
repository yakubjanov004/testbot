import logging
from typing import Optional, Dict

import asyncpg

from utils.db_config import DATABASES

logger = logging.getLogger(__name__)

_pools: Dict[str, asyncpg.pool.Pool] = {}


async def init_db_pools() -> Dict[str, asyncpg.pool.Pool]:
    """Initialize asyncpg pools for configured databases.

    Only initialize pools for known keys: 'clients' and region codes
    present in DATABASES (e.g., 'toshkent', 'samarqand'). If a generic
    'default' is provided, it will also be initialized.
    """
    global _pools
    if _pools:
        return _pools

    for name, dsn in DATABASES.items():
        try:
            pool = await asyncpg.create_pool(dsn, min_size=1, max_size=5)
            _pools[name] = pool
            logger.info(f"Database pool initialized: {name}")
        except Exception as e:
            logger.warning(f"Failed to init pool '{name}': {e}")
    if not _pools:
        logger.info("No database URLs configured; no pools initialized")
    return _pools


async def get_pool(name: str = "default") -> Optional[asyncpg.pool.Pool]:
    return _pools.get(name)


async def get_clients_pool() -> Optional[asyncpg.pool.Pool]:
    return _pools.get("clients")


async def get_region_pool(region: str) -> Optional[asyncpg.pool.Pool]:
    return _pools.get(region)


async def close_all_pools() -> None:
    global _pools
    for name, pool in list(_pools.items()):
        try:
            await pool.close()
            logger.info(f"Database pool closed: {name}")
        except Exception:
            pass
    _pools.clear()