"""
Unhandled Callbacks Router
Catches any unprocessed callback_data to prevent silent failures.
"""

from aiogram import Router
from aiogram.types import CallbackQuery


def get_unhandled_router() -> Router:
    router = Router()

    @router.callback_query()
    async def handle_unknown(callback: CallbackQuery):
        try:
            await callback.answer("❔ Noma'lum amal", show_alert=False)
        except Exception:
            # In case answering fails (message too old etc.)
            pass

    return router