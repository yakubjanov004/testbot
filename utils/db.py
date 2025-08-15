import os
import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

try:
	import asyncpg  # type: ignore
except Exception as e:
	# Defer import error until runtime if package is missing
	asyncpg = None  # type: ignore


logger = logging.getLogger(__name__)

# Load environment (safe to call multiple times)
load_dotenv()

DB_ENABLED = os.getenv('DB_ENABLED', '0').lower() in {'1', 'true', 'yes', 'on'}
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'alfaconnect_db')

_pool: Optional["asyncpg.Pool"] = None


async def init_db_pool() -> "asyncpg.Pool":
	"""Initialize the global database connection pool and ensure schema."""
	if not DB_ENABLED:
		raise RuntimeError("Database is disabled. Set DB_ENABLED=1 to enable.")
	global _pool
	if asyncpg is None:
		raise RuntimeError("asyncpg is not installed. Please add it to requirements and install dependencies.")
	if _pool is None:
		logger.info("Initializing database pool")
		_pool = await asyncpg.create_pool(
			host=DB_HOST,
			port=DB_PORT,
			user=DB_USER,
			password=DB_PASSWORD,
			database=DB_NAME,
			min_size=1,
			max_size=5,
		)
		async with _pool.acquire() as conn:
			await _ensure_schema(conn)
			await _seed_initial_data(conn)
	return _pool


def get_db_pool() -> Optional["asyncpg.Pool"]:
	"""Return the global database pool if initialized."""
	return _pool


async def close_db_pool() -> None:
	"""Gracefully close the global database pool."""
	global _pool
	if _pool is not None:
		await _pool.close()
		_pool = None


async def _ensure_schema(conn: "asyncpg.Connection") -> None:
	"""Create required tables if they don't already exist."""
	# Users table
	await conn.execute(
		"""
		CREATE TABLE IF NOT EXISTS users (
			id SERIAL PRIMARY KEY,
			telegram_id BIGINT UNIQUE NOT NULL,
			username TEXT,
			first_name TEXT,
			last_name TEXT,
			language TEXT DEFAULT 'uz',
			role TEXT DEFAULT 'client',
			is_bot BOOLEAN DEFAULT FALSE,
			created_at TIMESTAMP DEFAULT NOW(),
			updated_at TIMESTAMP DEFAULT NOW()
		);
		"""
	)
	# Orders table (generic orders for multiple roles)
	await conn.execute(
		"""
		CREATE TABLE IF NOT EXISTS orders (
			id SERIAL PRIMARY KEY,
			user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
			order_type TEXT NOT NULL,                                 -- 'service' | 'connection' | etc
			status TEXT NOT NULL,                                      -- 'new' | 'pending' | 'in_progress' | 'assigned' | 'completed' | 'cancelled'
			priority TEXT DEFAULT 'medium',                            -- 'low' | 'medium' | 'high' | 'urgent'
			description TEXT,
			region TEXT,
			address TEXT,
			assigned_to TEXT,                                          -- technician or responsible person name
			created_at TIMESTAMP DEFAULT NOW(),
			updated_at TIMESTAMP DEFAULT NOW()
		);
		"""
	)
	# Inventory table
	await conn.execute(
		"""
		CREATE TABLE IF NOT EXISTS inventory (
			id SERIAL PRIMARY KEY,
			name TEXT NOT NULL,
			quantity INTEGER NOT NULL DEFAULT 0,
			unit TEXT DEFAULT 'dona',
			price NUMERIC(12, 2) DEFAULT 0,
			min_quantity INTEGER DEFAULT 0,
			category TEXT,
			description TEXT,
			created_at TIMESTAMP DEFAULT NOW(),
			updated_at TIMESTAMP DEFAULT NOW()
		);
		"""
	)


