"""
Start Handler - Simplified Implementation

This module handles the /start command and shows appropriate menus
based on user role.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loader import get_user_role
from utils.role_system import show_role_menu

def get_start_router():
    """Get start router with all handlers"""
    router = Router()
    
    @router.message(F.text == "/start")
    async def start_command(message: Message, state: FSMContext):
        """Handle /start command"""
        try:
            user_role = get_user_role(message.from_user.id)
            
            # Clear any existing state
            await state.clear()
            
            # Show welcome message
            welcome_text = (
                f"👋 Xush kelibsiz, {message.from_user.first_name}!\n\n"
                f"🤖 Alfa Connect botiga xush kelibsiz!\n"
                f"👤 Sizning rolingiz: {user_role.upper()}\n\n"
                f"Quyidagi menyulardan birini tanlang:"
            )
            
            await message.answer(welcome_text)
            
            # Show appropriate menu based on role
            if user_role == 'client':
                from keyboards.client_buttons import get_main_menu_keyboard
                keyboard = get_main_menu_keyboard('uz')
                await message.answer("Quyidagi menyudan kerakli bo'limni tanlang.", reply_markup=keyboard)
            else:
                await show_role_menu(message, user_role)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    
    return router 