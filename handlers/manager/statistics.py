"""
Manager Statistics Handler

This module handles statistics and reports for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_statistics_router():
    """Get router for manager statistics"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.message(F.text.in_(["📊 Monitoring", "📊 Мониторинг"]))
    async def statistics_handler(message: Message, state: FSMContext):
        """Handle statistics request"""
        await message.answer(
            "📊 Statistika bo'limi hozircha ishlab chiqilmoqda...\n"
            "📊 Раздел статистики находится в разработке..."
        )
    
    return router