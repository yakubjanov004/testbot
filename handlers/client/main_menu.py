"""
Client Main Menu Handler - Optimized Implementation

This module handles the main menu navigation for clients with improved state management.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_main_menu_keyboard
from states.client_states import MainMenuStates
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

async def get_user_role(user_id: int) -> str:
    """Mock get user role"""
    return 'client'

def get_client_main_menu_router():
    """Get client main menu router with optimized handlers"""
    router = get_role_router("client")

    @router.message(F.text.in_(["🏠 Asosiy menyu", "🏠 Главное меню"]))
    async def main_menu_handler(message: Message, state: FSMContext):
        """Optimized main menu handler with state management"""
        try:
            # Get user data from state or database
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang')
            
            # If language not in state, get from database
            if not user_lang:
                user = await get_user_by_telegram_id(message.from_user.id)
                if not user:
                    logger.error(f"User not found: {message.from_user.id}")
                    await message.answer("❌ Xatolik yuz berdi. Iltimos, /start buyrug'ini qayta yuboring.")
                    return
                    
                user_lang = user.get('language', 'uz')
                # Update state with user data
                await state.update_data(
                    user_id=user['id'],
                    user_lang=user_lang,
                    user_role=user['role'],
                    user_full_name=user['full_name'],
                    user_phone=user['phone_number']
                )
            
            # Clear any temporary data but keep user info
            temp_keys = ['order_type', 'region', 'description', 'media', 'location']
            for key in temp_keys:
                if key in state_data:
                    state_data.pop(key)
            await state.set_data(state_data)
            
            # Prepare main menu text
            main_menu_text = (
                "🏠 Asosiy menyu\n\n"
                "Quyidagi menyudan kerakli bo'limni tanlang:"
                if user_lang == 'uz' else
                "🏠 Главное меню\n\n"
                "Выберите нужный раздел из меню ниже:"
            )
            
            # Send main menu
            sent_message = await message.answer(
                text=main_menu_text,
                reply_markup=get_main_menu_keyboard(user_lang)
            )
            
            # Update state
            await state.update_data(last_message_id=sent_message.message_id)
            await state.set_state(MainMenuStates.main_menu)
            
            logger.info(f"User returned to main menu: {message.from_user.id}")
            
        except Exception as e:
            logger.error(f"Error in main_menu_handler: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu_callback(callback: CallbackQuery, state: FSMContext):
        """Handle callback for returning to main menu"""
        try:
            await callback.answer()
            
            # Get user language from state
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang')
            
            if not user_lang:
                user = await get_user_by_telegram_id(callback.from_user.id)
                user_lang = user.get('language', 'uz') if user else 'uz'
            
            # Clear temporary data
            temp_keys = ['order_type', 'region', 'description', 'media', 'location']
            for key in temp_keys:
                if key in state_data:
                    state_data.pop(key)
            await state.set_data(state_data)
            
            main_menu_text = (
                "🏠 Asosiy menyu\n\n"
                "Quyidagi menyudan kerakli bo'limni tanlang:"
                if user_lang == 'uz' else
                "🏠 Главное меню\n\n"
                "Выберите нужный раздел из меню ниже:"
            )
            
            # Edit message with main menu
            await callback.message.edit_text(
                text=main_menu_text,
                reply_markup=get_main_menu_keyboard(user_lang)
            )
            
            await state.set_state(MainMenuStates.main_menu)
            
        except Exception as e:
            logger.error(f"Error in back_to_main_menu_callback: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    # Universal back handler for any "Orqaga" button
    @router.message(F.text.in_(["◀️ Orqaga", "◀️ Назад"]))
    async def universal_back_handler(message: Message, state: FSMContext):
        """Universal handler for back button - returns to main menu"""
        await main_menu_handler(message, state)

    return router
