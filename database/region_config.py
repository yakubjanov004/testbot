"""Region configuration loader.

Discovers region -> DSN mapping from environment variables.
B-variant: use env vars with prefix DB_URL_ e.g. DB_URL_TOSHKENT, DB_URL_SAMARQAND, ...
"""

import os
from typing import Dict, List


def get_region_dsn_map() -> Dict[str, str]:
	"""Return mapping of region_code (lowercase) -> DSN from environment.

	Looks for all env keys that start with 'DB_URL_' and maps the suffix (lowercased)
	to its DSN value.
	"""
	dsns: Dict[str, str] = {}
	for key, value in os.environ.items():
		if not key.startswith("DB_URL_"):
			continue
		region_code = key[len("DB_URL_"):].lower()
		if value:
			dsns[region_code] = value
	return dsns


def get_region_codes() -> List[str]:
	"""Return available region codes discovered from environment."""
	return sorted(get_region_dsn_map().keys())


def get_dsn_for_region(region_code: str) -> str:
	"""Get DSN for a specific region code (case-insensitive).

	Raises KeyError if not found.
	"""
	m = get_region_dsn_map()
	code = (region_code or "").lower()
	if code not in m:
		raise KeyError(f"No DSN configured for region '{region_code}' (env DB_URL_{region_code.upper()})")
	return m[code]