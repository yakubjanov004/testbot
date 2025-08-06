"""
Warehouse Orders Handler - Simplified Implementation

This module handles orders functionality for warehouse.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import get_orders_keyboard
from states.warehouse_states import OrdersStates

def get_warehouse_orders_router():
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
                    'type': 'Internet ulanish',
                    'status': 'Jarayonda',
                    'materials': ['Router TP-Link', 'Kabel UTP'],
                    'created': '2024-01-15 10:30',
                    'technician': 'Aziz Karimov'
                },
                {
                    'id': 'ORD002',
                    'client': 'Malika Yusupova',
                    'type': 'TV xizmati',
                    'status': 'Bajarilgan',
                    'materials': ['TV antena', 'Kabel'],
                    'created': '2024-01-15 11:45',
                    'technician': 'Bekzod Rahimov'
                },
                {
                    'id': 'ORD003',
                    'client': 'Bekzod Toirov',
                    'type': 'Texnik xizmat',
                    'status': 'Yangi',
                    'materials': ['Modem', 'Kabel'],
                    'created': '2024-01-15 09:15',
                    'technician': 'Olimjon Toshmatov'
                }
            ]
            
            text = "📋 **Barcha buyurtmalar**\n\n"
            for order in orders:
                status_emoji = {
                    'Yangi': '🆕',
                    'Jarayonda': '🔄',
                    'Bajarilgan': '✅',
                    'Bekor qilingan': '❌'
                }.get(order['status'], '⚪')
                
                text += (
                    f"{status_emoji} **{order['id']}** - {order['client']}\n"
                    f"📋 Tur: {order['type']}\n"
                    f"📊 Status: {order['status']}\n"
                    f"👨‍🔧 Texnik: {order['technician']}\n"
                    f"📦 Materiallar: {', '.join(order['materials'])}\n"
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

    @router.callback_query(F.data == "process_order")
    async def process_order(callback: CallbackQuery, state: FSMContext):
        """Process order"""
        try:
            await callback.answer()
            
            text = (
                "📋 **Buyurtmani qayta ishlash**\n\n"
                "Buyurtmalarni qayta ishlash funksiyasi.\n\n"
                "📋 Mavjud buyurtmalar:\n"
                "• ORD001 - Ahmad Karimov (Internet ulanish) - Jarayonda\n"
                "• ORD002 - Malika Yusupova (TV xizmati) - Bajarilgan\n"
                "• ORD003 - Bekzod Toirov (Texnik xizmat) - Yangi\n\n"
                "👨‍🔧 Mavjud texniklar:\n"
                "• Aziz Karimov (Internet texnik)\n"
                "• Bekzod Rahimov (TV texnik)\n"
                "• Olimjon Toshmatov (Umumiy texnik)"
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

    @router.callback_query(F.data == "order_statistics")
    async def order_statistics(callback: CallbackQuery, state: FSMContext):
        """Show order statistics"""
        try:
            await callback.answer()
            
            # Mock statistics data
            statistics = {
                'total_orders': 45,
                'new_orders': 12,
                'in_progress': 8,
                'completed': 25,
                'completion_rate': '55.6%',
                'avg_completion_time': '2.3 soat',
                'popular_services': [
                    {'service': 'Internet ulanish', 'count': 20},
                    {'service': 'TV xizmati', 'count': 15},
                    {'service': 'Texnik xizmat', 'count': 10}
                ]
            }
            
            text = (
                f"📊 **Buyurtmalar statistikasi**\n\n"
                f"📈 **Umumiy ma'lumotlar:**\n"
                f"• Jami buyurtmalar: {statistics['total_orders']}\n"
                f"• Yangi: {statistics['new_orders']}\n"
                f"• Jarayonda: {statistics['in_progress']}\n"
                f"• Bajarilgan: {statistics['completed']}\n\n"
                f"📈 **Samaradorlik:**\n"
                f"• Bajarilish darajasi: {statistics['completion_rate']}\n"
                f"• O'rtacha vaqt: {statistics['avg_completion_time']}\n\n"
                f"🏆 **Eng ko'p talab qilinadigan xizmatlar:**\n"
            )
            
            for service in statistics['popular_services']:
                text += f"• {service['service']}: {service['count']} ta\n"
            
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
