from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_contact_keyboard, get_main_menu_keyboard
from states.client_states import StartStates
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
    """Mock user language"""
    return 'uz'

def get_client_start_router():
    router = get_role_router("client")

    async def get_welcome_message(lang: str, user_id: int = None) -> str:
        """Get welcome message in the specified language"""
        try:
            if lang == 'uz':
                message = "Xush kelibsiz! Asosiy menyu quyidagicha:"
            else:
                message = "Xush kelibsiz! Asosiy menyu quyidagicha:"
            
            return message
            
        except Exception as e:
            # Return basic message on error
            return "Xush kelibsiz!"

    @router.message(F.text.in_(["🏠 Bosh sahifa"]))
    async def client_home_handler(message: Message, state: FSMContext):
        """Client home page handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            welcome_text = await get_welcome_message(lang, message.from_user.id)
            
            # Use send_and_track for inline cleanup
            sent_message = await message.answer(
                text=welcome_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.update_data(last_message_id=sent_message.message_id)
            await state.set_state(StartStates.home_page)
            
        except Exception as e:
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    return router