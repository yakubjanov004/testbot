from aiogram import Router
from aiogram.types import CallbackQuery
import logging

logger = logging.getLogger(__name__)


def get_unhandled_router() -> Router:
    """Router to catch and gracefully handle unregistered callback queries."""
    router = Router(name="unhandled_callbacks")

    @router.callback_query()
    async def _unhandled_callback(callback: CallbackQuery):
        """Catch-all fallback for unknown callback_data values."""
        logger.warning(
            "Unhandled callback_data received: %s from user %s",
            callback.data,
            callback.from_user.id,
        )
        # Alert user that the feature is not yet implemented
        try:
            await callback.answer("🔧 Bu tugma hozircha ishlamayapti.", show_alert=True)
        except Exception as e:
            # Even if answering fails, log the problem but avoid raising to stop the bot
            logger.error("Error sending unhandled callback alert: %s", e, exc_info=True)

    return router