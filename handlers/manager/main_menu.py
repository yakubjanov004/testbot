"""
Manager Main Menu Handler - Soddalashtirilgan versiya

Bu modul manager uchun asosiy menyu funksionalligini o'z ichiga oladi.
"""

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

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

async def cleanup_user_inline_messages(user_id: int):
    """Mock cleanup user inline messages"""
    print(f"Mock: Cleaning up inline messages for user {user_id}")

# Mock inline message manager
class MockInlineMessageManager:
    """Mock inline message manager"""
    async def track(self, user_id: int, message_id: int):
        """Mock track message"""
        print(f"Mock: Tracking message {message_id} for user {user_id}")

# Global mock instance
inline_message_manager = MockInlineMessageManager()

def get_manager_main_menu_router():
    """Get manager main menu router"""
    from aiogram import Router
    router = Router()

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
            await inline_message_manager.track(message.from_user.id, sent_message.message_id)
            
        except Exception as e:
            print(f"Error in manager_main_menu_handler: {str(e)}")
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    return router