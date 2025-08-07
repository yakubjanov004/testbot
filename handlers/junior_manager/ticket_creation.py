"""
Junior Manager Ticket Creation Handler

This module handles ticket creation for junior managers using shared ticket creation.
Junior managers can only create connection requests, not technical service requests.
"""

import logging
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from handlers.shared_ticket_creation import start_ticket_creation

# Logger sozlash
logger = logging.getLogger(__name__)

def get_junior_manager_ticket_creation_router():
    """Get junior manager ticket creation router"""
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def start_connection_order(message: Message, state: FSMContext):
        """Start connection order creation for junior manager"""
        try:
            await start_ticket_creation(message, state, "junior_manager")
        except Exception as e:
            logger.error(f"Error in start_connection_order - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router