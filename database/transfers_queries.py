"""Application Transfers queries - placeholder.

- create/list transfers
- filter by from_role/to_role/date
"""
from typing import Any, Dict, List, Optional

from .db_router import DBRouter

router = DBRouter()


async def create_transfer(region_code: str, application_id: str, from_role: Optional[str], to_role: str,
		transferred_by: int, transfer_reason: Optional[str] = None, transfer_notes: Optional[str] = None,
		application_type: str = "service_request") -> int:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO application_transfers(application_id, application_type, from_role, to_role, transferred_by, transfer_reason, transfer_notes)
			VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id
			""",
			application_id, application_type, from_role, to_role, transferred_by, transfer_reason, transfer_notes,
		)
		return int(row["id"]) if row else 0


async def list_transfers(region_code: str, application_id: Optional[str] = None,
		from_role: Optional[str] = None, to_role: Optional[str] = None, user_id: Optional[int] = None,
		limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
	conditions: List[str] = []
	args: List[Any] = []
	idx = 1
	if application_id:
		conditions.append(f"application_id = ${idx}")
		args.append(application_id)
		idx += 1
	if from_role:
		conditions.append(f"from_role = ${idx}")
		args.append(from_role)
		idx += 1
	if to_role:
		conditions.append(f"to_role = ${idx}")
		args.append(to_role)
		idx += 1
	if user_id:
		conditions.append(f"transferred_by = ${idx}")
		args.append(user_id)
		idx += 1
	where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
	sql = f"SELECT * FROM application_transfers {where} ORDER BY created_at DESC LIMIT ${idx} OFFSET ${idx+1}"
	args.extend([limit, offset])
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		rows = await conn.fetch(sql, *args)
		return [dict(r) for r in rows]