from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.technician_states import TechnicianMainMenuStates

def get_technician_main_menu_router():
    """Technician main menu router - Simplified Implementation"""
    router = Router()

    @router.message(F.text.in_(["🔧 Technician", "🔧 Texnik", "/start"]))
    async def technician_start(message: Message, state: FSMContext):
        """Technician start handler"""
        try:
            await state.set_state(TechnicianMainMenuStates.main_menu)
            
            welcome_text = """
🔧 <b>Technician Panel</b>

👋 Xush kelibsiz, Texnik xodimi!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Controllerdan kelgan zayavkalarni qabul qilish
• 🔍 Manzilga borib diagnostika qo'yish
• 📦 Ombor yordami kerakligini hal qilish
• 🛠️ Muammolarni hal qilish va ishlarni bajarish
• ✅ Zayavkalarni yakunlash va mijozga xabar berish
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📥 Inbox", callback_data="tech_inbox")],
                [InlineKeyboardButton(text="📋 Vazifalarim", callback_data="tech_tasks")],
                [InlineKeyboardButton(text="📊 Hisobotlar", callback_data="tech_reports")],
                [InlineKeyboardButton(text="🆘 Yordam", callback_data="tech_help")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="tech_language")]
            ])
            
            await message.answer(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "tech_main_menu")
    async def tech_back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Back to main menu handler"""
        try:
            await state.set_state(TechnicianMainMenuStates.main_menu)
            
            welcome_text = """
🔧 <b>Technician Panel</b>

👤 Texnik xodimi
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📥 Inbox", callback_data="tech_inbox")],
                [InlineKeyboardButton(text="📋 Vazifalarim", callback_data="tech_tasks")],
                [InlineKeyboardButton(text="📊 Hisobotlar", callback_data="tech_reports")],
                [InlineKeyboardButton(text="🆘 Yordam", callback_data="tech_help")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="tech_language")]
            ])
            
            await callback.message.edit_text(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_back")
    async def tech_back_handler(callback: CallbackQuery, state: FSMContext):
        """Back handler"""
        try:
            await tech_back_to_main_menu(callback, state)
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "🌐 Tilni o'zgartirish")
    async def change_language_handler(message: Message, state: FSMContext):
        """Change language handler"""
        try:
            text = "🌐 Tilni tanlang:"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="tech_lang_uz")],
                [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="tech_lang_ru")],
                [InlineKeyboardButton(text="🇬🇧 English", callback_data="tech_lang_en")]
            ])
            
            await message.answer(text, reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("tech_lang_"))
    async def set_language_callback(callback: CallbackQuery, state: FSMContext):
        """Set language callback"""
        try:
            new_lang = callback.data.replace("tech_lang_", "")
            
            text = "✅ Til muvaffaqiyatli o'zgartirildi!"
            await callback.answer(text, show_alert=True)
            
            await tech_back_to_main_menu(callback, state)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "📋 Vazifalarim")
    async def my_tasks_handler(message: Message, state: FSMContext):
        """My tasks handler"""
        try:
            text = """
📋 <b>Vazifalarim</b>

