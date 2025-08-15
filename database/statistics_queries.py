"""Statistics queries - placeholder.

- generate_daily_statistics
- get_employee_performance
"""
from typing import Any, Dict, List, Optional, Tuple
from datetime import date

from .db_router import DBRouter

router = DBRouter()


async def get_daily_statistics(region_code: str, on_date: date) -> Optional[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT * FROM daily_statistics WHERE date=$1", on_date)
		return dict(row) if row else None


async def upsert_daily_statistics(region_code: str, on_date: date, stats: Dict[str, Any]) -> bool:
	fields = [
		"date","total_requests","completed_requests","cancelled_requests","pending_requests",
		"avg_completion_time_minutes","total_work_hours","total_employees_worked","active_employees",
		"avg_rating","total_feedback","completion_rate",
	]
	values = [
		on_date,
		stats.get("total_requests", 0),
		stats.get("completed_requests", 0),
		stats.get("cancelled_requests", 0),
		stats.get("pending_requests", 0),
		stats.get("avg_completion_time_minutes"),
		stats.get("total_work_hours"),
		stats.get("total_employees_worked", 0),
		stats.get("active_employees", 0),
		stats.get("avg_rating"),
		stats.get("total_feedback", 0),
		stats.get("completion_rate"),
	]
	placeholders = ",".join(f"${i}" for i in range(1, len(values)+1))
	assignments = ",".join(f"{f}=EXCLUDED.{f}" for f in fields if f != "date")
	sql = f"""
		INSERT INTO daily_statistics({','.join(fields)}) VALUES({placeholders})
		ON CONFLICT (date) DO UPDATE SET {assignments}, updated_at = NOW()
	"""
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		res = await conn.execute(sql, *values)
		return res.upper().startswith("INSERT") or res.upper().startswith("UPDATE")


async def get_employee_performance(region_code: str, user_id: int, on_date: date) -> Optional[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT * FROM employee_performance WHERE user_id=$1 AND date=$2", user_id, on_date)
		return dict(row) if row else None


async def upsert_employee_performance(region_code: str, user_id: int, on_date: date, data: Dict[str, Any]) -> bool:
	fields = [
		"user_id","date","role","total_requests","completed_requests","total_time_minutes",
		"avg_time_per_request","efficiency_score","quality_rating","notes",
	]
	values = [
		user_id, on_date,
		data.get("role"),
		data.get("total_requests", 0),
		data.get("completed_requests", 0),
		data.get("total_time_minutes", 0),
		data.get("avg_time_per_request"),
		data.get("efficiency_score"),
		data.get("quality_rating"),
		data.get("notes"),
	]
	placeholders = ",".join(f"${i}" for i in range(1, len(values)+1))
	sql = f"""
		INSERT INTO employee_performance({','.join(fields)}) VALUES({placeholders})
		ON CONFLICT (user_id, date) DO UPDATE SET
			role = COALESCE(EXCLUDED.role, employee_performance.role),
			total_requests = EXCLUDED.total_requests,
			completed_requests = EXCLUDED.completed_requests,
			total_time_minutes = EXCLUDED.total_time_minutes,
			avg_time_per_request = EXCLUDED.avg_time_per_request,
			efficiency_score = EXCLUDED.efficiency_score,
			quality_rating = EXCLUDED.quality_rating,
			notes = COALESCE(EXCLUDED.notes, employee_performance.notes),
			updated_at = NOW()
	"""
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		res = await conn.execute(sql, *values)
		return res.upper().startswith("INSERT") or res.upper().startswith("UPDATE")