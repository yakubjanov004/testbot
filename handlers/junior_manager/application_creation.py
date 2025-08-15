"""
Junior Manager Application Creation Handler

This module handles application creation functionality for junior managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_junior_manager_application_creation_router():
    """Get junior manager application creation router"""
    router = Router()
    router.message.filter(RoleFilter("junior_manager"))
    
    @router.message(F.text == "🔌 Ulanish arizasi yaratish")
    async def show_application_creation(message: Message, state: FSMContext):
        """Show application creation menu"""
        await message.answer("🔌 Ulanish arizasi yaratish funksiyalari keyinchalik qo'shiladi.")
    
    return router