"""
Junior Manager Language Handler
Manages language settings for junior manager
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.junior_manager_buttons import get_language_keyboard
from states.junior_manager_states import JuniorManagerLanguageStates
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
async def set_user_language(user_id: int, language: str):
    """Mock set user language"""
    print(f"Mock: Setting user {user_id} language to {language}")
    return True

async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerLanguageStates(StatesGroup):
    changing_language = State()

def get_junior_manager_language_router():
    """Get junior manager language router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🌐 Tilni o'zgartirish"]))
    async def change_language(message: Message):
        """Handle language change request"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            text = (
                "🌐 <b>Tilni o'zgartirish</b>\n\n"
                "Kerakli tilni tanlang:"
            )
            
            await message.answer(
                text,
                reply_markup=get_language_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in change_language: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    return router 
