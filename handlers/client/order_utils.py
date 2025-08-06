"""
Client Order Utils - Simplified Implementation

This module provides utility functions for client orders.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_order_utils_keyboard, get_main_menu_keyboard
from states.client_states import OrderUtilsStates
from utils.role_system import get_role_router

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567'
    }

async def get_user_lang(user_id: int) -> str:
    """Mock get user language"""
    return 'uz'

async def get_order_status(order_id: str):
    """Mock get order status"""
    return {
        'status': 'in_progress',
        'progress': 75,
        'estimated_completion': '2024-01-20',
        'technician': 'Ahmad Karimov',
        'notes': 'Texnik xizmat jarayonda'
    }

def get_order_utils_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["🔧 Buyurtma yordamchisi", "🔧 Помощь заказа"]))
    async def order_utils_handler(message: Message, state: FSMContext):
        """Order utils handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            lang = user.get('language', 'uz')
            
            utils_text = (
                "🔧 <b>Buyurtma yordamchisi - To'liq ma'lumot</b>\n\n"
                "📋 <b>Mavjud funksiyalar:</b>\n"
                "• Buyurtma holatini tekshirish\n"
                "• Texnik xizmat ma'lumotlari\n"
                "• Narxlar va to'lov ma'lumotlari\n"
                "• Ish vaqti va jadval\n"
                "• Muhim telefon raqamlar\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "🔧 <b>Помощь заказа - Полная информация</b>\n\n"
                "📋 <b>Доступные функции:</b>\n"
                "• Проверка статуса заказа\n"
                "• Информация о техническом обслуживании\n"
                "• Цены и платежная информация\n"
                "• Рабочее время и расписание\n"
                "• Важные номера телефонов\n\n"
                "Выберите один из разделов ниже:"
            )
            
            sent_message = await message.answer(
                text=utils_text,
                reply_markup=get_order_utils_keyboard(lang),
                parse_mode='HTML'
            )
            
            await state.set_state(OrderUtilsStates.utils_menu)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "check_order_status")
    async def check_order_status(callback: CallbackQuery, state: FSMContext):
        """Check order status"""
        try:
            await callback.answer()
            
            # Mock order status
            status_info = await get_order_status("TX_12345678")
            
            status_text = (
                f"📊 <b>Buyurtma holati - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Buyurtma ID:</b> TX_12345678\n"
                f"📈 <b>Holat:</b> {status_info['status']}\n"
                f"📊 <b>Progress:</b> {status_info['progress']}%\n"
                f"⏰ <b>Taxminiy tugash:</b> {status_info['estimated_completion']}\n"
                f"👨‍🔧 <b>Texnik:</b> {status_info['technician']}\n"
                f"📝 <b>Izoh:</b> {status_info['notes']}\n\n"
                f"🔄 <b>Keyingi qadam:</b> Texnik xizmat yakunlanishi"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_utils")]
            ])
            
            await callback.message.edit_text(status_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_utils")
    async def back_to_utils(callback: CallbackQuery, state: FSMContext):
        """Back to utils menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            utils_text = (
                "🔧 <b>Buyurtma yordamchisi - To'liq ma'lumot</b>\n\n"
                "📋 <b>Mavjud funksiyalar:</b>\n"
                "• Buyurtma holatini tekshirish\n"
                "• Texnik xizmat ma'lumotlari\n"
                "• Narxlar va to'lov ma'lumotlari\n"
                "• Ish vaqti va jadval\n"
                "• Muhim telefon raqamlar\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "🔧 <b>Помощь заказа - Полная информация</b>\n\n"
                "📋 <b>Доступные функции:</b>\n"
                "• Проверка статуса заказа\n"
                "• Информация о техническом обслуживании\n"
                "• Цены и платежная информация\n"
                "• Рабочее время и расписание\n"
                "• Важные номера телефонов\n\n"
                "Выберите один из разделов ниже:"
            )
            
            await callback.message.edit_text(
                text=utils_text,
                reply_markup=get_order_utils_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router
