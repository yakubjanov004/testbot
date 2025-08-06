"""
Controller Technicians Handler - Simplified Implementation

This module handles technician management for controllers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_technicians_keyboard
from states.controller_states import TechniciansStates

def get_controller_technicians_router():
    router = Router()

    @router.message(F.text.in_(["👨‍🔧 Texniklar", "👨‍🔧 Техники"]))
    async def technicians_menu(message: Message, state: FSMContext):
        """Show technicians menu"""
        try:
            tech_text = (
                "👨‍🔧 **Texniklar boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_technicians_keyboard()
            await message.answer(
                text=tech_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_all_technicians")
    async def view_all_technicians(callback: CallbackQuery, state: FSMContext):
        """View all technicians"""
        try:
            await callback.answer()
            
            # Mock technicians data
            technicians = [
                {
                    'id': 1,
                    'name': 'Ahmad Karimov',
                    'specialization': 'Internet texnik',
                    'status': 'Faol',
                    'experience': '5 yil',
                    'rating': '4.8',
                    'current_orders': 3
                },
                {
                    'id': 2,
                    'name': 'Bekzod Rahimov',
                    'specialization': 'TV texnik',
                    'status': 'Faol',
                    'experience': '3 yil',
                    'rating': '4.6',
                    'current_orders': 2
                },
                {
                    'id': 3,
                    'name': 'Olimjon Toshmatov',
                    'specialization': 'Umumiy texnik',
                    'status': 'Dam olish',
                    'experience': '7 yil',
                    'rating': '4.9',
                    'current_orders': 0
                }
            ]
            
            text = "👨‍🔧 **Barcha texniklar**\n\n"
            for tech in technicians:
                status_emoji = '🟢' if tech['status'] == 'Faol' else '🟡'
                text += (
                    f"{status_emoji} **{tech['name']}**\n"
                    f"🔧 Mutaxassislik: {tech['specialization']}\n"
                    f"⭐ Baho: {tech['rating']}\n"
                    f"📅 Tajriba: {tech['experience']}\n"
                    f"📋 Joriy buyurtmalar: {tech['current_orders']}\n"
                    f"📊 Holat: {tech['status']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_tech_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "assign_technician")
    async def assign_technician(callback: CallbackQuery, state: FSMContext):
        """Assign technician to order"""
        try:
            await callback.answer()
            
            text = (
                "👨‍🔧 **Texnik tayinlash**\n\n"
                "Buyurtmalarga texnik tayinlash funksiyasi.\n\n"
                "📋 Mavjud buyurtmalar:\n"
                "• ORD001 - Internet uzulish (Ahmad Karimov)\n"
                "• ORD002 - TV signal yo'q (Bekzod Rahimov)\n\n"
                "👨‍🔧 Mavjud texniklar:\n"
                "• Ahmad Karimov (Internet texnik) - 3 buyurtma\n"
                "• Bekzod Rahimov (TV texnik) - 2 buyurtma\n"
                "• Olimjon Toshmatov (Umumiy texnik) - 0 buyurtma"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_tech_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_performance")
    async def technician_performance(callback: CallbackQuery, state: FSMContext):
        """Show technician performance"""
        try:
            await callback.answer()
            
            # Mock performance data
            performance = [
                {
                    'name': 'Ahmad Karimov',
                    'completed_orders': 45,
                    'avg_rating': '4.8',
                    'response_time': '1.5 soat',
                    'specialization': 'Internet texnik'
                },
                {
                    'name': 'Bekzod Rahimov',
                    'completed_orders': 38,
                    'avg_rating': '4.6',
                    'response_time': '2.1 soat',
                    'specialization': 'TV texnik'
                },
                {
                    'name': 'Olimjon Toshmatov',
                    'completed_orders': 52,
                    'avg_rating': '4.9',
                    'response_time': '1.8 soat',
                    'specialization': 'Umumiy texnik'
                }
            ]
            
            text = "📊 **Texniklar samaradorligi**\n\n"
            for perf in performance:
                text += (
                    f"👨‍🔧 **{perf['name']}** ({perf['specialization']})\n"
                    f"✅ Bajarilgan buyurtmalar: {perf['completed_orders']}\n"
                    f"⭐ O'rtacha baho: {perf['avg_rating']}\n"
                    f"⏱️ O'rtacha javob vaqti: {perf['response_time']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_tech_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_tech_menu")
    async def back_to_technicians_menu(callback: CallbackQuery, state: FSMContext):
        """Back to technicians menu"""
        try:
            await callback.answer()
            
            tech_text = (
                "👨‍🔧 **Texniklar boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_technicians_keyboard()
            await callback.message.edit_text(
                text=tech_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
