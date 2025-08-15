from typing import Any, Dict, List, Optional

from .db_router import DBRouter

router = DBRouter()


async def get_role_inbox(region_code: str, role: str, recipient_id: Optional[int] = None,
		limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		if recipient_id:
			rows = await conn.fetch(
				"""
				SELECT * FROM inbox_messages
				WHERE assigned_role=$1 AND (recipient_id=$2 OR recipient_id IS NULL)
				ORDER BY created_at DESC LIMIT $3 OFFSET $4
				""",
				role, recipient_id, limit, offset,
			)
		else:
			rows = await conn.fetch(
				"SELECT * FROM inbox_messages WHERE assigned_role=$1 ORDER BY created_at DESC LIMIT $2 OFFSET $3",
				role, limit, offset,
			)
		return [dict(r) for r in rows]


async def mark_read(region_code: str, inbox_id: int, recipient_id: Optional[int] = None) -> bool:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		if recipient_id:
			res = await conn.execute(
				"UPDATE inbox_messages SET is_read=true, inbox_viewed=true, seen_by_users = (seen_by_users || to_jsonb($2::int))::jsonb, updated_at=NOW() WHERE id=$1",
				inbox_id, recipient_id,
			)
		else:
			res = await conn.execute(
				"UPDATE inbox_messages SET is_read=true, inbox_viewed=true, updated_at=NOW() WHERE id=$1",
				inbox_id,
			)
		return res.upper().startswith("UPDATE")


async def mark_completed(region_code: str, inbox_id: int) -> bool:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		res = await conn.execute(
			"UPDATE inbox_messages SET completed=true, updated_at=NOW() WHERE id=$1",
			inbox_id,
		)
		return res.upper().startswith("UPDATE")


async def create_on_assignment(
	region_code: str,
	application_id: str,
	assigned_role: str,
	title: str,
	description: Optional[str] = None,
	priority: str = "medium",
	recipient_id: Optional[int] = None,
	reply_markup_data: Optional[Dict[str, Any]] = None,
	application_type: str = "service_request",
	message_type: str = "application",
	metadata: Optional[Dict[str, Any]] = None,
) -> int:
	pool = await router.get_pool(region_code)
	reply_markup_data = reply_markup_data or {}
	metadata = metadata or {}
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO inbox_messages(
				application_id, application_type, assigned_role, message_type,
				title, description, priority, is_read, recipient_id,
				reply_markup_data, telegram_message_id, reply_button_clicked, inbox_viewed,
				completed, seen_by_users, metadata
			) VALUES (
				$1,$2,$3,$4,$5,$6,$7,false,$8,$9,NULL,false,false,false,'[]'::jsonb,$10
			) RETURNING id
			""",
			application_id, application_type, assigned_role, message_type,
			title, description, priority, recipient_id, reply_markup_data, metadata,
		)
		return int(row["id"]) if row else 0