async def _seed_initial_data(conn: "asyncpg.Connection") -> None:
	"""Insert lightweight demo data if tables are empty to ensure handlers show something."""
	# Seed inventory
	inv_count = await conn.fetchval("SELECT COUNT(*) FROM inventory")
	if inv_count == 0:
		await conn.executemany(
			"""
			INSERT INTO inventory (name, quantity, unit, price, min_quantity, category, description)
			VALUES ($1, $2, $3, $4, $5, $6, $7)
			""",
			[
				("Cable", 50, "dona", 15000, 10, "cables", "Internet kabeli"),
				("Router", 10, "dona", 500000, 5, "equipment", "WiFi router"),
				("Connector", 100, "dona", 5000, 15, "equipment", "RJ45 connector"),
			],
		)
		logger.info("Seeded demo inventory data")

	# Seed a demo user (for controller views we don't strictly need user link)
	users_count = await conn.fetchval("SELECT COUNT(*) FROM users")
	if users_count == 0:
		await conn.execute(
			"""
			INSERT INTO users (telegram_id, username, first_name, last_name, language, role, is_bot)
			VALUES (1234567890, 'demo_user', 'Demo', 'User', 'uz', 'client', FALSE)
			ON CONFLICT (telegram_id) DO NOTHING
			"""
		)
		logger.info("Seeded demo user")

	# Seed some orders for controller to view
	orders_count = await conn.fetchval("SELECT COUNT(*) FROM orders")
	if orders_count == 0:
		user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = 1234567890")
		orders: List[Tuple[Any, ...]] = [
			("service", "new", "Yuqori tezlikdagi internet muammosi", "Toshkent shahri", "Chilanzar tumani, 15-uy", "Aziz Karimov", "high"),
			("connection", "in_progress", "Yangi ulanish", "Toshkent viloyati", "Zangiota tumani, 25-uy", "Malika Yusupova", "medium"),
			("service", "completed", "Router sozlamalari", "Samarqand", "Samarqand shahri, 30-uy", "Bekzod Azimov", "low"),
		]
		await conn.executemany(
			"""
			INSERT INTO orders (user_id, order_type, status, description, region, address, assigned_to, priority)
			VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
			""",
			[(user_id, *o) for o in orders],
		)
		logger.info("Seeded demo orders")


