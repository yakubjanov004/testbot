"""
Admin Callbacks - minimal fallback router
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery
from filters.role_filter import RoleFilter


def get_admin_callbacks_router() -> Router:
    router = Router()

    role_filter = RoleFilter("admin")
    router.callback_query.filter(role_filter)

    # Generic handler for unhandled admin_* callbacks to avoid silent failures
    @router.callback_query(F.data.startswith("admin_"))
    async def handle_generic_admin_callbacks(callback: CallbackQuery):
        try:
            await callback.answer("Amal bajarildi", show_alert=False)
        except Exception:
            # Swallow any error to avoid breaking the flow
            pass

    return router