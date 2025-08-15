"""Clients DB connection (pool).

Uses env var CLIENTS_DB_URL for DSN.
"""

import os
import asyncio
from typing import Optional

import asyncpg  # type: ignore

_pool: Optional[asyncpg.Pool] = None
_lock = asyncio.Lock()


async def get_pool() -> asyncpg.Pool:
	"""Get (or create) global asyncpg pool for Clients DB."""
	global _pool
	if _pool is not None:
		return _pool
	async with _lock:
		if _pool is not None:
			return _pool
		dsn = os.environ.get("CLIENTS_DB_URL")
		if not dsn:
			raise RuntimeError("CLIENTS_DB_URL is not set")
		_pool = await asyncpg.create_pool(dsn)
		return _pool


async def close_pool() -> None:
	"""Close the global pool if opened."""
	global _pool
	async with _lock:
		if _pool is not None:
			await _pool.close()
			_pool = None