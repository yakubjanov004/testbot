"""
Junior Manager Main Menu Handler - Simplified Implementation

Bu modul junior manager uchun asosiy menyu funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.junior_manager_states import JuniorManagerMainMenuStates

def get_junior_manager_main_menu_router():
    """Get router for junior manager main menu handlers - Simplified Implementation"""
    router = Router()

    @router.message(F.text.in_(["/start", "🏠 Asosiy menyu"]))
    async def show_main_menu(message: Message, state: FSMContext):
        """Show main menu for junior manager"""
        try:
            await state.set_state(JuniorManagerMainMenuStates.main_menu)
            
            welcome_text = """
🏠 <b>Junior Manager Panel</b>

👋 Xush kelibsiz, Junior Manager!

📋 <b>Sizning vazifalaringiz:</b>
• 📋 Arizalarni ko'rish va boshqarish
• 👥 Xodimlarni boshqarish
• 📊 Statistikalarni ko'rish
• 📞 Mijozlar bilan bog'lanish
• ⚙️ Sozlamalarni boshqarish
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📋 Arizalar", callback_data="junior_manager_applications")],
                [InlineKeyboardButton(text="👥 Xodimlar", callback_data="junior_manager_staff")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="junior_manager_stats")],
                [InlineKeyboardButton(text="📞 Mijozlar", callback_data="junior_manager_clients")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="junior_manager_settings")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="junior_manager_language")]
            ])
            
            await message.answer(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "junior_manager_main_menu")
    async def junior_manager_main_menu_callback(callback: CallbackQuery, state: FSMContext):
        """Return to junior manager main menu"""
        try:
            await state.set_state(JuniorManagerMainMenuStates.main_menu)
            
            welcome_text = """
🏠 <b>Junior Manager Panel</b>

👤 Junior Manager
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📋 Arizalar", callback_data="junior_manager_applications")],
                [InlineKeyboardButton(text="👥 Xodimlar", callback_data="junior_manager_staff")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="junior_manager_stats")],
                [InlineKeyboardButton(text="📞 Mijozlar", callback_data="junior_manager_clients")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="junior_manager_settings")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="junior_manager_language")]
            ])
            
            await callback.message.edit_text(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "junior_manager_back")
    async def junior_manager_back_handler(callback: CallbackQuery, state: FSMContext):
        """Back to junior manager main menu"""
        try:
            await junior_manager_main_menu_callback(callback, state)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router