from typing import Optional
import logging

from utils.db import init_db_pool

logger = logging.getLogger(__name__)


async def get_user_role(telegram_id: int) -> Optional[str]:
    pool = await init_db_pool()
    if not pool:
        return None

    query = """
        SELECT role
        FROM users
        WHERE telegram_id = $1
        LIMIT 1
    """
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, telegram_id)
            if not row:
                return None
            role = row[0]
            return str(role) if role is not None else None
    except Exception as e:
        logger.warning(f"Failed to fetch user role for {telegram_id}: {e}")
        return None