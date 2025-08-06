"""
Manager Main Menu Handler - Simplified Implementation

This module handles the main menu for managers.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_main_keyboard
from states.manager_states import ManagerMainMenuStates

def get_manager_main_menu_router():
    """Get manager main menu router"""
    router = Router()

    @router.message(F.text.in_(["/start", "🏠 Asosiy menyu"]))
    async def manager_main_menu_handler(message: Message, state: FSMContext):
        """Manager main menu handler"""
        try:
            main_menu_text = "Menejer paneliga xush kelibsiz! Quyidagi menyudan kerakli bo'limni tanlang."
            
            sent_message = await message.answer(
                text=main_menu_text,
                reply_markup=get_manager_main_keyboard('uz')
            )
            
            await state.update_data(last_message_id=sent_message.message_id)
            await state.set_state(ManagerMainMenuStates.main_menu)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router