from typing import Optional, Dict, Any, Tuple
import logging

from utils.db import get_clients_pool, get_pool

logger = logging.getLogger(__name__)


async def get_user_role(telegram_id: int) -> Optional[str]:
    # Default lookup from default DB if configured, else try clients
    for pool_name in ("default", "clients"):
        pool = await get_pool(pool_name)
        if not pool:
            continue
        query = """
            SELECT role
            FROM users
            WHERE telegram_id = $1
            LIMIT 1
        """
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(query, telegram_id)
                if row:
                    role = row[0]
                    return str(role) if role is not None else None
        except Exception as e:
            logger.debug(f"Role lookup failed in {pool_name} for {telegram_id}: {e}")
    return None


async def upsert_user_in_clients(user: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Insert or update user into clients database."""
    pool = await get_clients_pool()
    if not pool:
        return False, None

    query = """
        INSERT INTO users (telegram_id, username, first_name, last_name, language, role, is_bot)
        VALUES ($1, $2, $3, $4, $5, COALESCE($6, 'client'), $7)
        ON CONFLICT (telegram_id) DO UPDATE SET
            username = EXCLUDED.username,
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            language = EXCLUDED.language,
            role = EXCLUDED.role,
            is_bot = EXCLUDED.is_bot
        RETURNING telegram_id, username, first_name, last_name, language, role, is_bot
    """
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                user.get("telegram_id"),
                user.get("username"),
                user.get("first_name"),
                user.get("last_name"),
                user.get("language"),
                user.get("role"),
                user.get("is_bot", False),
            )
            saved = dict(row) if row else None
            return True, saved
    except Exception as e:
        logger.warning(f"Failed to upsert user in clients DB: {e}")
        return False, None