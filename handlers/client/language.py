"""
Client Language Handler - Simplified Implementation

This module handles client language selection functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_language_keyboard, get_main_menu_keyboard
from states.client_states import LanguageStates
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

async def update_user_language(user_id: int, language: str):
    """Mock update user language"""
    return True

def get_client_language_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["🌐 Til", "🌐 Язык"]))
    async def client_language_handler(message: Message, state: FSMContext):
        """Client language handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            lang = user.get('language', 'uz')
            
            language_text = (
                "Tilni tanlang:"
                if lang == 'uz' else
                "Выберите язык:"
            )
            
            sent_message = await message.answer(
                text=language_text,
                reply_markup=get_language_keyboard()
            )
            
            await state.set_state(LanguageStates.selecting_language)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("lang_"))
    async def handle_language_selection(callback: CallbackQuery, state: FSMContext):
        """Handle language selection"""
        try:
            await callback.answer()
            
            selected_lang = callback.data.split("_")[1]
            
            # Update user language
            success = await update_user_language(callback.from_user.id, selected_lang)
            
            if success:
                success_text = (
                    f"✅ Til muvaffaqiyatli o'zgartirildi: {'O\'zbekcha' if selected_lang == 'uz' else 'Русский'}"
                    if selected_lang == 'uz' else
                    f"✅ Язык успешно изменен: {'O\'zbekcha' if selected_lang == 'uz' else 'Русский'}"
                )
                
                await callback.message.edit_text(
                    text=success_text,
                    reply_markup=get_main_menu_keyboard(selected_lang)
                )
                
                await state.clear()
            else:
                error_text = (
                    "❌ Til o'zgartirishda xatolik yuz berdi."
                    if selected_lang == 'uz' else
                    "❌ Ошибка при изменении языка."
                )
                
                await callback.message.edit_text(error_text)
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "cancel_language")
    async def cancel_language_selection(callback: CallbackQuery, state: FSMContext):
        """Cancel language selection"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            cancel_text = (
                "❌ Til o'zgartirish bekor qilindi."
                if lang == 'uz' else
                "❌ Изменение языка отменено."
            )
            
            await callback.message.edit_text(
                text=cancel_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.clear()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router
