"""
Controller Main Menu Handler - Simplified Implementation

This module handles the main menu for controllers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.controller_states import MainMenuStates

def get_controller_main_menu_router():
    """Controller main menu router - Simplified Implementation"""
    router = Router()

    @router.message(F.text.in_(["/start", "🏠 Asosiy menyu", "🏠 Главное меню"]))
    async def main_menu_handler(message: Message, state: FSMContext):
        """Controller main menu handler"""
        try:
            await state.set_state(MainMenuStates.main_menu)
            
            welcome_text = """
🎛️ <b>Controller Panel</b>

👋 Xush kelibsiz, Controller xodimi!

📋 <b>Sizning vazifalaringiz:</b>
• 📋 Arizalarni ko'rish va boshqarish
• 🔍 Arizalarni tekshirish va tasdiqlash
• 📊 Statistikalarni ko'rish
• ⚙️ Sozlamalarni boshqarish
• 📞 Mijozlar bilan bog'lanish
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📋 Arizalar", callback_data="controller_applications")],
                [InlineKeyboardButton(text="🔍 Tekshirish", callback_data="controller_review")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="controller_stats")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="controller_settings")],
                [InlineKeyboardButton(text="📞 Mijozlar", callback_data="controller_clients")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="controller_language")]
            ])
            
            await message.answer(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Back to main menu"""
        try:
            await state.set_state(MainMenuStates.main_menu)
            
            welcome_text = """
🎛️ <b>Controller Panel</b>

👤 Controller xodimi
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📋 Arizalar", callback_data="controller_applications")],
                [InlineKeyboardButton(text="🔍 Tekshirish", callback_data="controller_review")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="controller_stats")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="controller_settings")],
                [InlineKeyboardButton(text="📞 Mijozlar", callback_data="controller_clients")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="controller_language")]
            ])
            
            await callback.message.edit_text(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "controller_main_menu")
    async def controller_main_menu_callback(callback: CallbackQuery, state: FSMContext):
        """Return to controller main menu"""
        try:
            await state.set_state(MainMenuStates.main_menu)
            
            welcome_text = """
🎛️ <b>Controller Panel</b>

👤 Controller xodimi
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📋 Arizalar", callback_data="controller_applications")],
                [InlineKeyboardButton(text="🔍 Tekshirish", callback_data="controller_review")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="controller_stats")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="controller_settings")],
                [InlineKeyboardButton(text="📞 Mijozlar", callback_data="controller_clients")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="controller_language")]
            ])
            
            await callback.message.edit_text(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
