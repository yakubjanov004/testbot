"""
Manager Statistics Handler - Simplified Implementation

This module handles statistics and reports for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_statistics_keyboard
from states.manager_states import StatisticsStates

def get_manager_statistics_router():
    router = Router()

    @router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
    async def statistics_menu(message: Message, state: FSMContext):
        """Show statistics menu"""
        try:
            stats_text = (
                "📊 **Statistika va hisobotlar**\n\n"
                "Quyidagi hisobotlardan birini tanlang:"
            )
            
            keyboard = get_statistics_keyboard()
            await message.answer(
                text=stats_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "daily_stats")
    async def show_daily_statistics(callback: CallbackQuery, state: FSMContext):
        """Show daily statistics"""
        try:
            await callback.answer()
            
            # Mock daily statistics
            daily_stats = {
                'total_applications': 45,
                'new_applications': 12,
                'in_progress': 8,
                'completed': 25,
                'total_revenue': 2500000,
                'avg_completion_time': '2.3 soat',
                'staff_online': 8,
                'satisfaction_rate': '92%'
            }
            
            text = (
                f"📊 **Kunlik statistika**\n\n"
                f"📋 **Ariyalar:**\n"
                f"• Jami: {daily_stats['total_applications']}\n"
                f"• Yangi: {daily_stats['new_applications']}\n"
                f"• Jarayonda: {daily_stats['in_progress']}\n"
                f"• Bajarilgan: {daily_stats['completed']}\n\n"
                f"💰 **Moliyaviy:**\n"
                f"• Jami tushum: {daily_stats['total_revenue']:,} so'm\n\n"
                f"👥 **Xodimlar:**\n"
                f"• Faol: {daily_stats['staff_online']}\n"
                f"• O'rtacha vaqt: {daily_stats['avg_completion_time']}\n"
                f"• Mijozlar mamnuniyati: {daily_stats['satisfaction_rate']}"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_stats_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "weekly_stats")
    async def show_weekly_statistics(callback: CallbackQuery, state: FSMContext):
        """Show weekly statistics"""
        try:
            await callback.answer()
            
            # Mock weekly statistics
            weekly_stats = {
                'total_applications': 234,
                'avg_daily': 33,
                'completed': 198,
                'completion_rate': '85%',
                'total_revenue': 12500000,
                'top_services': ['Internet ulanish', 'Texnik xizmat', 'TV xizmati'],
                'staff_performance': [
                    {'name': 'Aziz Karimov', 'applications': 45, 'rating': '4.8'},
                    {'name': 'Malika Yusupova', 'applications': 38, 'rating': '4.6'},
                    {'name': 'Bekzod Toirov', 'applications': 42, 'rating': '4.7'}
                ]
            }
            
            text = (
                f"📊 **Haftalik statistika**\n\n"
                f"📋 **Ariyalar:**\n"
                f"• Jami: {weekly_stats['total_applications']}\n"
                f"• O'rtacha kunlik: {weekly_stats['avg_daily']}\n"
                f"• Bajarilgan: {weekly_stats['completed']}\n"
                f"• Bajarilish darajasi: {weekly_stats['completion_rate']}\n\n"
                f"💰 **Moliyaviy:**\n"
                f"• Jami tushum: {weekly_stats['total_revenue']:,} so'm\n\n"
                f"🔍 **Eng ko'p xizmatlar:**\n"
            )
            
            for service in weekly_stats['top_services']:
                text += f"• {service}\n"
            
            text += f"\n👥 **Xodimlar samaradorligi:**\n"
            for staff in weekly_stats['staff_performance']:
                text += f"• {staff['name']}: {staff['applications']} ariza, {staff['rating']} ⭐\n"
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_stats_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "performance_report")
    async def show_performance_report(callback: CallbackQuery, state: FSMContext):
        """Show performance report"""
        try:
            await callback.answer()
            
            # Mock performance data
            performance = [
                {
                    'name': 'Aziz Karimov',
                    'position': 'Katta menejer',
                    'applications_today': 8,
                    'avg_rating': '4.8',
                    'response_time': '2.1 soat',
                    'status': 'Faol'
                },
                {
                    'name': 'Malika Yusupova',
                    'position': 'Menejer',
                    'applications_today': 6,
                    'avg_rating': '4.6',
                    'response_time': '2.5 soat',
                    'status': 'Faol'
                },
                {
                    'name': 'Bekzod Toirov',
                    'position': 'Kichik menejer',
                    'applications_today': 4,
                    'avg_rating': '4.7',
                    'response_time': '2.3 soat',
                    'status': 'Dam olish'
                }
            ]
            
            text = "📊 **Samaradorlik hisoboti**\n\n"
            for perf in performance:
                status_emoji = '🟢' if perf['status'] == 'Faol' else '🟡'
                text += (
                    f"{status_emoji} **{perf['name']}** ({perf['position']})\n"
                    f"📋 Bugungi ariyalar: {perf['applications_today']}\n"
                    f"⭐ O'rtacha baho: {perf['avg_rating']}\n"
                    f"⏱️ O'rtacha javob vaqti: {perf['response_time']}\n"
                    f"📈 Holat: {perf['status']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_stats_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_stats_menu")
    async def back_to_statistics_menu(callback: CallbackQuery, state: FSMContext):
        """Back to statistics menu"""
        try:
            await callback.answer()
            
            stats_text = (
                "📊 **Statistika va hisobotlar**\n\n"
                "Quyidagi hisobotlardan birini tanlang:"
            )
            
            keyboard = get_statistics_keyboard()
            await callback.message.edit_text(
                text=stats_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
