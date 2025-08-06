"""
Manager Main Menu Handler - Soddalashtirilgan versiya

Bu modul manager uchun asosiy menyu funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from filters.role_filter import RoleFilter

from keyboards.manager_buttons import get_manager_main_keyboard
from states.manager_states import ManagerMainMenuStates

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

def get_manager_main_menu_router():
    """Get manager main menu router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["/start", "🏠 Asosiy menyu"]))
    async def manager_main_menu_handler(message: Message, state: FSMContext):
        """Manager main menu handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            main_menu_text = "Menejer paneliga xush kelibsiz! Quyidagi menyudan kerakli bo'limni tanlang."
            
            sent_message = await message.answer(
                text=main_menu_text,
                reply_markup=get_manager_main_keyboard(lang)
            )
            
            await state.update_data(last_message_id=sent_message.message_id)
            await state.set_state(ManagerMainMenuStates.main_menu)
            
        except Exception as e:
            print(f"Error in manager_main_menu_handler: {str(e)}")
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data == "manager_back_to_main")
    async def manager_back_to_main_handler(callback: CallbackQuery, state: FSMContext):
        """Handle manager back to main menu button"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            main_menu_text = "Menejer paneliga xush kelibsiz! Quyidagi menyudan kerakli bo'limni tanlang."
            
            await callback.message.edit_text(
                text=main_menu_text,
                reply_markup=get_manager_main_keyboard(lang)
            )
            
            await state.set_state(ManagerMainMenuStates.main_menu)
            
        except Exception as e:
            await callback.message.answer("❌ Xatolik yuz berdi")

    return router