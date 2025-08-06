"""
Manager Technician Assignment Handler - Simplified Implementation

This module handles technician assignment for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_technician_assignment_keyboard
from states.manager_states import TechnicianAssignmentStates

def get_manager_technician_assignment_router():
    router = Router()

    @router.message(F.text.in_(["👨‍🔧 Texnik tayinlash", "👨‍🔧 Назначение техника"]))
    async def technician_assignment_menu(message: Message, state: FSMContext):
        """Show technician assignment menu"""
        try:
            assignment_text = (
                "👨‍🔧 **Texnik tayinlash**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_technician_assignment_keyboard()
            await message.answer(
                text=assignment_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_available_technicians")
    async def view_available_technicians(callback: CallbackQuery, state: FSMContext):
        """View available technicians"""
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
            
            text = "👨‍🔧 **Mavjud texniklar**\n\n"
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
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_assignment_menu")]
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
                "• APP001 - Ahmad Karimov (Ulanish) - Texnik kerak\n"
                "• APP002 - Malika Yusupova (Texnik xizmat) - Texnik kerak\n"
                "• APP003 - Bekzod Toirov (Ulanish) - Texnik tayinlangan\n\n"
                "👨‍🔧 Mavjud texniklar:\n"
                "• Ahmad Karimov (Internet texnik) - 3 buyurtma\n"
                "• Bekzod Rahimov (TV texnik) - 2 buyurtma\n"
                "• Olimjon Toshmatov (Umumiy texnik) - 0 buyurtma"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_assignment_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "technician_performance")
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
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_assignment_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_assignment_menu")
    async def back_to_technician_assignment_menu(callback: CallbackQuery, state: FSMContext):
        """Back to technician assignment menu"""
        try:
            await callback.answer()
            
            assignment_text = (
                "👨‍🔧 **Texnik tayinlash**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_technician_assignment_keyboard()
            await callback.message.edit_text(
                text=assignment_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router 