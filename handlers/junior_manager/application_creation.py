"""
Junior Manager Application Creation Handler

This module handles application creation for junior managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_junior_manager_application_creation_router():
    """Get router for junior manager application creation"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("create_application_"))
    async def create_application_handler(callback: CallbackQuery, state: FSMContext):
        """Handle application creation"""
        await callback.answer("Ariza yaratish funksiyasi ishlab chiqilmoqda...")
    
    return router