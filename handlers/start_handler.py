"""
Start Handler - Simplified Implementation

This module handles the /start command and shows appropriate menus
based on user role.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from loader import get_user_role
from utils.role_system import show_role_menu
from keyboards.client_buttons import get_main_menu_keyboard, get_language_keyboard, get_contact_keyboard
from states.client_states import RegistrationStates
from utils.mock_db import create_or_get_user, is_registered, set_language, set_phone, set_full_name, get_user

def get_start_router():
    """Get start router with all handlers"""
    router = Router()
    
    @router.message(F.text == "/start")
    async def start_command(message: Message, state: FSMContext):
        """Handle /start command"""
        try:
            user_role = get_user_role(message.from_user.id)

            # Clear any existing state
            await state.clear()

            if user_role == 'client':
                # Initialize user in mock storage
                user = create_or_get_user(message.from_user.id)

                if not is_registered(message.from_user.id):
                    # Ask language selection first
                    await state.set_state(RegistrationStates.choosing_language)
                    await message.answer(
                        "Tilni tanlang / Выберите язык:",
                        reply_markup=get_language_keyboard(role="client")
                    )
                    return

                # Already registered -> show main menu in saved language
                lang = user.get('language', 'uz')
                keyboard = get_main_menu_keyboard(lang)
                await message.answer(
                    ("Quyidagi menyudan kerakli bo'limni tanlang." if lang == 'uz' else "Выберите нужный раздел из меню ниже."),
                    reply_markup=keyboard
                )
            else:
                # Non-client roles keep previous behavior
                await message.answer(
                    (
                        f"👋 Xush kelibsiz, {message.from_user.first_name}!\n\n"
                        f"🤖 Alfa Connect botiga xush kelibsiz!\n"
                        f"👤 Sizning rolingiz: {user_role.upper()}\n\n"
                        f"Quyidagi menyulardan birini tanlang:"
                    )
                )
                await show_role_menu(message, user_role)
        except Exception as e:
            pass

    @router.callback_query(F.data.startswith("client_lang_"))
    async def handle_registration_language(callback: CallbackQuery, state: FSMContext):
        """Handle language selection during registration"""
        try:
            await callback.answer()
            selected_lang = callback.data.split("_")[-1]
            set_language(callback.from_user.id, selected_lang)

            # Ask for contact
            await state.set_state(RegistrationStates.waiting_contact)
            await callback.message.edit_text(
                ("Iltimos, telefon raqamingizni yuboring" if selected_lang == 'uz' else "Пожалуйста, отправьте ваш номер телефона"),
            )
            await callback.message.answer(
                ("Quyidagi tugma orqali kontakt ulashing" if selected_lang == 'uz' else "Поделитесь контактом через кнопку ниже"),
                reply_markup=get_contact_keyboard(selected_lang)
            )
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(RegistrationStates.waiting_contact, F.contact)
    async def handle_registration_contact(message: Message, state: FSMContext):
        """Save contact during registration and ask for name"""
        try:
            user = get_user(message.from_user.id) or create_or_get_user(message.from_user.id)
            lang = user.get('language', 'uz')
            phone = message.contact.phone_number if message.contact else None
            if phone:
                set_phone(message.from_user.id, phone)
            await state.set_state(RegistrationStates.waiting_name)
            await message.answer(
                ("Iltimos, to'liq ismingizni kiriting" if lang == 'uz' else "Пожалуйста, введите ваше полное имя"),
            )
        except Exception:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(RegistrationStates.waiting_name)
    async def handle_registration_name(message: Message, state: FSMContext):
        """Save full name and show main menu"""
        try:
            set_full_name(message.from_user.id, message.text.strip())
            user = get_user(message.from_user.id)
            lang = user.get('language', 'uz')
            await state.clear()
            await message.answer(
                ("Ro'yxatdan o'tish yakunlandi!" if lang == 'uz' else "Регистрация завершена!"),
                reply_markup=get_main_menu_keyboard(lang)
            )
        except Exception:
            await message.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to main menu button"""
        try:
            await callback.answer()
            
            user_role = get_user_role(callback.from_user.id)
            
            # Clear any existing state
            await state.clear()
            
            # Show appropriate menu based on role
            if user_role == 'client':
                from utils.mock_db import get_user as mock_get_user
                user = mock_get_user(callback.from_user.id)
                lang = user.get('language', 'uz') if user else 'uz'
                keyboard = get_main_menu_keyboard(lang)
                await callback.message.edit_text(
                    ("Quyidagi menyudan kerakli bo'limni tanlang." if lang == 'uz' else "Выберите нужный раздел из меню ниже."),
                    reply_markup=keyboard
                )
            else:
                await show_role_menu(callback.message, user_role)
            
        except Exception as e:
            #await callback.message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            pass
    
    return router 