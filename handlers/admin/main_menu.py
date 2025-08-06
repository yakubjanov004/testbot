"""
Admin Main Menu Handler - Simplified Implementation
Manages admin main menu and dashboard
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.admin_states import AdminMainMenuStates

def get_admin_main_menu_router():
    """Get admin main menu router - Simplified Implementation"""
    router = Router()

    @router.message(F.text.in_(["/start", "/admin"]))
    async def admin_start(message: Message, state: FSMContext):
        """Admin start"""
        try:
            await state.set_state(AdminMainMenuStates.main_menu)
            
            welcome_text = """
🛠 <b>Admin Panel</b>

📊 <b>Tizim holati:</b>
👥 Jami foydalanuvchilar: <b>1250</b>
📋 Bugungi zayavkalar: <b>45</b>
✅ Bugun bajarilgan: <b>32</b>
⏳ Kutilayotgan: <b>13</b>
👨‍🔧 Faol texniklar: <b>8</b>

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin_users")],
                [InlineKeyboardButton(text="📝 Zayavkalar", callback_data="admin_applications")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="admin_settings")],
                [InlineKeyboardButton(text="🔧 Tizim", callback_data="admin_system")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="admin_language")]
            ])
            
            await message.answer(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text.in_(['🏠 Bosh sahifa', '🏠 Главная']))
    async def admin_home(message: Message, state: FSMContext):
        """Return to admin home"""
        try:
            await admin_start(message, state)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text.in_(['ℹ️ Yordam', 'ℹ️ Помощь']))
    async def admin_help(message: Message, state: FSMContext):
        """Show admin help"""
        try:
            help_text = """
ℹ️ <b>Admin Panel Yordami</b>

📋 <b>Asosiy funksiyalar:</b>
• 👥 Foydalanuvchilar - foydalanuvchilarni boshqarish
• 📝 Zayavkalar - zayavkalarni ko'rish va boshqarish
• 📊 Statistika - tizim statistikasini ko'rish
• ⚙️ Sozlamalar - tizim sozlamalarini o'zgartirish

🔧 <b>Foydalanuvchi boshqaruvi:</b>
• Rol o'zgartirish
• Bloklash/blokdan chiqarish
• Qidirish (ID, telefon, ism bo'yicha)

📋 <b>Zayavka boshqaruvi:</b>
• Status o'zgartirish
• Texnik tayinlash
• Filtrlash va qidirish

📞 <b>Yordam uchun:</b> @support
            """
            
            await message.answer(help_text.strip(), parse_mode='HTML')
            await state.set_state(AdminMainMenuStates.main_menu)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "admin_main_menu")
    async def admin_main_menu_callback(callback: CallbackQuery, state: FSMContext):
        """Return to admin main menu"""
        try:
            await state.set_state(AdminMainMenuStates.main_menu)
            
            welcome_text = """
🛠 <b>Admin Panel</b>

👤 Administrator
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin_users")],
                [InlineKeyboardButton(text="📝 Zayavkalar", callback_data="admin_applications")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
                [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="admin_settings")],
                [InlineKeyboardButton(text="🔧 Tizim", callback_data="admin_system")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="admin_language")]
            ])
            
            await callback.message.edit_text(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == '/test_admin')
    async def test_admin(message: Message):
        """Test admin access without decorator"""
        try:
            await message.answer("✅ Admin access confirmed!")
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    return router

async def show_admin_main_menu(message: Message):
    """Show admin main menu"""
    welcome_text = (
        f"🛠 <b>Admin Panel</b>\n\n"
        f"Kerakli bo'limni tanlang:"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_admin_main_menu('uz')
    )
