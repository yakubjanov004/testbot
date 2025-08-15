"""
Manager Technician Assignment Handler

This module handles technician assignment for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_technician_assignment_router():
    """Get router for manager technician assignment"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("assign_technician_"))
    async def assign_technician_handler(callback: CallbackQuery, state: FSMContext):
        """Handle technician assignment"""
        await callback.answer("Texnik tayinlash funksiyasi ishlab chiqilmoqda...")
    
    return router