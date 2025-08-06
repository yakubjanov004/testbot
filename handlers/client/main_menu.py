"""
Client Main Menu Handler - Simplified Implementation

This module handles the main menu for clients.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_main_menu_keyboard
from states.client_states import MainMenuStates

def get_client_main_menu_router():
    router = Router()

    @router.message(F.text.in_(["🏠 Asosiy menyu", "🏠 Главное меню"]))
    async def main_menu_handler(message: Message, state: FSMContext):
        """Client main menu handler"""
        try:
            main_menu_text = "Quyidagi menyudan kerakli bo'limni tanlang."
            
            sent_message = await message.answer(
                text=main_menu_text,
                reply_markup=get_main_menu_keyboard('uz')
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
            
            main_menu_text = "Quyidagi menyudan kerakli bo'limni tanlang."
            
            await callback.message.edit_text(
                text=main_menu_text,
                reply_markup=get_main_menu_keyboard('uz')
            )
            
            await state.set_state(MainMenuStates.main_menu)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router
