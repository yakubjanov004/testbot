"""
Manager Applications Handler - Simplified Implementation

This module handles application management for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_applications_keyboard
from states.manager_states import ApplicationsStates

def get_manager_applications_router():
    router = Router()

    @router.message(F.text.in_(["📋 Ariyalar", "📋 Заявки"]))
    async def applications_menu(message: Message, state: FSMContext):
        """Show applications menu"""
        try:
            apps_text = (
                "📋 **Ariyalar boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_applications_keyboard()
            await message.answer(
                text=apps_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_all_applications")
    async def view_all_applications(callback: CallbackQuery, state: FSMContext):
        """View all applications"""
        try:
            await callback.answer()
            
            # Mock applications data
            applications = [
                {
                    'id': 'APP001',
                    'type': 'Ulanish',
                    'client': 'Ahmad Karimov',
                    'status': 'Yangi',
                    'created': '2024-01-15 10:30',
                    'priority': 'Yuqori'
                },
                {
                    'id': 'APP002',
                    'type': 'Texnik xizmat',
                    'client': 'Malika Yusupova',
                    'status': 'Jarayonda',
                    'created': '2024-01-15 11:45',
                    'priority': 'O\'rta'
                },
                {
                    'id': 'APP003',
                    'type': 'Ulanish',
                    'client': 'Bekzod Toirov',
                    'status': 'Bajarilgan',
                    'created': '2024-01-15 09:15',
                    'priority': 'Past'
                }
            ]
            
            text = "📋 **Barcha ariyalar**\n\n"
            for app in applications:
                status_emoji = {
                    'Yangi': '🆕',
                    'Jarayonda': '🔄',
                    'Bajarilgan': '✅',
                    'Bekor qilingan': '❌'
                }.get(app['status'], '⚪')
                
                priority_emoji = {
                    'Yuqori': '🔴',
                    'O\'rta': '🟡',
                    'Past': '🟢'
                }.get(app['priority'], '⚪')
                
                text += (
                    f"{status_emoji} **{app['id']}** - {app['client']}\n"
                    f"📋 Tur: {app['type']}\n"
                    f"{priority_emoji} Daraja: {app['priority']}\n"
                    f"📅 Sana: {app['created']}\n"
                    f"📊 Holat: {app['status']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_apps_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "process_applications")
    async def process_applications(callback: CallbackQuery, state: FSMContext):
        """Process applications"""
        try:
            await callback.answer()
            
            text = (
                "📋 **Ariyalarni qayta ishlash**\n\n"
                "Ariyalarni qayta ishlash funksiyasi.\n\n"
                "📋 Mavjud ariyalar:\n"
                "• APP001 - Ahmad Karimov (Ulanish) - Yangi\n"
                "• APP002 - Malika Yusupova (Texnik xizmat) - Jarayonda\n\n"
                "👨‍💼 Mavjud menejerlar:\n"
                "• Aziz Karimov (Katta menejer)\n"
                "• Malika Yusupova (Menejer)\n"
                "• Bekzod Toirov (Kichik menejer)"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_apps_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_apps_menu")
    async def back_to_applications_menu(callback: CallbackQuery, state: FSMContext):
        """Back to applications menu"""
        try:
            await callback.answer()
            
            apps_text = (
                "📋 **Ariyalar boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_applications_keyboard()
            await callback.message.edit_text(
                text=apps_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router