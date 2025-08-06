"""
Call Center Supervisor Statistics Handler - Simplified Implementation

This module handles statistics and reports for call center supervisors.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.call_center_supervisor_buttons import get_statistics_keyboard
from states.call_center_supervisor_states import StatisticsStates

def get_call_center_supervisor_statistics_router():
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
                'total_calls': 156,
                'answered_calls': 142,
                'missed_calls': 14,
                'avg_call_duration': '4.2 daqiqa',
                'satisfaction_rate': '92%',
                'total_orders': 89,
                'completed_orders': 76,
                'pending_orders': 13,
                'staff_online': 8,
                'peak_hours': '10:00-12:00, 15:00-17:00'
            }
            
            text = (
                f"📊 **Kunlik statistika**\n\n"
                f"📞 **Qo'ng'iroqlar:**\n"
                f"• Jami: {daily_stats['total_calls']}\n"
                f"• Javob berilgan: {daily_stats['answered_calls']}\n"
                f"• O'tkazib yuborilgan: {daily_stats['missed_calls']}\n"
                f"• O'rtacha vaqt: {daily_stats['avg_call_duration']}\n\n"
                f"📋 **Buyurtmalar:**\n"
                f"• Jami: {daily_stats['total_orders']}\n"
                f"• Bajarilgan: {daily_stats['completed_orders']}\n"
                f"• Kutilayotgan: {daily_stats['pending_orders']}\n\n"
                f"👥 **Xodimlar:**\n"
                f"• Faol: {daily_stats['staff_online']}\n"
                f"• Mijozlar mamnuniyati: {daily_stats['satisfaction_rate']}\n\n"
                f"⏰ **Eng faol vaqtlar:**\n"
                f"• {daily_stats['peak_hours']}"
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
                'total_calls': 892,
                'avg_daily_calls': 127,
                'total_orders': 534,
                'completed_orders': 487,
                'completion_rate': '91%',
                'top_issues': ['Internet uzulish', 'TV signal yo\'q', 'Tezlik sekin'],
                'staff_performance': [
                    {'name': 'Aziz Karimov', 'calls': 156, 'orders': 89, 'rating': '4.8'},
                    {'name': 'Malika Yusupova', 'calls': 142, 'orders': 78, 'rating': '4.6'},
                    {'name': 'Bekzod Toirov', 'calls': 134, 'orders': 76, 'rating': '4.7'}
                ]
            }
            
            text = (
                f"📊 **Haftalik statistika**\n\n"
                f"📞 **Qo'ng'iroqlar:**\n"
                f"• Jami: {weekly_stats['total_calls']}\n"
                f"• O'rtacha kunlik: {weekly_stats['avg_daily_calls']}\n\n"
                f"📋 **Buyurtmalar:**\n"
                f"• Jami: {weekly_stats['total_orders']}\n"
                f"• Bajarilgan: {weekly_stats['completed_orders']}\n"
                f"• Bajarilish darajasi: {weekly_stats['completion_rate']}\n\n"
                f"🔍 **Eng ko'p muammolar:**\n"
            )
            
            for issue in weekly_stats['top_issues']:
                text += f"• {issue}\n"
            
            text += f"\n👥 **Xodimlar samaradorligi:**\n"
            for staff in weekly_stats['staff_performance']:
                text += f"• {staff['name']}: {staff['calls']} qo'ng'iroq, {staff['orders']} buyurtma, {staff['rating']} ⭐\n"
            
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

    @router.callback_query(F.data == "staff_performance")
    async def show_staff_performance(callback: CallbackQuery, state: FSMContext):
        """Show staff performance statistics"""
        try:
            await callback.answer()
            
            # Mock staff performance data
            staff_performance = [
                {
                    'name': 'Aziz Karimov',
                    'position': 'Operator',
                    'calls_today': 23,
                    'orders_today': 12,
                    'avg_rating': '4.8',
                    'response_time': '2.1 daqiqa',
                    'status': 'Faol'
                },
                {
                    'name': 'Malika Yusupova',
                    'position': 'Operator',
                    'calls_today': 19,
                    'orders_today': 10,
                    'avg_rating': '4.6',
                    'response_time': '2.3 daqiqa',
                    'status': 'Faol'
                },
                {
                    'name': 'Bekzod Toirov',
                    'position': 'Texnik',
                    'calls_today': 15,
                    'orders_today': 8,
                    'avg_rating': '4.7',
                    'response_time': '2.5 daqiqa',
                    'status': 'Dam olish'
                }
            ]
            
            text = "👥 **Xodimlar samaradorligi**\n\n"
            for staff in staff_performance:
                status_emoji = '🟢' if staff['status'] == 'Faol' else '🟡'
                text += (
                    f"{status_emoji} **{staff['name']}** ({staff['position']})\n"
                    f"📞 Bugungi qo'ng'iroqlar: {staff['calls_today']}\n"
                    f"📋 Bugungi buyurtmalar: {staff['orders_today']}\n"
                    f"⭐ O'rtacha baho: {staff['avg_rating']}\n"
                    f"⏱️ O'rtacha javob vaqti: {staff['response_time']}\n"
                    f"📊 Holat: {staff['status']}\n\n"
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