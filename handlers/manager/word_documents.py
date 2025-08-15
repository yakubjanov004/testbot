"""
Manager Word Documents Handler

This module handles word document generation for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_word_documents_router():
    """Get router for manager word documents"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("generate_word_"))
    async def generate_word_handler(callback: CallbackQuery, state: FSMContext):
        """Handle word document generation"""
        await callback.answer("Word hujjat yaratish funksiyasi ishlab chiqilmoqda...")
    
    return router