"""
Manager Notifications Handler

This module handles notifications for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_notifications_router():
    """Get router for manager notifications"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("notification_"))
    async def notification_handler(callback: CallbackQuery, state: FSMContext):
        """Handle notifications"""
        await callback.answer("Bildirishnoma funksiyasi ishlab chiqilmoqda...")
    
    return router