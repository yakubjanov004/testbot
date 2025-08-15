"""
Junior Manager Staff Application Creation Handler

This module handles staff application creation for junior managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_junior_manager_staff_application_router():
    """Get router for junior manager staff application creation"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("staff_application_"))
    async def staff_application_handler(callback: CallbackQuery, state: FSMContext):
        """Handle staff application creation"""
        await callback.answer("Xodim arizasi yaratish funksiyasi ishlab chiqilmoqda...")
    
    return router