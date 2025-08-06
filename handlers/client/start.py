"""
Client Start Handler - Optimized Implementation

This module handles client start functionality with improved error handling and state management.
"""

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_main_menu_keyboard
from states.client_states import StartStates, MainMenuStates
from utils.role_system import get_role_router
import logging

# Logger setup
logger = logging.getLogger(__name__)

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
    """Get client start router with optimized handlers"""
    router = get_role_router("client")

    @router.message(F.text.in_(["🚀 Boshlash", "🚀 Начать"]))
    async def client_start_handler(message: Message, state: FSMContext):
        """Optimized client start handler with better error handling"""
        try:
            # Clear any previous state
            await state.clear()
            
            # Get user information
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                logger.error(f"User not found for telegram_id: {message.from_user.id}")
                await message.answer("❌ Foydalanuvchi topilmadi. Iltimos, administrator bilan bog'laning.")
                return
            
            # Get user language
            lang = user.get('language', 'uz')
            
            # Store user data in state for future use
            await state.update_data(
                user_id=user['id'],
                user_lang=lang,
                user_role=user['role'],
                user_full_name=user['full_name'],
                user_phone=user['phone_number']
            )
            
            # Prepare welcome message
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
            
            # Send welcome message with main menu
            sent_message = await message.answer(
                text=welcome_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            # Update state with message ID for future reference
            await state.update_data(last_message_id=sent_message.message_id)
            
            # Set state to main menu
            await state.set_state(MainMenuStates.main_menu)
            
            logger.info(f"Client started successfully: {user['telegram_id']}")
            
        except Exception as e:
            logger.error(f"Error in client_start_handler: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router