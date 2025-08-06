"""
Manager Staff Application Creation Handler - Simplified Implementation

This module handles staff application creation for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from datetime import datetime
from keyboards.manager_buttons import get_staff_application_keyboard
from states.manager_states import StaffApplicationStates

def get_manager_staff_application_creation_router():
    router = Router()

    @router.message(F.text.in_(["📝 Xodim arizi", "📝 Заявка сотрудника"]))
    async def staff_application_menu(message: Message, state: FSMContext):
        """Show staff application menu"""
        try:
            app_text = (
                "📝 **Xodim arizi yaratish**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_staff_application_keyboard()
            await message.answer(
                text=app_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "create_staff_application")
    async def create_staff_application(callback: CallbackQuery, state: FSMContext):
        """Start creating staff application"""
        try:
            await callback.answer()
            
            text = (
                "📝 **Xodim arizi yaratish**\n\n"
                "Yangi xodim arizasini yaratish funksiyasi.\n\n"
                "📋 Ariza turlari:\n"
                "• Ishga qabul qilish\n"
                "• Lavozim o'zgartirish\n"
                "• Ishdan bo'shatish\n"
                "• Qo'shimcha ma'lumot\n\n"
                "👥 Xodim turlari:\n"
                "• Texnik\n"
                "• Menejer\n"
                "• Call center\n"
                "• Warehouse"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_staff_app_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "view_staff_applications")
    async def view_staff_applications(callback: CallbackQuery, state: FSMContext):
        """View staff applications"""
        try:
            await callback.answer()
            
            # Mock staff applications data
            applications = [
                {
                    'id': 'STAFF001',
                    'employee_name': 'Ahmad Karimov',
                    'type': 'Ishga qabul qilish',
                    'position': 'Texnik',
                    'status': 'Ko\'rib chiqilmoqda',
                    'created': '2024-01-15 10:30',
                    'department': 'Texnik xizmat'
                },
                {
                    'id': 'STAFF002',
                    'employee_name': 'Malika Yusupova',
                    'type': 'Lavozim o\'zgartirish',
                    'position': 'Menejer',
                    'status': 'Tasdiqlangan',
                    'created': '2024-01-15 11:45',
                    'department': 'Boshqaruv'
                },
                {
                    'id': 'STAFF003',
                    'employee_name': 'Bekzod Toirov',
                    'type': 'Ishdan bo\'shatish',
                    'position': 'Call center',
                    'status': 'Bajarilgan',
                    'created': '2024-01-15 09:15',
                    'department': 'Mijozlar xizmati'
                }
            ]
            
            text = "📝 **Xodim arizalari**\n\n"
            for app in applications:
                status_emoji = {
                    'Ko\'rib chiqilmoqda': '🔄',
                    'Tasdiqlangan': '✅',
                    'Bajarilgan': '✅',
                    'Bekor qilingan': '❌'
                }.get(app['status'], '⚪')
                
                text += (
                    f"{status_emoji} **{app['id']}** - {app['employee_name']}\n"
                    f"📋 Tur: {app['type']}\n"
                    f"👤 Lavozim: {app['position']}\n"
                    f"🏢 Bo'lim: {app['department']}\n"
                    f"📊 Status: {app['status']}\n"
                    f"📅 Sana: {app['created']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_staff_app_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "process_staff_application")
    async def process_staff_application(callback: CallbackQuery, state: FSMContext):
        """Process staff application"""
        try:
            await callback.answer()
            
            text = (
                "📝 **Xodim arizasini qayta ishlash**\n\n"
                "Xodim arizalarini qayta ishlash funksiyasi.\n\n"
                "📋 Ko'rib chiqilayotgan arizalar:\n"
                "• STAFF001 - Ahmad Karimov (Ishga qabul qilish)\n"
                "• STAFF002 - Malika Yusupova (Lavozim o'zgartirish)\n\n"
                "👨‍💼 Mas'ul shaxslar:\n"
                "• Aziz Karimov (HR menejer)\n"
                "• Malika Yusupova (Bosh menejer)\n"
                "• Bekzod Toirov (Kichik menejer)"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_staff_app_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_staff_app_menu")
    async def back_to_staff_application_menu(callback: CallbackQuery, state: FSMContext):
        """Back to staff application menu"""
        try:
            await callback.answer()
            
            app_text = (
                "📝 **Xodim arizi yaratish**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_staff_application_keyboard()
            await callback.message.edit_text(
                text=app_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
