"""
Call Center Supervisor Main Menu Handler - Simplified Implementation

This module handles the main menu for call center supervisors.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.call_center_supervisor_states import MainMenuStates

def get_call_center_supervisor_main_menu_router():
    """Call center supervisor main menu router - Simplified Implementation"""
    router = Router()

    @router.message(F.text.in_(["/start", "🏠 Asosiy menyu", "🏠 Главное меню"]))
    async def main_menu_handler(message: Message, state: FSMContext):
        """Call center supervisor main menu handler"""
        try:
            await state.set_state(MainMenuStates.main_menu)
            
            welcome_text = """
👨‍💼 <b>Call Center Supervisor Panel</b>

👋 Xush kelibsiz, Call Center Supervisor!

📋 <b>Sizning vazifalaringiz:</b>
• 👥 Xodimlarni boshqarish
• 📊 Statistikalarni ko'rish
• 📞 Qo'ng'iroqlarni nazorat qilish
• 📋 Buyurtmalarni ko'rish
• ⚙️ Sozlamalarni boshqarish
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👥 Xodimlar", callback_data="supervisor_staff")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="supervisor_stats")],
                [InlineKeyboardButton(text="📞 Qo'ng'iroqlar", callback_data="supervisor_calls")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="supervisor_orders")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="supervisor_settings")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="supervisor_language")]
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
👨‍💼 <b>Call Center Supervisor Panel</b>

👤 Call Center Supervisor
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👥 Xodimlar", callback_data="supervisor_staff")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="supervisor_stats")],
                [InlineKeyboardButton(text="📞 Qo'ng'iroqlar", callback_data="supervisor_calls")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="supervisor_orders")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="supervisor_settings")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="supervisor_language")]
            ])
            
            await callback.message.edit_text(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "supervisor_main_menu")
    async def supervisor_main_menu_callback(callback: CallbackQuery, state: FSMContext):
        """Return to supervisor main menu"""
        try:
            await state.set_state(MainMenuStates.main_menu)
            
            welcome_text = """
👨‍💼 <b>Call Center Supervisor Panel</b>

👤 Call Center Supervisor
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👥 Xodimlar", callback_data="supervisor_staff")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="supervisor_stats")],
                [InlineKeyboardButton(text="📞 Qo'ng'iroqlar", callback_data="supervisor_calls")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="supervisor_orders")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="supervisor_settings")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="supervisor_language")]
            ])
            
            await callback.message.edit_text(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router