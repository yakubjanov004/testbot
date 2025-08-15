"""
Junior Manager Staff Application Creation Handler

This module handles staff application creation functionality for junior managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_junior_manager_staff_application_router():
    """Get junior manager staff application router"""
    router = Router()
    router.message.filter(RoleFilter("junior_manager"))
    
    @router.message(F.text == "👥 Xodim arizasi yaratish")
    async def show_staff_application(message: Message, state: FSMContext):
        """Show staff application menu"""
        await message.answer("👥 Xodim arizasi yaratish funksiyalari keyinchalik qo'shiladi.")
    
    return router