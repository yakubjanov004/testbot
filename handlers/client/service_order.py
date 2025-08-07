"""
Client Service Order Handler - Updated Implementation

This module handles service order creation for clients using shared ticket creation.
"""

import logging
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from handlers.shared_ticket_creation import start_ticket_creation

# Logger sozlash
logger = logging.getLogger(__name__)

def get_service_order_router():
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔧 Texnik xizmat"]))
    async def new_service_request(message: Message, state: FSMContext):
        """New service request handler"""
        try:
            await start_ticket_creation(message, state, "client")
        except Exception as e:
            logger.error(f"Error in new_service_request - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router

