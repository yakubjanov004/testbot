"""State Transitions queries - placeholder.

- insert_transition
- get history / latest transition
"""

from typing import Any, Dict, List, Optional

from .db_router import DBRouter

router = DBRouter()


async def insert_transition(region_code: str, request_id: str, to_role: str, action: str,
		actor_id: Optional[int] = None,
		from_role: Optional[str] = None,
		transition_data: Optional[Dict[str, Any]] = None,
		comments: Optional[str] = None) -> int:
	"""Insert new state transition and return its id."""
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO state_transitions(request_id, from_role, to_role, action, actor_id, transition_data, comments)
			VALUES ($1,$2,$3,$4,$5, COALESCE($6,'{}'::jsonb), $7)
			RETURNING id
			""",
			request_id, from_role, to_role, action, actor_id, transition_data, comments,
		)
		return int(row["id"]) if row else 0


async def get_transitions_by_request(region_code: str, request_id: str, limit: int = 100,
		offset: int = 0) -> List[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		rows = await conn.fetch(
			"SELECT * FROM state_transitions WHERE request_id=$1 ORDER BY created_at ASC LIMIT $2 OFFSET $3",
			request_id, limit, offset,
		)
		return [dict(r) for r in rows]


async def get_latest_transition(region_code: str, request_id: str) -> Optional[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"SELECT * FROM state_transitions WHERE request_id=$1 ORDER BY created_at DESC LIMIT 1",
			request_id,
		)
		return dict(row) if row else None