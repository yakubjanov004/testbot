"""Service Requests queries - placeholder.

- create/update/get service_requests
- search/filter by role/status/priority
"""
from typing import Any, Dict, List, Optional, Tuple
import uuid

from .db_router import DBRouter

router = DBRouter()


_ALLOWED_UPDATE_FIELDS = {
	"workflow_type", "client_id", "role_current", "current_status", "priority",
	"description", "location", "contact_info", "state_data", "equipment_used",
	"inventory_updated", "completion_rating", "feedback_comments",
	"current_assignee_id", "current_assignee_role", "created_by_staff",
	"staff_creator_id", "staff_creator_role", "creation_source",
	"client_notified_at", "diagnosis", "service_order_number", "accepted_by_fio",
	"approvers", "installation_date", "installed_by", "diagnosis_date",
	"diagnosed_by", "rated_at", "assigned_technician_id", "ready_to_install",
}


async def create_service_request(region_code: str, data: Dict[str, Any]) -> str:
	"""Create a service_request; returns request id."""
	req_id = data.get("id") or str(uuid.uuid4())
	fields = [
		"id","workflow_type","client_id","role_current","current_status","priority",
		"description","location","contact_info","state_data","equipment_used",
		"inventory_updated","completion_rating","feedback_comments",
		"current_assignee_id","current_assignee_role","created_by_staff",
		"staff_creator_id","staff_creator_role","creation_source","client_notified_at",
		"diagnosis","service_order_number","accepted_by_fio","approvers",
		"installation_date","installed_by","diagnosis_date","diagnosed_by",
		"rated_at","assigned_technician_id","ready_to_install",
	]
	values = [
		req_id,
		data.get("workflow_type","connection_request"),
		data.get("client_id"),
		data.get("role_current","manager"),
		data.get("current_status","created"),
		data.get("priority","medium"),
		data.get("description"),
		data.get("location"),
		data.get("contact_info",{}),
		data.get("state_data",{}),
		data.get("equipment_used",[]),
		bool(data.get("inventory_updated", False)),
		data.get("completion_rating"),
		data.get("feedback_comments"),
		data.get("current_assignee_id"),
		data.get("current_assignee_role"),
		bool(data.get("created_by_staff", False)),
		data.get("staff_creator_id"),
		data.get("staff_creator_role"),
		data.get("creation_source","client"),
		data.get("client_notified_at"),
		data.get("diagnosis"),
		data.get("service_order_number"),
		data.get("accepted_by_fio"),
		data.get("approvers",[]),
		data.get("installation_date"),
		data.get("installed_by"),
		data.get("diagnosis_date"),
		data.get("diagnosed_by"),
		data.get("rated_at"),
		data.get("assigned_technician_id"),
		bool(data.get("ready_to_install", False)),
	]
	placeholders = ",".join(f"${i}" for i in range(1, len(values)+1))
	columns = ",".join(fields)
	sql = f"INSERT INTO service_requests ({columns}) VALUES ({placeholders}) RETURNING id"
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(sql, *values)
		return row["id"]


async def update_service_request(region_code: str, request_id: str, updates: Dict[str, Any]) -> bool:
	"""Partial update. Only allows whitelisted fields."""
	allowed = {k: v for k, v in updates.items() if k in _ALLOWED_UPDATE_FIELDS}
	if not allowed:
		return False
	set_parts: List[str] = []
	args: List[Any] = []
	idx = 1
	for k, v in allowed.items():
		set_parts.append(f"{k} = ${idx}")
		args.append(v)
		idx += 1
	set_parts.append(f"updated_at = NOW()")
	args.append(request_id)
	sql = f"UPDATE service_requests SET {', '.join(set_parts)} WHERE id = ${idx}"
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		res = await conn.execute(sql, *args)
		return res.upper().startswith("UPDATE")


async def get_service_request(region_code: str, request_id: str) -> Optional[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT * FROM service_requests WHERE id=$1", request_id)
		return dict(row) if row else None


async def search_service_requests(
	region_code: str,
	role_current: Optional[str] = None,
	status: Optional[str] = None,
	priority: Optional[str] = None,
	assignee_id: Optional[int] = None,
	client_id: Optional[int] = None,
	limit: int = 50,
	offset: int = 0,
) -> List[Dict[str, Any]]:
	conditions: List[str] = []
	args: List[Any] = []
	idx = 1
	if role_current:
		conditions.append(f"role_current = ${idx}")
		args.append(role_current)
		idx += 1
	if status:
		conditions.append(f"current_status = ${idx}")
		args.append(status)
		idx += 1
	if priority:
		conditions.append(f"priority = ${idx}")
		args.append(priority)
		idx += 1
	if assignee_id:
		conditions.append(f"current_assignee_id = ${idx}")
		args.append(assignee_id)
		idx += 1
	if client_id:
		conditions.append(f"client_id = ${idx}")
		args.append(client_id)
		idx += 1
	where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
	sql = f"SELECT * FROM service_requests {where} ORDER BY created_at DESC LIMIT ${idx} OFFSET ${idx+1}"
	args.extend([limit, offset])
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		rows = await conn.fetch(sql, *args)
		return [dict(r) for r in rows]