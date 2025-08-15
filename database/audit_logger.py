"""Audit logger helper.

Use to write actions into audit_log.
"""

from typing import Any, Dict, Optional

from .db_router import DBRouter

router = DBRouter()


async def log_action(
	region_code: str,
	actor_user_id: int,
	actor_role: str,
	action: str,
	*,
	entity_type: Optional[str] = None,
	entity_id: Optional[str] = None,
	request_id: Optional[str] = None,
	target_user_id: Optional[int] = None,
	channel: Optional[str] = None,
	params: Optional[Dict[str, Any]] = None,
	before_data: Optional[Dict[str, Any]] = None,
	after_data: Optional[Dict[str, Any]] = None,
	status: Optional[str] = None,
	error_message: Optional[str] = None,
	source_ip: Optional[str] = None,
	user_agent: Optional[str] = None,
	message_id: Optional[int] = None,
	correlation_id: Optional[str] = None,
	session_id: Optional[str] = None,
) -> int:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO audit_log(
				actor_user_id, actor_role, action, entity_type, entity_id, request_id, target_user_id,
				channel, params, before_data, after_data, status, error_message, source_ip, user_agent,
				message_id, correlation_id, session_id
			) VALUES (
				$1,$2,$3,$4,$5,$6,$7,$8, COALESCE($9,'{}'::jsonb), $10,$11,$12,$13,$14,$15,$16,$17,$18
			) RETURNING id
			""",
			actor_user_id, actor_role, action, entity_type, entity_id, request_id, target_user_id,
			channel, params, before_data, after_data, status, error_message, source_ip, user_agent,
			message_id, correlation_id, session_id,
		)
		return int(row["id"]) if row else 0