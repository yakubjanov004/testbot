"""Core query helpers - placeholder.

- ensure_user_in_region (JIT upsert)
- get_user_by_telegram_id / get_user_role
- promote/demote staff
"""

from typing import Any, Dict, Optional
from datetime import datetime

from .db_router import DBRouter

router = DBRouter()


async def ensure_user_in_region(region_code: str, telegram_id: int,
		full_name: Optional[str] = None,
		username: Optional[str] = None,
		phone: Optional[str] = None,
		language: str = "uz",
		abonent_id: Optional[str] = None,
		address: Optional[str] = None) -> int:
	"""Upsert user by telegram_id in the regional users table and return id.
	- Default role remains unchanged on conflict; new users default to 'client'.
	"""
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO users(telegram_id, full_name, username, phone, role, language, is_active, address, abonent_id, last_activity, created_at, updated_at)
			VALUES ($1, $2, $3, $4, 'client', $5, true, $6, $7, NOW(), NOW(), NOW())
			ON CONFLICT (telegram_id)
			DO UPDATE SET
				full_name = COALESCE(EXCLUDED.full_name, users.full_name),
				username = COALESCE(EXCLUDED.username, users.username),
				phone = COALESCE(EXCLUDED.phone, users.phone),
				language = COALESCE(EXCLUDED.language, users.language),
				address = COALESCE(EXCLUDED.address, users.address),
				abonent_id = COALESCE(EXCLUDED.abonent_id, users.abonent_id),
				last_activity = NOW(),
				updated_at = NOW()
			RETURNING id
			""",
			telegram_id, full_name, username, phone, language, address, abonent_id,
		)
		return int(row["id"]) if row else 0


async def get_user_by_telegram_id(region_code: str, telegram_id: int) -> Optional[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT * FROM users WHERE telegram_id=$1", telegram_id)
		return dict(row) if row else None


async def get_user_role(region_code: str, telegram_id: int) -> Optional[str]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT role FROM users WHERE telegram_id=$1", telegram_id)
		return row["role"] if row else None


async def promote_staff(region_code: str, telegram_id: int, new_role: str) -> bool:
	"""Set user's role to a staff role (e.g., technician, manager)."""
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		res = await conn.execute(
			"UPDATE users SET role=$1, updated_at=NOW() WHERE telegram_id=$2",
			new_role, telegram_id,
		)
		return res.upper().startswith("UPDATE")


async def demote_to_client(region_code: str, telegram_id: int) -> bool:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		res = await conn.execute(
			"UPDATE users SET role='client', updated_at=NOW() WHERE telegram_id=$1",
			telegram_id,
		)
		return res.upper().startswith("UPDATE")


async def set_last_activity(region_code: str, telegram_id: int) -> None:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		await conn.execute(
			"UPDATE users SET last_activity=NOW(), updated_at=NOW() WHERE telegram_id=$1",
			telegram_id,
		)