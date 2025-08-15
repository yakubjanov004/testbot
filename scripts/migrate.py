#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path

import asyncpg  # type: ignore
from dotenv import load_dotenv

# Load env
load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
CLIENTS_MIGR = ROOT / "database" / "clients" / "migrations"
REGIONAL_MIGR = ROOT / "database" / "migrations"


def _read_file(path: Path) -> str:
	with path.open("r", encoding="utf-8") as f:
		return f.read()


def _collect_sql_files(folder: Path) -> list[Path]:
	files = [p for p in folder.glob("*.sql") if p.is_file()]
	return sorted(files, key=lambda p: p.name)


async def _apply_sql(dsn: str, sql: str, name: str) -> None:
	conn = None
	try:
		conn = await asyncpg.connect(dsn)
		await conn.execute(sql)
		print(f"✅ Migration applied: {name}")
	finally:
		if conn:
			await conn.close()


async def main() -> int:
	# Clients DB
	clients_dsn = os.getenv("CLIENTS_DB_URL") or os.getenv("CLIENTS_DATABASE_URL")
	if clients_dsn:
		print("➡️  Applying clients migrations...")
		for sql_file in _collect_sql_files(CLIENTS_MIGR):
			await _apply_sql(clients_dsn, _read_file(sql_file), f"clients:{sql_file.name}")
	else:
		print("ℹ️  CLIENTS_DB_URL not set, skipping clients migrations")

	# Regional DBs discovered from env
	from database.region_config import get_region_dsn_map

	region_map = get_region_dsn_map()
	if not region_map:
		print("ℹ️  No regional DSNs discovered, skipping regional migrations")
		return 0

	region_sql_files = _collect_sql_files(REGIONAL_MIGR)
	for code, dsn in region_map.items():
		print(f"➡️  Applying regional migrations for '{code}'...")
		for sql_file in region_sql_files:
			await _apply_sql(dsn, _read_file(sql_file), f"region:{code}:{sql_file.name}")

	return 0


if __name__ == "__main__":
	try:
		code = asyncio.run(main())
		sys.exit(code)
	except KeyboardInterrupt:
		print("\nInterrupted")
		sys.exit(130)