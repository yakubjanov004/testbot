from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

from config import settings, get_admin_regions
from utils.db import get_pool, get_clients_pool
from database.region_config import get_region_codes


async def _check_pool(name: str) -> str:
    pool = await get_pool(name)
    if not pool:
        return f"{name}: not configured"
    try:
        async with pool.acquire() as conn:
            await conn.execute("SELECT 1")
        return f"{name}: OK"
    except Exception as e:
        return f"{name}: ERROR ({e})"


async def _check_clients() -> str:
    pool = await get_clients_pool()
    if not pool:
        return "clients: not configured"
    try:
        async with pool.acquire() as conn:
            await conn.execute("SELECT 1")
        return "clients: OK"
    except Exception as e:
        return f"clients: ERROR ({e})"


def get_admin_status_router() -> Router:
    router = Router()

    @router.message(Command("status"))
    async def status(message: Message):
        if message.from_user.id not in settings.admin_ids:
            return
        regions = get_region_codes()
        checks = [_check_pool(region) for region in regions]
        checks.append(_check_clients())
        results = await asyncio.gather(*checks, return_exceptions=False)
        assigned_regions = get_admin_regions(message.from_user.id)
        text = "\n".join([
            "🔎 DB status:",
            *results,
            "",
            f"👮‍♂️ Siz admin bo'lgan regionlar: {', '.join(assigned_regions) if assigned_regions else '—'}",
        ])
        await message.answer(text)

    return router