# =========================
# Users API
# =========================
async def upsert_user(user_id: int, user_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
	"""
	Create or update a user record by Telegram user_id.
	This mirrors the mock function signature used in handlers.
	Returns (is_created, saved_record)
	"""
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		existing = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", user_id)
		if existing is None:
			row = await conn.fetchrow(
				"""
				INSERT INTO users (telegram_id, username, first_name, last_name, language, role, is_bot)
				VALUES ($1, $2, $3, $4, $5, $6, $7)
				RETURNING *
				""",
				user_id,
				user_data.get("username"),
				user_data.get("first_name"),
				user_data.get("last_name"),
				user_data.get("language", "uz"),
				user_data.get("role", "client"),
				bool(user_data.get("is_bot", False)),
			)
			return True, dict(row)
		else:
			row = await conn.fetchrow(
				"""
				UPDATE users
				SET username = $2,
					first_name = $3,
					last_name = $4,
					language = $5,
					role = $6,
					is_bot = $7,
					updated_at = NOW()
				WHERE telegram_id = $1
				RETURNING *
				""",
				user_id,
				user_data.get("username"),
				user_data.get("first_name"),
				user_data.get("last_name"),
				user_data.get("language", existing.get("language", "uz")),
				user_data.get("role", existing.get("role", "client")),
				bool(user_data.get("is_bot", existing.get("is_bot", False))),
			)
			return False, dict(row)


async def get_user_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
		return dict(row) if row else None


# =========================
# Orders API
# =========================

def _status_uz(status_internal: str) -> str:
	return {
		"new": "Yangi",
		"pending": "Kutilmoqda",
		"in_progress": "Jarayonda",
		"assigned": "Jarayonda",
		"completed": "Bajarilgan",
		"cancelled": "Bekor qilingan",
	}.get(status_internal, status_internal)


def _priority_uz(priority: str) -> str:
	return {
		"low": "Past",
		"medium": "O'rta",
		"high": "Yuqori",
		"urgent": "Shoshilinch",
	}.get(priority, priority)


def _service_type_uz(order_type: str) -> str:
	return "Texnik xizmati" if order_type == "service" else "Internet xizmati"


async def get_user_orders(telegram_id: int, page: int = 1, limit: int = 5) -> Dict[str, Any]:
	"""Return paginated orders for a given Telegram user id for Client handlers."""
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		user_id = await conn.fetchval("SELECT id FROM users WHERE telegram_id = $1", telegram_id)
		if not user_id:
			return {"orders": [], "total": 0, "page": page, "total_pages": 0}
		total: int = await conn.fetchval("SELECT COUNT(*) FROM orders WHERE user_id = $1", user_id)
		offset = max(0, (page - 1) * limit)
		rows = await conn.fetch(
			"""
			SELECT id, order_type, status, description, region, address, created_at
			FROM orders
			WHERE user_id = $1
			ORDER BY created_at DESC
			LIMIT $2 OFFSET $3
			""",
			user_id,
			limit,
			offset,
		)
		orders: List[Dict[str, Any]] = []
		for r in rows:
			created_at_str = r["created_at"].strftime("%Y-%m-%d %H:%M:%S") if r["created_at"] else ""
			orders.append(
				{
					"id": r["id"],
					"type": r["order_type"],
					"status": {
						"new": "active",
						"pending": "pending",
						"in_progress": "active",
						"assigned": "active",
						"completed": "completed",
						"cancelled": "cancelled",
					}.get(r["status"], r["status"]),
					"created_at": created_at_str,
					"description": r["description"] or "",
					"region": r["region"] or "",
					"address": r["address"] or "",
					"request_id": f"{'TX' if r['order_type']=='service' else 'UL'}_{r['id']:08d}",
				}
			)
		total_pages = (total + limit - 1) // limit if total else 0
		return {"orders": orders, "total": total, "page": page, "total_pages": total_pages}


async def get_order_details(order_id: int) -> Optional[Dict[str, Any]]:
	"""Get rich order details for Client handler."""
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			SELECT o.*, u.first_name || ' ' || COALESCE(u.last_name,'') AS full_name
			FROM orders o
			LEFT JOIN users u ON u.id = o.user_id
			WHERE o.id = $1
			""",
			order_id,
		)
		if not row:
			return None
		created_at_str = row["created_at"].strftime("%Y-%m-%d %H:%M:%S") if row["created_at"] else ""
		return {
			"id": row["id"],
			"type": row["order_type"],
			"status": {
				"new": "active",
				"pending": "pending",
				"in_progress": "active",
				"assigned": "active",
				"completed": "completed",
				"cancelled": "cancelled",
			}.get(row["status"], row["status"]),
			"created_at": created_at_str,
			"description": row["description"] or "",
			"region": row["region"] or "",
			"address": row["address"] or "",
			"request_id": f"{'TX' if row['order_type']=='service' else 'UL'}_{row['id']:08d}",
			"phone": "",
			"full_name": row.get("full_name", "") or "",
		}


async def get_all_orders(limit: int = 50) -> List[Dict[str, Any]]:
	"""Return orders for Controller views with localized fields."""
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		rows = await conn.fetch(
			"""
			SELECT o.*, u.first_name || ' ' || COALESCE(u.last_name,'') AS client_name
			FROM orders o
			LEFT JOIN users u ON u.id = o.user_id
			ORDER BY o.created_at DESC
			LIMIT $1
			""",
			limit,
		)
		orders: List[Dict[str, Any]] = []
		for r in rows:
			orders.append(
				{
					"id": r["id"],
					"order_number": f"ORD-{r['id']:03d}",
					"client_name": r.get("client_name", "Test Client"),
					"service_type": _service_type_uz(r["order_type"]),
					"status": _status_uz(r["status"]),
					"priority": _priority_uz(r.get("priority", "medium")),
					"created_at": (r["created_at"].strftime("%Y-%m-%d %H:%M") if r["created_at"] else ""),
					"assigned_to": r.get("assigned_to", "Tayinlanmagan") or "Tayinlanmagan",
					"description": r.get("description", "") or "",
				}
			)
		return orders


async def get_orders_by_status(statuses: List[str]) -> List[Dict[str, Any]]:
	"""Filter orders by internal statuses for Controller. Accepts english codes like 'new', 'pending'."""
	if not statuses:
		return await get_all_orders()
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		rows = await conn.fetch(
			"""
			SELECT o.*, u.first_name || ' ' || COALESCE(u.last_name,'') AS client_name
			FROM orders o
			LEFT JOIN users u ON u.id = o.user_id
			WHERE o.status = ANY($1::text[])
			ORDER BY o.created_at DESC
			LIMIT 200
			""",
			statuses,
		)
		orders: List[Dict[str, Any]] = []
		for r in rows:
			orders.append(
				{
					"id": r["id"],
					"order_number": f"ORD-{r['id']:03d}",
					"client_name": r.get("client_name", "Test Client"),
					"service_type": _service_type_uz(r["order_type"]),
					"status": _status_uz(r["status"]),
					"priority": _priority_uz(r.get("priority", "medium")),
					"created_at": (r["created_at"].strftime("%Y-%m-%d %H:%M") if r["created_at"] else ""),
					"assigned_to": r.get("assigned_to", "Tayinlanmagan") or "Tayinlanmagan",
					"description": r.get("description", "") or "",
				}
			)
		return orders


async def get_single_order_details(order_id: int) -> Optional[Dict[str, Any]]:
	"""Detailed order for Controller view with localized fields."""
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		r = await conn.fetchrow(
			"""
			SELECT o.*, u.first_name || ' ' || COALESCE(u.last_name,'') AS client_name
			FROM orders o
			LEFT JOIN users u ON u.id = o.user_id
			WHERE o.id = $1
			""",
			order_id,
		)
		if not r:
			return None
		return {
			"id": r["id"],
			"order_number": f"ORD-{r['id']:03d}",
			"client_name": r.get("client_name", "Test Client"),
			"service_type": _service_type_uz(r["order_type"]),
			"status": _status_uz(r["status"]),
			"priority": _priority_uz(r.get("priority", "medium")),
			"created_at": (r["created_at"].strftime("%Y-%m-%d %H:%M") if r["created_at"] else ""),
			"assigned_to": r.get("assigned_to", "Tayinlanmagan") or "Tayinlanmagan",
			"description": r.get("description", "") or "",
		}


# =========================
# Inventory API
# =========================
async def get_all_inventory_items() -> List[Dict[str, Any]]:
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		rows = await conn.fetch("SELECT * FROM inventory ORDER BY name ASC")
		return [dict(r) for r in rows]


async def add_new_inventory_item(item_data: Dict[str, Any]) -> Optional[int]:
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		row = await conn.fetchrow(
			"""
			INSERT INTO inventory (name, quantity, unit, price, min_quantity, category, description)
			VALUES ($1, $2, $3, $4, $5, $6, $7)
			RETURNING id
			""",
			item_data.get("name"),
			int(item_data.get("quantity", 0)),
			item_data.get("unit", "dona"),
			float(item_data.get("price", 0)),
			int(item_data.get("min_quantity", 0)),
			item_data.get("category", "general"),
			item_data.get("description", ""),
		)
		return int(row["id"]) if row else None


async def update_inventory_item_data(item_id: int, update_data: Dict[str, Any]) -> bool:
	if not update_data:
		return False
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		# Build dynamic UPDATE statement
		columns = list(update_data.keys())
		set_clauses = []
		values: List[Any] = []
		for idx, col in enumerate(columns, start=1):
			set_clauses.append(f"{col} = ${idx}")
			values.append(update_data[col])
		values.append(item_id)
		query = f"UPDATE inventory SET {', '.join(set_clauses)}, updated_at = NOW() WHERE id = ${len(values)}"
		result = await conn.execute(query, *values)
		return result.upper().startswith("UPDATE")


async def get_inventory_item_by_id(item_id: int) -> Optional[Dict[str, Any]]:
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		row = await conn.fetchrow("SELECT * FROM inventory WHERE id = $1", item_id)
		return dict(row) if row else None


async def search_inventory_items(query: str) -> List[Dict[str, Any]]:
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		rows = await conn.fetch(
			"SELECT * FROM inventory WHERE LOWER(name) LIKE LOWER($1) OR LOWER(COALESCE(description,'')) LIKE LOWER($1) ORDER BY name ASC",
			f"%{query}%",
		)
		return [dict(r) for r in rows]


async def get_low_stock_inventory_items() -> List[Dict[str, Any]]:
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		rows = await conn.fetch("SELECT * FROM inventory WHERE quantity < min_quantity ORDER BY name ASC")
		return [dict(r) for r in rows]


async def get_out_of_stock_items() -> List[Dict[str, Any]]:
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		rows = await conn.fetch("SELECT * FROM inventory WHERE quantity <= 0 ORDER BY name ASC")
		return [dict(r) for r in rows]


async def delete_inventory_item(item_id: int) -> bool:
	pool = await init_db_pool() if get_db_pool() is None else get_db_pool()
	assert pool is not None
	async with pool.acquire() as conn:
		result = await conn.execute("DELETE FROM inventory WHERE id = $1", item_id)
		return result.upper().startswith("DELETE")


# Compatibility alias for handlers/client/orders.py
get_single_order = get_single_order_details