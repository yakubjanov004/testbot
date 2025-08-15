"""
Manager Statistics Handler

This module handles statistics and reporting functionality for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_statistics_router():
    """Get manager statistics router"""
    router = Router()
    router.message.filter(RoleFilter("manager"))
    
    @router.message(F.text == "📊 Monitoring")
    async def show_statistics(message: Message, state: FSMContext):
        """Show statistics menu"""
        await message.answer("📊 Statistika va monitoring funksiyalari keyinchalik qo'shiladi.")
    
    return router