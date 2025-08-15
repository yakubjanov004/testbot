"""Clients DB queries.

Minimal helpers for /start and global search.
"""

from typing import Optional, Dict, Any
from datetime import datetime

from .db import get_pool


async def ensure_global_user(telegram_id: int, full_name: str = None, username: str = None,
                             phone: str = None, language: str = "uz", address: str = None,
                             abonent_id: str = None) -> int:
	"""Upsert client by telegram_id and return id.
	
	This implementation performs a manual SELECT-then-UPDATE/INSERT sequence
	to avoid requiring a unique constraint on telegram_id.
	"""
	pool = await get_pool()
	async with pool.acquire() as conn:
		# Check if user exists
		row = await conn.fetchrow("SELECT id FROM users WHERE telegram_id = $1 LIMIT 1", telegram_id)
		if row:
			# Update existing
			row = await conn.fetchrow(
				"""
				UPDATE users
				SET full_name = $2,
					username = $3,
					phone    = $4,
					language = $5,
					address  = $6,
					abonent_id = $7,
					updated_at = NOW()
				WHERE telegram_id = $1
				RETURNING id
				""",
				telegram_id, full_name, username, phone, language, address, abonent_id,
			)
			return int(row["id"]) if row else -1
		else:
			# Insert new
			row = await conn.fetchrow(
				"""
				INSERT INTO users(telegram_id, full_name, username, phone, language, is_active, address, abonent_id, created_at, updated_at)
				VALUES ($1, $2, $3, $4, $5, true, $6, $7, NOW(), NOW())
				RETURNING id
				""",
				telegram_id, full_name, username, phone, language, address, abonent_id,
			)
			return int(row["id"]) if row else -1


async def get_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
	pool = await get_pool()
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
		return dict(row) if row else None


async def get_by_phone(phone: str) -> Optional[Dict[str, Any]]:
	pool = await get_pool()
	# Simple normalize example (strip spaces). You can enhance it.
	norm = (phone or "").replace(" ", "").replace("-", "")
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT * FROM users WHERE phone = $1", norm)
		return dict(row) if row else None


async def delete_by_telegram_id(telegram_id: int) -> bool:
	pool = await get_pool()
	async with pool.acquire() as conn:
		res = await conn.execute("DELETE FROM users WHERE telegram_id = $1", telegram_id)
		return res.startswith("DELETE")