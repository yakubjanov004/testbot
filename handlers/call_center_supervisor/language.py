"""
Call Center Supervisor Language Handler - Simplified Implementation

This module handles language settings for call center supervisors.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.call_center_supervisor_buttons import get_language_keyboard
from states.call_center_supervisor_states import LanguageStates

def get_call_center_supervisor_language_router():
    router = Router()

    @router.message(F.text.in_(["🌐 Til", "🌐 Язык"]))
    async def language_menu(message: Message, state: FSMContext):
        """Show language selection menu"""
        try:
            await message.answer(
                "Tilni tanlang / Выберите язык:",
                reply_markup=get_language_keyboard()
            )
            await state.set_state(LanguageStates.selecting_language)
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("lang_"))
    async def select_language(callback: CallbackQuery, state: FSMContext):
        """Handle language selection"""
        try:
            await callback.answer()
            language = callback.data.split("_")[1]
            
            # Update user language (mock)
            await state.update_data(language=language)
            
            success_text = "✅ Til muvaffaqiyatli o'zgartirildi!" if language == "uz" else "✅ Язык успешно изменен!"
            await callback.message.edit_text(success_text)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router 
