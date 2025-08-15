"""
Manager Technician Assignment Handler

This module handles technician assignment functionality for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_manager_technician_assignment_router():
    """Get manager technician assignment router"""
    router = Router()
    router.message.filter(RoleFilter("manager"))
    
    @router.message(F.text == "👥 Xodimlar faoliyati")
    async def show_staff_activity(message: Message, state: FSMContext):
        """Show staff activity menu"""
        await message.answer("👥 Xodimlar faoliyati funksiyalari keyinchalik qo'shiladi.")
    
    return router