"""
Junior Manager Details Input Handler

This module handles details input for junior managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_junior_manager_details_input_router():
    """Get router for junior manager details input"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("input_details_"))
    async def input_details_handler(callback: CallbackQuery, state: FSMContext):
        """Handle details input"""
        await callback.answer("Ma'lumot kiritish funksiyasi ishlab chiqilmoqda...")
    
    return router