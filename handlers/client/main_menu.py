"""
Client Main Menu Handler - Simplified Implementation

This module handles the main menu for clients.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_main_menu_keyboard
from states.client_states import MainMenuStates
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567'
    }

async def get_user_lang(user_id: int) -> str:
    """Mock get user language"""
    return 'uz'

async def get_user_role(user_id: int) -> str:
    """Mock get user role"""
    return 'client'

def get_client_main_menu_router():
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🏠 Asosiy menyu", "🏠 Главное меню"]))
    async def main_menu_handler(message: Message, state: FSMContext):
        """Client main menu handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            main_menu_text = (
                "Quyidagi menyudan kerakli bo'limni tanlang."
                if lang == 'uz' else
                "Выберите нужный раздел из меню ниже."
            )
            
            sent_message = await message.answer(
                text=main_menu_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.update_data(last_message_id=sent_message.message_id)
            await state.set_state(MainMenuStates.main_menu)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Back to main menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            main_menu_text = (
                "Quyidagi menyudan kerakli bo'limni tanlang."
                if lang == 'uz' else
                "Выберите нужный раздел из меню ниже."
            )
            
            await callback.message.edit_text(
                text=main_menu_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.set_state(MainMenuStates.main_menu)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router
