"""
Junior Manager Workflow Management Handler

This module handles workflow management functionality for junior managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_junior_manager_workflow_router():
    """Get junior manager workflow router"""
    router = Router()
    router.message.filter(RoleFilter("junior_manager"))
    
    @router.message(F.text == "🔄 Workflow boshqaruvi")
    async def show_workflow_management(message: Message, state: FSMContext):
        """Show workflow management menu"""
        await message.answer("🔄 Workflow boshqaruvi funksiyalari keyinchalik qo'shiladi.")
    
    return router