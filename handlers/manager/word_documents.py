"""
Manager Word Documents Handler

This module handles word document generation functionality for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_word_documents_router():
    """Get manager word documents router"""
    router = Router()
    router.message.filter(RoleFilter("manager"))
    
    @router.message(F.text == "📤 Export")
    async def show_export_menu(message: Message, state: FSMContext):
        """Show export menu"""
        await message.answer("📤 Export va hujjat yaratish funksiyalari keyinchalik qo'shiladi.")
    
    return router