"""
Client Language Handler - Optimized Implementation

This module handles language selection and switching for clients.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_main_menu_keyboard
from states.client_states import LanguageStates, MainMenuStates
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

async def update_user_language(user_id: int, language: str) -> bool:
    """Mock update user language"""
    return True

def get_client_language_router():
    """Get client language router with optimized handlers"""
    router = get_role_router("client")

    @router.message(F.text.in_(["🌐 Til o'zgartirish", "🌐 Изменить язык"]))
    async def language_menu_handler(message: Message, state: FSMContext):
        """Handle language change request"""
        try:
            # Get current language from state or database
            state_data = await state.get_data()
            current_lang = state_data.get('user_lang')
            
            if not current_lang:
                user = await get_user_by_telegram_id(message.from_user.id)
                current_lang = user.get('language', 'uz') if user else 'uz'
            
            # Prepare language selection text
            lang_text = (
                "🌐 Tilni tanlang:\n\n"
                f"Hozirgi til: {'🇺🇿 O\'zbek' if current_lang == 'uz' else '🇷🇺 Русский'}"
                if current_lang == 'uz' else
                "🌐 Выберите язык:\n\n"
                f"Текущий язык: {'🇺🇿 O\'zbek' if current_lang == 'uz' else '🇷🇺 Русский'}"
            )
            
            # Create language selection keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🇺🇿 O'zbek tili",
                        callback_data="set_lang_uz"
                    ),
                    InlineKeyboardButton(
                        text="🇷🇺 Русский язык",
                        callback_data="set_lang_ru"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="◀️ Orqaga" if current_lang == 'uz' else "◀️ Назад",
                        callback_data="back_to_main_menu"
                    )
                ]
            ])
            
            await message.answer(
                text=lang_text,
                reply_markup=keyboard
            )
            
            await state.set_state(LanguageStates.selecting_language)
            
        except Exception as e:
            logger.error(f"Error in language_menu_handler: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["set_lang_uz", "set_lang_ru"]))
    async def set_language_handler(callback: CallbackQuery, state: FSMContext):
        """Handle language selection"""
        try:
            await callback.answer()
            
            # Get new language
            new_lang = 'uz' if callback.data == "set_lang_uz" else 'ru'
            
            # Get user data
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
                return
            
            # Update language in database (mock)
            success = await update_user_language(user['id'], new_lang)
            
            if success:
                # Update language in state
                await state.update_data(user_lang=new_lang)
                
                # Success message
                success_text = (
                    "✅ Til muvaffaqiyatli o'zgartirildi!\n\n"
                    "Yangi til: 🇺🇿 O'zbek"
                    if new_lang == 'uz' else
                    "✅ Язык успешно изменен!\n\n"
                    "Новый язык: 🇷🇺 Русский"
                )
                
                await callback.message.edit_text(success_text)
                
                # Send main menu with new language
                await callback.message.answer(
                    "🏠 Asosiy menyu" if new_lang == 'uz' else "🏠 Главное меню",
                    reply_markup=get_main_menu_keyboard(new_lang)
                )
                
                await state.set_state(MainMenuStates.main_menu)
                
                logger.info(f"Language changed for user {user['telegram_id']}: {new_lang}")
                
            else:
                error_text = (
                    "❌ Tilni o'zgartirishda xatolik yuz berdi"
                    if new_lang == 'uz' else
                    "❌ Ошибка при изменении языка"
                )
                await callback.message.edit_text(error_text)
                
        except Exception as e:
            logger.error(f"Error in set_language_handler: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    # Quick language switch handlers
    @router.message(F.text == "🇺🇿 O'zbek")
    async def quick_switch_uz(message: Message, state: FSMContext):
        """Quick switch to Uzbek"""
        await state.update_data(user_lang='uz')
        await message.answer(
            "✅ Til o'zgartirildi: 🇺🇿 O'zbek",
            reply_markup=get_main_menu_keyboard('uz')
        )
        await state.set_state(MainMenuStates.main_menu)

    @router.message(F.text == "🇷🇺 Русский")
    async def quick_switch_ru(message: Message, state: FSMContext):
        """Quick switch to Russian"""
        await state.update_data(user_lang='ru')
        await message.answer(
            "✅ Язык изменен: 🇷🇺 Русский",
            reply_markup=get_main_menu_keyboard('ru')
        )
        await state.set_state(MainMenuStates.main_menu)

    return router
