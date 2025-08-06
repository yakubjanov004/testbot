"""
Call Center Supervisor Orders Handler - Simplified Implementation

This module handles order management for call center supervisors.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.call_center_supervisor_buttons import get_orders_keyboard
from states.call_center_supervisor_states import OrdersStates

def get_call_center_supervisor_orders_router():
    router = Router()

    @router.message(F.text.in_(["📋 Buyurtmalar", "📋 Заказы"]))
    async def orders_menu(message: Message, state: FSMContext):
        """Show orders menu"""
        try:
            orders_text = (
                "📋 **Buyurtmalar boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_orders_keyboard()
            await message.answer(
                text=orders_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_all_orders")
    async def view_all_orders(callback: CallbackQuery, state: FSMContext):
        """View all orders"""
        try:
            await callback.answer()
            
            # Mock orders data
            orders = [
                {
                    'id': 'ORD001',
                    'client': 'Ahmad Karimov',
                    'type': 'Ulanish',
                    'status': 'Faol',
                    'priority': 'Yuqori',
                    'created': '2024-01-15 10:30',
                    'assigned_to': 'Aziz Karimov'
                },
                {
                    'id': 'ORD002',
                    'client': 'Malika Yusupova',
                    'type': 'Texnik xizmat',
                    'status': 'Kutilmoqda',
                    'priority': 'O\'rta',
                    'created': '2024-01-15 11:45',
                    'assigned_to': 'Malika Yusupova'
                },
                {
                    'id': 'ORD003',
                    'client': 'Bekzod Toirov',
                    'type': 'Ulanish',
                    'status': 'Bajarilgan',
                    'priority': 'Past',
                    'created': '2024-01-15 09:15',
                    'assigned_to': 'Bekzod Toirov'
                }
            ]
            
            text = "📋 **Barcha buyurtmalar**\n\n"
            for order in orders:
                status_emoji = {
                    'Faol': '🟡',
                    'Kutilmoqda': '🟠',
                    'Bajarilgan': '🟢'
                }.get(order['status'], '⚪')
                
                priority_emoji = {
                    'Yuqori': '🔴',
                    'O\'rta': '🟡',
                    'Past': '🟢'
                }.get(order['priority'], '⚪')
                
                text += (
                    f"{status_emoji} **{order['id']}** - {order['client']}\n"
                    f"📋 Tur: {order['type']}\n"
                    f"{priority_emoji} Daraja: {order['priority']}\n"
                    f"👤 Bajaruvchi: {order['assigned_to']}\n"
                    f"📅 Sana: {order['created']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_orders_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "view_pending_orders")
    async def view_pending_orders(callback: CallbackQuery, state: FSMContext):
        """View pending orders"""
        try:
            await callback.answer()
            
            # Mock pending orders
            pending_orders = [
                {
                    'id': 'ORD002',
                    'client': 'Malika Yusupova',
                    'type': 'Texnik xizmat',
                    'priority': 'O\'rta',
                    'created': '2024-01-15 11:45',
                    'description': 'Internet tezligi sekin'
                }
            ]
            
            text = "⏳ **Kutilayotgan buyurtmalar**\n\n"
            for order in pending_orders:
                priority_emoji = {
                    'Yuqori': '🔴',
                    'O\'rta': '🟡',
                    'Past': '🟢'
                }.get(order['priority'], '⚪')
                
                text += (
                    f"📋 **{order['id']}** - {order['client']}\n"
                    f"🔧 Tur: {order['type']}\n"
                    f"{priority_emoji} Daraja: {order['priority']}\n"
                    f"📝 Tavsif: {order['description']}\n"
                    f"📅 Sana: {order['created']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_orders_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "assign_orders")
    async def assign_orders(callback: CallbackQuery, state: FSMContext):
        """Assign orders to staff"""
        try:
            await callback.answer()
            
            text = (
                "👥 **Buyurtma berish**\n\n"
                "Buyurtmalarni xodimlarga berish funksiyasi.\n\n"
                "📋 Mavjud buyurtmalar:\n"
                "• ORD002 - Malika Yusupova (Texnik xizmat)\n\n"
                "👤 Mavjud xodimlar:\n"
                "• Aziz Karimov (Operator)\n"
                "• Malika Yusupova (Operator)\n"
                "• Bekzod Toirov (Texnik)"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_orders_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_orders_menu")
    async def back_to_orders_menu(callback: CallbackQuery, state: FSMContext):
        """Back to orders menu"""
        try:
            await callback.answer()
            
            orders_text = (
                "📋 **Buyurtmalar boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_orders_keyboard()
            await callback.message.edit_text(
                text=orders_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router