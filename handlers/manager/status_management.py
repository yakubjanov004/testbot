"""
Manager Status Management Handler - Simplified Implementation

This module handles status management for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_status_management_keyboard
from states.manager_states import StatusManagementStates

def get_manager_status_management_router():
    router = Router()

    @router.message(F.text.in_(["📊 Status boshqaruvi", "📊 Управление статусом"]))
    async def status_management_menu(message: Message, state: FSMContext):
        """Show status management menu"""
        try:
            status_text = (
                "📊 **Status boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_status_management_keyboard()
            await message.answer(
                text=status_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_all_statuses")
    async def view_all_statuses(callback: CallbackQuery, state: FSMContext):
        """View all statuses"""
        try:
            await callback.answer()
            
            # Mock status data
            statuses = [
                {
                    'id': 'APP001',
                    'client': 'Ahmad Karimov',
                    'type': 'Ulanish',
                    'status': 'Yangi',
                    'created': '2024-01-15 10:30',
                    'assigned_to': 'Aziz Karimov'
                },
                {
                    'id': 'APP002',
                    'client': 'Malika Yusupova',
                    'type': 'Texnik xizmat',
                    'status': 'Jarayonda',
                    'created': '2024-01-15 11:45',
                    'assigned_to': 'Malika Yusupova'
                },
                {
                    'id': 'APP003',
                    'client': 'Bekzod Toirov',
                    'type': 'Ulanish',
                    'status': 'Bajarilgan',
                    'created': '2024-01-15 09:15',
                    'assigned_to': 'Bekzod Toirov'
                }
            ]
            
            text = "📊 **Barcha statuslar**\n\n"
            for status in statuses:
                status_emoji = {
                    'Yangi': '🆕',
                    'Jarayonda': '🔄',
                    'Bajarilgan': '✅',
                    'Bekor qilingan': '❌'
                }.get(status['status'], '⚪')
                
                text += (
                    f"{status_emoji} **{status['id']}** - {status['client']}\n"
                    f"📋 Tur: {status['type']}\n"
                    f"📊 Status: {status['status']}\n"
                    f"👤 Mas'ul: {status['assigned_to']}\n"
                    f"📅 Sana: {status['created']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_status_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "change_status")
    async def change_status(callback: CallbackQuery, state: FSMContext):
        """Change status"""
        try:
            await callback.answer()
            
            text = (
                "📊 **Status o'zgartirish**\n\n"
                "Ariyalar statusini o'zgartirish funksiyasi.\n\n"
                "📋 Mavjud ariyalar:\n"
                "• APP001 - Ahmad Karimov (Ulanish) - Yangi\n"
                "• APP002 - Malika Yusupova (Texnik xizmat) - Jarayonda\n"
                "• APP003 - Bekzod Toirov (Ulanish) - Bajarilgan\n\n"
                "📊 Status turlari:\n"
                "• Yangi - qabul qilindi\n"
                "• Jarayonda - ishga olingan\n"
                "• Bajarilgan - tugallangan\n"
                "• Bekor qilingan - bekor qilindi"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_status_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "status_report")
    async def status_report(callback: CallbackQuery, state: FSMContext):
        """Show status report"""
        try:
            await callback.answer()
            
            # Mock status report data
            status_report = {
                'total_applications': 45,
                'new': 12,
                'in_progress': 8,
                'completed': 25,
                'cancelled': 0,
                'completion_rate': '55.6%',
                'avg_completion_time': '2.3 soat'
            }
            
            text = (
                f"📊 **Status hisoboti**\n\n"
                f"📋 **Umumiy ma'lumotlar:**\n"
                f"• Jami ariyalar: {status_report['total_applications']}\n"
                f"• Yangi: {status_report['new']}\n"
                f"• Jarayonda: {status_report['in_progress']}\n"
                f"• Bajarilgan: {status_report['completed']}\n"
                f"• Bekor qilingan: {status_report['cancelled']}\n\n"
                f"📈 **Samaradorlik:**\n"
                f"• Bajarilish darajasi: {status_report['completion_rate']}\n"
                f"• O'rtacha vaqt: {status_report['avg_completion_time']}"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_status_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_status_menu")
    async def back_to_status_management_menu(callback: CallbackQuery, state: FSMContext):
        """Back to status management menu"""
        try:
            await callback.answer()
            
            status_text = (
                "📊 **Status boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_status_management_keyboard()
            await callback.message.edit_text(
                text=status_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router