"""
Client Contact Handler - Simplified Implementation

This module handles client contact functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.client_states import ContactStates
from filters.role_filter import RoleFilter
from keyboards.client_buttons import get_back_keyboard, get_contact_operator_keyboard, get_main_menu_keyboard
from utils.mock_db import get_user as mock_get_user

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
    """Mock get user language"""
    return 'uz'

async def get_user_role(user_id: int) -> str:
    """Mock get user role"""
    return 'client'

def get_client_contact_router():
    """Get client contact router with role filtering"""
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📞 Operator bilan bog'lanish", "📞 Связаться с оператором"]))
    async def contact_handler(message: Message, state: FSMContext):
        """Open operator contact submenu (reply keyboard)"""
        try:
            user = mock_get_user(message.from_user.id) or await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz') if user else 'uz'
            text = ("Bog'lanish turini tanlang:" if lang == 'uz' else "Выберите способ связи:")
            await message.answer(text, reply_markup=get_contact_operator_keyboard(lang))
            await state.set_state(ContactStates.viewing_contact)
        except Exception:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(ContactStates.viewing_contact, F.text.startswith("📞 "))
    async def handle_phone_choice(message: Message, state: FSMContext):
        try:
            user = mock_get_user(message.from_user.id) or await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz') if user else 'uz'
            phone = message.text.replace("📞 ", "").strip()
            confirm = (f"Qo'ng'iroq qilish uchun: {phone}" if lang == 'uz' else f"Позвонить по номеру: {phone}")
            await message.answer(confirm)
        except Exception:
            await message.answer("❌ Xatolik yuz berdi.")

    @router.message(ContactStates.viewing_contact, F.text.in_(["◀️ Orqaga", "◀️ Назад"]))
    async def contact_back_to_main(message: Message, state: FSMContext):
        try:
            user = mock_get_user(message.from_user.id) or await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz') if user else 'uz'
            await state.clear()
            await message.answer(
                ("Quyidagi menyudan kerakli bo'limni tanlang." if lang == 'uz' else "Выберите нужный раздел из меню ниже."),
                reply_markup=get_main_menu_keyboard(lang)
            )
        except Exception:
            await message.answer("❌ Xatolik yuz berdi.")

    return router
