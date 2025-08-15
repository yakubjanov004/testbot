"""
Centralized configuration for the bot.

Reads environment variables from .env (if present) and exposes a typed settings
object that other modules can import. Keeps parsing logic (IDs, log level, etc.)
in one place.
"""

import os
import logging
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

# Load .env early so all imports see the variables
load_dotenv()


def _parse_admin_ids(raw: str) -> List[int]:
	ids: List[int] = []
	for part in (raw or "").split(","):
		part = part.strip()
		if not part:
			continue
		try:
			ids.append(int(part))
		except ValueError:
			# Ignore invalid entries silently
			continue
	return ids


def _parse_group_id(raw: str) -> int:
	# Accept values with optional quotes and possible negative values for supergroups
	value = (raw or "0").strip().strip('"').strip("'")
	try:
		return int(value)
	except ValueError:
		return 0


@dataclass(frozen=True)
class Settings:
	bot_token: str
	admin_ids: List[int]
	bot_id: int
	zayavka_group_id: int
	log_level: str

	@property
	def numeric_log_level(self) -> int:
		lvl = (self.log_level or "INFO").upper()
		return getattr(logging, lvl, logging.INFO)

	@staticmethod
	def from_env() -> "Settings":
		bot_token = os.getenv("BOT_TOKEN", "").strip()
		admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))
		bot_id_str = os.getenv("BOT_ID", "0").strip()
		zayavka_group_id = _parse_group_id(os.getenv("ZAYAVKA_GROUP_ID", "0"))
		log_level = os.getenv("LOG_LEVEL", "INFO").strip()

		# Derive BOT_ID from token if not explicitly provided
		try:
			bot_id = int(bot_id_str)
		except ValueError:
			bot_id = 0
		if bot_id == 0 and bot_token and ":" in bot_token:
			try:
				bot_id = int(bot_token.split(":", 1)[0])
			except ValueError:
				bot_id = 0

		return Settings(
			bot_token=bot_token,
			admin_ids=admin_ids,
			bot_id=bot_id,
			zayavka_group_id=zayavka_group_id,
			log_level=log_level,
		)


# Eagerly load settings at import time
settings = Settings.from_env()


def get_settings() -> Settings:
	return settings