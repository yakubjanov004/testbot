from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Client:
	id: Optional[int] = None
	telegram_id: Optional[int] = None
	full_name: Optional[str] = None
	username: Optional[str] = None
	phone: Optional[str] = None
	language: str = "uz"
	is_active: bool = True
	address: Optional[str] = None
	abonent_id: Optional[str] = None
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None