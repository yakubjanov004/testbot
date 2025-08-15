"""Export log queries - placeholder.

- insert/list excel_exports
"""
from typing import Any, Dict, List, Optional

from .db_router import DBRouter

router = DBRouter()


async def insert_export(region_code: str, user_id: int, export_type: str,
		date_range_start: Optional[str] = None, date_range_end: Optional[str] = None,
		file_name: Optional[str] = None, file_size_bytes: Optional[int] = None,
		file_hash: Optional[str] = None, filters_applied: Optional[Dict[str, Any]] = None,
		record_count: Optional[int] = None) -> int:
	pool = await router.get_pool(region_code)
	filters_applied = filters_applied or {}
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO excel_exports(user_id, export_type, date_range_start, date_range_end, file_name,
				file_size_bytes, file_hash, filters_applied, record_count)
			VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING id
			""",
			user_id, export_type, date_range_start, date_range_end, file_name,
			file_size_bytes, file_hash, filters_applied, record_count,
		)
		return int(row["id"]) if row else 0


async def list_exports(region_code: str, user_id: Optional[int] = None, export_type: Optional[str] = None,
		limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
	conditions: List[str] = []
	args: List[Any] = []
	idx = 1
	if user_id is not None:
		conditions.append(f"user_id = ${idx}")
		args.append(user_id)
		idx += 1
	if export_type is not None:
		conditions.append(f"export_type = ${idx}")
		args.append(export_type)
		idx += 1
	where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
	sql = f"SELECT * FROM excel_exports {where} ORDER BY created_at DESC LIMIT ${idx} OFFSET ${idx+1}"
	args.extend([limit, offset])
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		rows = await conn.fetch(sql, *args)
		return [dict(r) for r in rows]