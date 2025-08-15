"""
Junior Manager Application Viewing Handler

This module handles application viewing functionality for junior managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_junior_manager_application_viewing_router():
    """Get junior manager application viewing router"""
    router = Router()
    router.message.filter(RoleFilter("junior_manager"))
    
    @router.message(F.text == "📋 Arizalarni ko'rish")
    async def show_applications(message: Message, state: FSMContext):
        """Show applications menu"""
        await message.answer("📋 Arizalarni ko'rish funksiyalari keyinchalik qo'shiladi.")
    
    return router