"""
Junior Manager Application Viewing Handler

This module handles application viewing for junior managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_junior_manager_application_viewing_router():
    """Get router for junior manager application viewing"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("view_application_"))
    async def view_application_handler(callback: CallbackQuery, state: FSMContext):
        """Handle application viewing"""
        await callback.answer("Arizani ko'rish funksiyasi ishlab chiqilmoqda...")
    
    return router