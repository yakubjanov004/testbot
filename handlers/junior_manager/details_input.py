"""
Junior Manager Details Input Handler

This module handles details input functionality for junior managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_junior_manager_details_input_router():
    """Get junior manager details input router"""
    router = Router()
    router.message.filter(RoleFilter("junior_manager"))
    
    @router.message(F.text == "📝 Ma'lumotlarni kiritish")
    async def show_details_input(message: Message, state: FSMContext):
        """Show details input menu"""
        await message.answer("📝 Ma'lumotlarni kiritish funksiyalari keyinchalik qo'shiladi.")
    
    return router