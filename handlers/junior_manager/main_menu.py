"""
Junior Manager Main Menu Handler
Manages main menu for junior manager
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.junior_manager_buttons import get_junior_manager_main_keyboard
from states.junior_manager_states import JuniorManagerMainMenuStates
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
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

def get_junior_manager_main_menu_router():
    """Get junior manager main menu router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["/start", "🏠 Asosiy menyu"]))
    async def show_main_menu(message: Message, state: FSMContext):
        """Show junior manager main menu"""
        user_id = message.from_user.id
        
        try:
            await state.clear()
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'junior_manager':
                text = "Sizda ruxsat yo'q."
                await message.answer(text)
                return
                
            await state.set_state(JuniorManagerMainMenuStates.main_menu)
            lang = user.get('language', 'uz')
            
            welcome_text = (
                "👨‍💼 <b>Junior Manager paneli</b>\n\n"
                "Xush kelibsiz! Quyidagi bo'limlardan birini tanlang:"
            )
            
            await message.answer(welcome_text, reply_markup=get_junior_manager_main_keyboard(lang), parse_mode='HTML')
            
        except Exception as e:
            print(f"Error in show_main_menu: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    return router