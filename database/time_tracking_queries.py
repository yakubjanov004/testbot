"""Time Tracking queries - placeholder.

- start/end tracking
- list by request/user
"""
from typing import Any, Dict, List, Optional

from .db_router import DBRouter

router = DBRouter()


async def start_tracking(region_code: str, request_id: str, user_id: int, role: str,
		action_type: str = "started", workflow_stage: Optional[str] = None,
		notes: Optional[str] = None) -> int:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO time_tracking(request_id, user_id, role, action_type, workflow_stage, notes)
			VALUES ($1,$2,$3,$4,$5,$6)
			ON CONFLICT (request_id, user_id, action_type)
			DO UPDATE SET started_at = COALESCE(time_tracking.started_at, NOW()),
				workflow_stage = COALESCE(EXCLUDED.workflow_stage, time_tracking.workflow_stage),
				notes = COALESCE(EXCLUDED.notes, time_tracking.notes),
				updated_at = NOW()
			RETURNING id
			""",
			request_id, user_id, role, action_type, workflow_stage, notes,
		)
		return int(row["id"]) if row else 0


async def end_tracking(region_code: str, request_id: str, user_id: int, action_type: str = "started",
		efficiency_score: Optional[float] = None, quality_rating: Optional[float] = None) -> bool:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		res = await conn.execute(
			"""
			UPDATE time_tracking
			SET ended_at = COALESCE(ended_at, NOW()),
				duration_minutes = COALESCE(duration_minutes, CAST(EXTRACT(EPOCH FROM (COALESCE(ended_at, NOW()) - started_at))/60 AS INT)),
				efficiency_score = COALESCE($4, efficiency_score),
				quality_rating = COALESCE($5, quality_rating),
				updated_at = NOW()
			WHERE request_id=$1 AND user_id=$2 AND action_type=$3
			""",
			request_id, user_id, action_type, efficiency_score, quality_rating,
		)
		return res.upper().startswith("UPDATE")


async def list_tracking_by_request(region_code: str, request_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		rows = await conn.fetch(
			"SELECT * FROM time_tracking WHERE request_id=$1 ORDER BY started_at ASC LIMIT $2 OFFSET $3",
			request_id, limit, offset,
		)
		return [dict(r) for r in rows]


async def list_tracking_by_user(region_code: str, user_id: int, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		rows = await conn.fetch(
			"SELECT * FROM time_tracking WHERE user_id=$1 ORDER BY started_at DESC LIMIT $2 OFFSET $3",
			user_id, limit, offset,
		)
		return [dict(r) for r in rows]