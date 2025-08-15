"""
Manager Reports Handler

This module handles reports functionality for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_reports_router():
    """Get manager reports router"""
    router = Router()
    router.message.filter(RoleFilter("manager"))
    
    @router.message(F.text == "📊 Hisobotlar")
    async def show_reports(message: Message, state: FSMContext):
        """Show reports menu"""
        await message.answer("📊 Hisobotlar funksiyalari keyinchalik qo'shiladi.")
    
    return router