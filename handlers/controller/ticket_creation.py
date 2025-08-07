"""
Controller Ticket Creation Handler

This module handles ticket creation for controllers using shared ticket creation.
"""

import logging
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from handlers.shared_ticket_creation import start_ticket_creation

# Logger sozlash
logger = logging.getLogger(__name__)

def get_controller_ticket_creation_router():
    """Get controller ticket creation router"""
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def start_connection_order(message: Message, state: FSMContext):
        """Start connection order creation for controller"""
        try:
            await start_ticket_creation(message, state, "controller")
        except Exception as e:
            logger.error(f"Error in start_connection_order - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish"]))
    async def start_technical_service(message: Message, state: FSMContext):
        """Start technical service creation for controller"""
        try:
            await start_ticket_creation(message, state, "controller")
        except Exception as e:
            logger.error(f"Error in start_technical_service - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router