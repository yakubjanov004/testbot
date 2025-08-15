"""
Manager Reports Handler

This module handles reports generation for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_reports_router():
    """Get router for manager reports"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("report_"))
    async def report_handler(callback: CallbackQuery, state: FSMContext):
        """Handle report generation"""
        await callback.answer("Hisobot yaratish funksiyasi ishlab chiqilmoqda...")
    
    return router