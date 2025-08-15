from typing import Any, Dict, List, Optional

from .db_router import DBRouter

router = DBRouter()


# ===== Materials =====
async def create_material(region_code: str, name: str, category: str = "general",
		quantity: int = 0, unit: str = "pcs", min_quantity: int = 5,
		price: float = 0.0, description: Optional[str] = None, supplier: Optional[str] = None) -> int:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO materials(name, category, quantity, unit, min_quantity, price, description, supplier)
			VALUES($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id
			""",
			name, category, quantity, unit, min_quantity, price, description, supplier,
		)
		return int(row["id"]) if row else 0


async def update_material(region_code: str, material_id: int, updates: Dict[str, Any]) -> bool:
	allowed = {"name","category","quantity","unit","min_quantity","price","description","supplier","is_active"}
	set_parts: List[str] = []
	args: List[Any] = []
	idx = 1
	for k, v in updates.items():
		if k not in allowed:
			continue
		set_parts.append(f"{k} = ${idx}")
		args.append(v)
		idx += 1
	if not set_parts:
		return False
	args.append(material_id)
	sql = f"UPDATE materials SET {', '.join(set_parts)}, updated_at=NOW() WHERE id = ${idx}"
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		res = await conn.execute(sql, *args)
		return res.upper().startswith("UPDATE")


async def get_material(region_code: str, material_id: int) -> Optional[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT * FROM materials WHERE id=$1", material_id)
		return dict(row) if row else None


async def list_materials(region_code: str, category: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
	conditions: List[str] = []
	args: List[Any] = []
	idx = 1
	if category:
		conditions.append(f"category = ${idx}")
		args.append(category)
		idx += 1
	where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
	sql = f"SELECT * FROM materials {where} ORDER BY name ASC LIMIT ${idx} OFFSET ${idx+1}"
	args.extend([limit, offset])
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		rows = await conn.fetch(sql, *args)
		return [dict(r) for r in rows]


# ===== Request Materials =====
async def add_request_material(region_code: str, request_id: str, material_id: int, quantity: int, unit: str = "pcs") -> int:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"INSERT INTO request_materials(request_id, material_id, quantity, unit) VALUES ($1,$2,$3,$4) RETURNING id",
			request_id, material_id, quantity, unit,
		)
		return int(row["id"]) if row else 0


async def list_request_materials(region_code: str, request_id: str) -> List[Dict[str, Any]]:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		rows = await conn.fetch("SELECT * FROM request_materials WHERE request_id=$1", request_id)
		return [dict(r) for r in rows]


# ===== Inventory Transactions / Issued Items =====
async def add_inventory_transaction(region_code: str, request_id: Optional[str], material_id: Optional[int],
		change_type: str, quantity: int, unit_price: Optional[float], total_price: Optional[float],
		performed_by: Optional[int], performed_role: Optional[str]) -> int:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO inventory_transactions(request_id, material_id, change_type, quantity, unit_price, total_price, performed_by, performed_role)
			VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id
			""",
			request_id, material_id, change_type, quantity, unit_price, total_price, performed_by, performed_role,
		)
		return int(row["id"]) if row else 0


async def issue_item(region_code: str, request_id: Optional[str], material_id: int, quantity: int,
		issued_by: int, issued_to: Optional[int]) -> int:
	pool = await router.get_pool(region_code)
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"INSERT INTO issued_items(request_id, material_id, quantity, issued_by, issued_to) VALUES ($1,$2,$3,$4,$5) RETURNING id",
			request_id, material_id, quantity, issued_by, issued_to,
		)
		return int(row["id"]) if row else 0