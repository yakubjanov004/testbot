"""
Manager Notifications Handler

This module handles notifications functionality for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_notifications_router():
    """Get manager notifications router"""
    router = Router()
    router.message.filter(RoleFilter("manager"))
    
    @router.message(F.text == "🔔 Bildirishnomalar")
    async def show_notifications(message: Message, state: FSMContext):
        """Show notifications menu"""
        await message.answer("🔔 Bildirishnomalar funksiyalari keyinchalik qo'shiladi.")
    
    return router