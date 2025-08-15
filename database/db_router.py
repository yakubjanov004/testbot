"""DB router (region -> async DB pool).

Minimal implementation using asyncpg with lazy-initialized pools.
"""

import asyncio
from typing import Dict, Optional

import asyncpg  # type: ignore

from .region_config import get_dsn_for_region


class DBRouter:
	def __init__(self) -> None:
		self._pools: Dict[str, asyncpg.Pool] = {}
		self._lock = asyncio.Lock()

	async def get_pool(self, region_code: str) -> asyncpg.Pool:
		code = (region_code or "").lower()
		if code in self._pools:
			return self._pools[code]
		async with self._lock:
			if code in self._pools:
				return self._pools[code]
			dsn = get_dsn_for_region(code)
			pool = await asyncpg.create_pool(dsn)  # relies on DSN string
			self._pools[code] = pool
			return pool

	async def close_all(self) -> None:
		async with self._lock:
			for pool in self._pools.values():
				await pool.close()
			self._pools.clear()


# global router instance (optional usage)
router: Optional[DBRouter] = None


async def get_router() -> DBRouter:
	global router
	if router is None:
		router = DBRouter()
	return router