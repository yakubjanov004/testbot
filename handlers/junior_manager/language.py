"""
Junior Manager Language Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun til o'zgartirish funksionalligini o'z ichiga oladi.
"""

from aiogram import Router, F
from aiogram.types import Message

# Mock functions to replace utils and database imports
async def set_user_language(user_id: int, language: str):
    """Mock set user language"""
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
    """Get router for junior manager language handlers"""
    router = Router()

    @router.message(F.text.in_(["🌐 Tilni o'zgartirish"]))
    async def change_language(message: Message):
        """Handle language change request"""
        user_id = message.from_user.id
        
        try:
            # Get current language
            lang = await get_user_lang(user_id)
            
            # Set new language
            if lang == "uz":
                await set_user_language(user_id, "ru")
                response_text = "Til rus tiliga o'zgartirildi."
            else:
                await set_user_language(user_id, "uz")
                response_text = "Til o'zbek tiliga o'zgartirildi."
            
            # Send response
            await message.answer(response_text)
            
        except Exception as e:
            print(f"Error in change_language: {e}")
            
            # Send error message
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router 
