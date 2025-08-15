"""
Warehouse Workflow Integration Handler

This module handles workflow integration functionality for warehouse staff.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_warehouse_workflow_router():
    """Get warehouse workflow integration router"""
    router = Router()
    router.message.filter(RoleFilter("warehouse"))
    
    @router.message(F.text == "🔄 Workflow integratsiyasi")
    async def show_workflow_integration(message: Message, state: FSMContext):
        """Show workflow integration menu"""
        await message.answer("🔄 Workflow integratsiyasi funksiyalari keyinchalik qo'shiladi.")
    
    return router