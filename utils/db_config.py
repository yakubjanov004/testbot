"""
Database configuration helper

Centralizes reading database URLs from environment variables and provides
simple access helpers. This does not open connections; it only parses config.
"""

import os
from typing import Optional, Dict

from dotenv import load_dotenv

# Ensure env is loaded if this module is imported directly
load_dotenv()


def _read_env_url(name: str) -> Optional[str]:
    value = os.getenv(name, "").strip()
    return value or None


# Collect databases from common env names
_DATABASES: Dict[str, str] = {}

_default_url = _read_env_url("DATABASE_URL")
if _default_url:
    _DATABASES["default"] = _default_url

# Backward/alternative names supported for regions
_toshkent = _read_env_url("DATABASE_URL_TOSHKENT") or _read_env_url("DB_URL_TOSHKENT")
if _toshkent:
    _DATABASES["toshkent"] = _toshkent

_samarqand = _read_env_url("DATABASE_URL_SAMARQAND") or _read_env_url("DB_URL_SAMARQAND")
if _samarqand:
    _DATABASES["samarqand"] = _samarqand

_clients = _read_env_url("CLIENTS_DATABASE_URL") or _read_env_url("CLIENTS_DB_URL")
if _clients:
    _DATABASES["clients"] = _clients


# Optionally build default DSN from split parts if not provided
if "default" not in _DATABASES:
    host = os.getenv("DB_HOST", "").strip()
    port = os.getenv("DB_PORT", "").strip()
    user = os.getenv("DB_USER", "").strip()
    password = os.getenv("DB_PASSWORD", "").strip()
    name = os.getenv("DB_NAME", "").strip()
    if host and name and user:
        # Password is optional
        creds = f"{user}:{password}@" if password else f"{user}@"
        port_part = f":{port}" if port else ""
        _DATABASES["default"] = f"postgresql://{creds}{host}{port_part}/{name}"


DATABASES: Dict[str, str] = dict(_DATABASES)


def get_database_url(name: str = "default") -> Optional[str]:
    """Return database URL by name if configured."""
    return DATABASES.get(name)


__all__ = ["DATABASES", "get_database_url"]