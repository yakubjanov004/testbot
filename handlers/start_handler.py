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

# DB optional import and flag
from os import getenv
DB_ENABLED = getenv('DB_ENABLED', '0').lower() in {'1','true','yes','on'}
if DB_ENABLED:
        from utils.db import upsert_user


def get_start_router():
        """Get start router with all handlers"""
        router = Router()
        
        @router.message(F.text == "/start")
        async def start_command(message: Message, state: FSMContext):
                """Handle /start command"""
                try:
                        user_role = get_user_role(message.from_user.id)

                        # Persist user on first start if DB is enabled
                        is_created = False
                        if DB_ENABLED:
                                try:
                                        is_created, saved = await upsert_user(
                                                message.from_user.id,
                                                {
                                                        "telegram_id": message.from_user.id,
                                                        "username": message.from_user.username,
                                                        "first_name": message.from_user.first_name,
                                                        "last_name": message.from_user.last_name,
                                                        "language": message.from_user.language_code or "uz",
                                                        "role": user_role,
                                                        "is_bot": message.from_user.is_bot,
                                                },
                                        )
                                except Exception:
                                        is_created = False
                        
                        # Clear any existing state
                        await state.clear()
                        
                        # Show welcome message
                        created_note = "🆕 Ro'yxatdan o'tdingiz." if is_created else ""
                        welcome_text = (
                                f"👋 Xush kelibsiz, {message.from_user.first_name}!\n\n"
                                f"🤖 Alfa Connect botiga xush kelibsiz!\n"
                                f"👤 Sizning rolingiz: {user_role.upper()}\n"
                                f"{created_note}\n\n"
                                f"Quyidagi menyulardan birini tanlang:"
                        )
                        
                        await message.answer(welcome_text)
                        
                        # Show appropriate menu based on role
                        if user_role == 'client':
                                from keyboards.client_buttons import get_main_menu_keyboard
                                keyboard = get_main_menu_keyboard('uz')
                                await message.answer("Quyidagi menyudan kerakli bo'limni tanlang.", reply_markup=keyboard)
                        else:
                                await show_role_menu(message, user_role)
                        
                except Exception as e:
                        #await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
                        pass
        
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
                                from keyboards.client_buttons import get_main_menu_keyboard
                                keyboard = get_main_menu_keyboard('uz')
                                await callback.message.edit_text(
                                        "Quyidagi menyudan kerakli bo'limni tanlang.",
                                        reply_markup=keyboard
                                )
                        else:
                                await show_role_menu(callback.message, user_role)
                        
                except Exception as e:
                        #await callback.message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
                        pass
        
        return router 