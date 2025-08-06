"""
Client Start Handler - Simplified Implementation

This module handles client start functionality.
"""

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_main_menu_keyboard
from states.client_states import StartStates
from utils.role_system import get_role_router

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

def get_client_start_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["🚀 Boshlash", "🚀 Начать"]))
    async def client_start_handler(message: Message, state: FSMContext):
        """Client start handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            lang = user.get('language', 'uz')
            
            welcome_text = (
                f"👋 Xush kelibsiz, {message.from_user.first_name}!\n\n"
                f"🤖 Alfa Connect botiga xush kelibsiz!\n"
                f"📱 Sizning telefon raqamingiz: {user['phone_number']}\n"
                f"👤 To'liq ismingiz: {user['full_name']}\n\n"
                f"Quyidagi menyudan kerakli bo'limni tanlang:"
                if lang == 'uz' else
                f"👋 Добро пожаловать, {message.from_user.first_name}!\n\n"
                f"🤖 Добро пожаловать в бот Alfa Connect!\n"
                f"📱 Ваш номер телефона: {user['phone_number']}\n"
                f"👤 Ваше полное имя: {user['full_name']}\n\n"
                f"Выберите нужный раздел из меню ниже:"
            )
            
            sent_message = await message.answer(
                text=welcome_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.set_state(StartStates.started)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router