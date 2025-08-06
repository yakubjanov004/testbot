"""
Junior Manager Main Menu Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun asosiy menyu funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.junior_manager_buttons import get_junior_manager_main_keyboard

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
    """Get router for junior manager main menu handlers"""
    router = Router()

    @router.message(F.text.in_(["/start", "🏠 Asosiy menyu"]))
    async def show_main_menu(message: Message, state: FSMContext):
        """Show main menu for junior manager"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await message.answer(
                    "Sizda ruxsat yo'q.",
                    message.from_user.id
                )
                return

            lang = user.get('language', 'uz')
            
            # Build main menu text
            text = f"""🏠 **Asosiy menyu**

            👤 **Foydalanuvchi:** {user.get('full_name', 'N/A')}
            📱 **Telefon:** {user.get('phone_number', 'N/A')}
            🎯 **Rol:** Kichik menejer

            Quyidagi bo'limlardan birini tanlang:"""
            
            # Create keyboard
            keyboard = get_junior_manager_main_keyboard(lang)
            
            # Send message
            await message.answer(
                text,
                message.from_user.id,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in show_main_menu: {e}")
            await message.answer(
                "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
                message.from_user.id
            )

    

    return router