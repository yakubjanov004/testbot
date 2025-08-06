"""
Manager Staff Activity Handler - Simplified Implementation

This module handles staff activity management for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_staff_activity_keyboard
from states.manager_states import StaffActivityStates

def get_manager_staff_activity_router():
    router = Router()

    @router.message(F.text.in_(["👥 Xodimlar faolligi", "👥 Активность персонала"]))
    async def staff_activity_menu(message: Message, state: FSMContext):
        """Show staff activity menu"""
        try:
            activity_text = (
                "👥 **Xodimlar faolligi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_staff_activity_keyboard()
            await message.answer(
                text=activity_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_staff_activity")
    async def view_staff_activity(callback: CallbackQuery, state: FSMContext):
        """View staff activity"""
        try:
            await callback.answer()
            
            # Mock staff activity data
            staff_activity = [
                {
                    'name': 'Aziz Karimov',
                    'role': 'Katta menejer',
                    'status': 'Faol',
                    'orders_today': 8,
                    'response_time': '2.1 soat',
                    'rating': '4.8'
                },
                {
                    'name': 'Malika Yusupova',
                    'role': 'Menejer',
                    'status': 'Faol',
                    'orders_today': 6,
                    'response_time': '2.5 soat',
                    'rating': '4.6'
                },
                {
                    'name': 'Bekzod Toirov',
                    'role': 'Kichik menejer',
                    'status': 'Dam olish',
                    'orders_today': 0,
                    'response_time': 'N/A',
                    'rating': '4.7'
                }
            ]
            
            text = "👥 **Xodimlar faolligi**\n\n"
            for staff in staff_activity:
                status_emoji = '🟢' if staff['status'] == 'Faol' else '🟡'
                text += (
                    f"{status_emoji} **{staff['name']}** ({staff['role']})\n"
                    f"📊 Bugungi buyurtmalar: {staff['orders_today']}\n"
                    f"⏱️ O'rtacha javob vaqti: {staff['response_time']}\n"
                    f"⭐ Baho: {staff['rating']}\n"
                    f"📈 Holat: {staff['status']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_activity_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "assign_tasks")
    async def assign_tasks(callback: CallbackQuery, state: FSMContext):
        """Assign tasks to staff"""
        try:
            await callback.answer()
            
            text = (
                "📋 **Vazifa berish**\n\n"
                "Xodimlarga vazifa berish funksiyasi.\n\n"
                "👥 Mavjud xodimlar:\n"
                "• Aziz Karimov (Katta menejer) - 8 buyurtma\n"
                "• Malika Yusupova (Menejer) - 6 buyurtma\n"
                "• Bekzod Toirov (Kichik menejer) - 0 buyurtma\n\n"
                "📋 Mavjud vazifalar:\n"
                "• Yangi ariyalarni ko'rib chiqish\n"
                "• Texniklarni tayinlash\n"
                "• Mijozlar bilan bog'lanish\n"
                "• Hisobot tayyorlash"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_activity_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "performance_review")
    async def performance_review(callback: CallbackQuery, state: FSMContext):
        """Show performance review"""
        try:
            await callback.answer()
            
            # Mock performance data
            performance = [
                {
                    'name': 'Aziz Karimov',
                    'completed_orders': 45,
                    'avg_rating': '4.8',
                    'response_time': '2.1 soat',
                    'efficiency': '92%'
                },
                {
                    'name': 'Malika Yusupova',
                    'completed_orders': 38,
                    'avg_rating': '4.6',
                    'response_time': '2.5 soat',
                    'efficiency': '88%'
                },
                {
                    'name': 'Bekzod Toirov',
                    'completed_orders': 42,
                    'avg_rating': '4.7',
                    'response_time': '2.3 soat',
                    'efficiency': '90%'
                }
            ]
            
            text = "📊 **Samaradorlik baholash**\n\n"
            for perf in performance:
                text += (
                    f"👤 **{perf['name']}**\n"
                    f"✅ Bajarilgan buyurtmalar: {perf['completed_orders']}\n"
                    f"⭐ O'rtacha baho: {perf['avg_rating']}\n"
                    f"⏱️ O'rtacha javob vaqti: {perf['response_time']}\n"
                    f"📈 Samaradorlik: {perf['efficiency']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_activity_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_activity_menu")
    async def back_to_staff_activity_menu(callback: CallbackQuery, state: FSMContext):
        """Back to staff activity menu"""
        try:
            await callback.answer()
            
            activity_text = (
                "👥 **Xodimlar faolligi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_staff_activity_keyboard()
            await callback.message.edit_text(
                text=activity_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
