"""
Start Handler - Complete Implementation

This module handles the /start command and shows appropriate menus
based on user role.
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from loader import get_user_role
from utils.role_system import show_role_menu
from utils.logger import log_user_activity, log_error, log_handler_start, log_handler_end

# Logger sozlash
logger = logging.getLogger(__name__)

def get_start_router():
    """Get start router with all handlers"""
    router = Router()
    
    @router.message(F.text == "/start")
    async def start_command(message: Message, state: FSMContext):
        """Handle /start command"""
        user_id = message.from_user.id
        user_name = message.from_user.full_name
        handler_name = "start_command"
        
        try:
            # Handler boshlanishini log qilish
            log_handler_start(handler_name, user_id, user_name)
            log_user_activity(user_id, user_name, "Started bot", "Command: /start")
            
            user_role = get_user_role(user_id)
            
            # Clear any existing state
            await state.clear()
            
            # Show welcome message
            welcome_text = (
                f"👋 Xush kelibsiz, {message.from_user.first_name}!\n\n"
                f"🤖 Alfa Connect botiga xush kelibsiz!\n"
                f"👤 Sizning rolingiz: {user_role.upper()}\n\n"
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
            
            # Handler tugashini log qilish
            log_handler_end(handler_name, user_id, user_name, success=True)
            
        except Exception as e:
            log_error(user_id, user_name, e, context="start_command")
            log_handler_end(handler_name, user_id, user_name, success=False)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    
    # @router.message(F.text.in_(["🏠 Bosh sahifa", "🏠 Главная", "🏠 Home"]))
    # async def home_command(message: Message, state: FSMContext):
    #     """Handle home command"""
    #     try:
    #         user_id = message.from_user.id
    #         user_role = get_user_role(user_id)
            
    #         # Clear any existing state
    #         await state.clear()
            
    #         # Show appropriate menu based on role
    #         await show_role_menu(message, user_role)
            
    #     except Exception as e:
    #         await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    
    # @router.message(F.text.in_(["ℹ️ Yordam", "ℹ️ Помощь", "ℹ️ Help"]))
    # async def help_command(message: Message, state: FSMContext):
    #     """Handle help command"""
    #     try:
    #         help_text = (
    #             "ℹ️ **Yordam**\n\n"
    #             "🤖 Bu bot Alfa Connect kompaniyasi uchun yaratilgan.\n\n"
    #             "📋 **Mavjud funksiyalar:**\n"
    #             "• Ariza yaratish va boshqarish\n"
    #             "• Xodimlar faoliyatini kuzatish\n"
    #             "• Hisobotlar va statistikalar\n"
    #             "• Ombor boshqaruvi\n"
    #             "• Call Center funksiyalari\n\n"
    #             "🔧 **Texnik yordam:**\n"
    #             "Agar muammolar bo'lsa, administrator bilan bog'laning.\n\n"
    #             "📞 **Aloqa:**\n"
    #             "Telegram: @admin_username"
    #         )
            
    #         await message.answer(help_text, parse_mode='Markdown')
            
    #     except Exception as e:
    #         await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    
    # @router.message(F.text.in_(["👤 Profil", "👤 Профиль", "👤 Profile"]))
    # async def profile_command(message: Message, state: FSMContext):
    #     """Handle profile command"""
    #     try:
    #         user_id = message.from_user.id
    #         user_role = get_user_role(user_id)
            
    #         profile_text = (
    #             f"👤 **Profil ma'lumotlari**\n\n"
    #             f"🆔 **ID:** {user_id}\n"
    #             f"👤 **Ism:** {message.from_user.first_name}\n"
    #             f"📝 **Familiya:** {message.from_user.last_name or 'Kiritilmagan'}\n"
    #             f"👤 **Username:** @{message.from_user.username or 'Kiritilmagan'}\n"
    #             f"🎭 **Rol:** {user_role.upper()}\n\n"
    #             f"📅 **Ro'yxatdan o'tgan:** {message.date.strftime('%d.%m.%Y %H:%M')}\n"
    #             f"🌐 **Til:** O'zbekcha"
    #         )
            
    #         await message.answer(profile_text, parse_mode='Markdown')
            
    #     except Exception as e:
    #         await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    
    return router 