🔧 Texnik xizmat arizalari
📥 Inbox - tayinlangan arizalar
📊 Hisobotlar - ish natijalari
🆘 Yordam - qo'llab-quvvatlash

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📥 Inbox", callback_data="tech_inbox")],
                [InlineKeyboardButton(text="📊 Hisobotlar", callback_data="tech_reports")],
                [InlineKeyboardButton(text="🆘 Yordam", callback_data="tech_help")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_main_menu")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "📊 Hisobotlar")
    async def reports_handler(message: Message, state: FSMContext):
        """Reports handler"""
        try:
            text = """
📊 <b>Hisobotlar</b>

📈 Kunlik hisobot
📊 Haftalik hisobot
📋 Oylik hisobot
📋 Ish natijalari

Kerakli hisobotni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📈 Kunlik hisobot", callback_data="tech_daily_report")],
                [InlineKeyboardButton(text="📊 Haftalik hisobot", callback_data="tech_weekly_report")],
                [InlineKeyboardButton(text="📋 Oylik hisobot", callback_data="tech_monthly_report")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_main_menu")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "🆘 Yordam")
    async def help_handler(message: Message, state: FSMContext):
        """Help handler"""
        try:
            text = """
🆘 <b>Yordam</b>

📞 Manager bilan bog'lanish
🔧 Texnik yordam
📦 Ombor bilan bog'lanish
🚨 Shoshilinch holatlar

Kerakli yordam turini tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📞 Manager bilan bog'lanish", callback_data="tech_contact_manager")],
                [InlineKeyboardButton(text="🔧 Texnik yordam", callback_data="tech_technical_help")],
                [InlineKeyboardButton(text="📦 Ombor bilan bog'lanish", callback_data="tech_warehouse_help")],
                [InlineKeyboardButton(text="🚨 Shoshilinch holatlar", callback_data="tech_emergency_help")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_main_menu")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "📥 Inbox")
    async def inbox_handler(message: Message, state: FSMContext):
        """Inbox handler"""
        try:
            text = """
📥 <b>Inbox</b>

📋 Tayinlangan arizalar
📊 Holatlar
📈 Statistika

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📋 Tayinlangan arizalar", callback_data="tech_assigned_applications")],
                [InlineKeyboardButton(text="📊 Holatlar", callback_data="tech_status_overview")],
                [InlineKeyboardButton(text="📈 Statistika", callback_data="tech_inbox_stats")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_main_menu")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "🔧 Texnik xizmat")
    async def technical_service_handler(message: Message, state: FSMContext):
        """Technical service handler"""
        try:
            text = """
🔧 <b>Texnik xizmat</b>

🛠️ Muammolarni hal qilish
🔍 Diagnostika
📦 Materiallar
✅ Yakunlash

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🛠️ Muammolarni hal qilish", callback_data="tech_solve_issues")],
                [InlineKeyboardButton(text="🔍 Diagnostika", callback_data="tech_diagnostics")],
                [InlineKeyboardButton(text="📦 Materiallar", callback_data="tech_materials")],
                [InlineKeyboardButton(text="✅ Yakunlash", callback_data="tech_completion")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_main_menu")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "📞 Manager bilan bog'lanish")
    async def contact_manager_handler(message: Message, state: FSMContext):
        """Contact manager handler"""
        try:
            text = """
📞 <b>Manager bilan bog'lanish</b>

👤 Manager: +998901234567
📧 Email: manager@example.com
💬 Telegram: @manager_bot

Xabar yuborish uchun tugmani bosing:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📞 Xabar yuborish", callback_data="tech_send_message_manager")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_main_menu")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "🔧 Texnik yordam")
    async def technical_help_handler(message: Message, state: FSMContext):
        """Technical help handler"""
        try:
            text = """
🔧 <b>Texnik yordam</b>

📞 Texnik yordam: +998901234568
📧 Email: support@example.com
💬 Telegram: @support_bot

Muammo bo'lsa bog'laning:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📞 Bog'lanish", callback_data="tech_contact_support")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_main_menu")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "📦 Ombor bilan bog'lanish")
    async def contact_warehouse_handler(message: Message, state: FSMContext):
        """Contact warehouse handler"""
        try:
            text = """
📦 <b>Ombor bilan bog'lanish</b>

👤 Ombor: +998901234569
📧 Email: warehouse@example.com
💬 Telegram: @warehouse_bot

Material kerak bo'lsa bog'laning:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 Material so'rash", callback_data="tech_request_materials")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_main_menu")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "🚨 Shoshilinch holatlar")
    async def emergency_handler(message: Message, state: FSMContext):
        """Emergency handler"""
        try:
            text = """
🚨 <b>Shoshilinch holatlar</b>

📞 Shoshilinch: +998901234570
🚑 Ambulansiya: 103
🚔 Politsiya: 102
🔥 O't o'chirish: 101

Shoshilinch holatda darhol bog'laning!
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚨 Shoshilinch chaqirish", callback_data="tech_emergency_call")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_main_menu")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    return router
