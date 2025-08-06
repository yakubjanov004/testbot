"""
Client Orders Handler - Simplified Implementation

This module handles viewing client orders with pagination.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from states.client_states import OrderStates

def get_orders_router():
    router = Router()

    @router.message(F.text.in_(["📋 Mening buyurtmalarim"]))
    async def show_my_orders(message: Message, state: FSMContext):
        """Show user orders"""
        try:
            # Mock orders data with complete information
            orders = [
                {
                    'id': 1,
                    'type': 'service',
                    'status': 'active',
                    'created_at': '2024-01-15 10:30:00',
                    'description': 'Internet tezligi sekin',
                    'region': 'Toshkent shahri',
                    'address': 'Chilanzar tumani, 15-uy',
                    'request_id': 'TX_12345678',
                    'priority': 'high',
                    'assigned_technician': 'Ahmad Karimov',
                    'estimated_completion': '2024-01-20',
                    'notes': 'Mijoz internet tezligi juda sekin ekanligini bildirdi'
                },
                {
                    'id': 2,
                    'type': 'connection',
                    'status': 'completed',
                    'created_at': '2024-01-10 14:20:00',
                    'description': 'Yangi ulanish',
                    'region': 'Toshkent viloyati',
                    'address': 'Zangiota tumani, 25-uy',
                    'request_id': 'UL_87654321',
                    'priority': 'medium',
                    'assigned_technician': 'Bekzod Rahimov',
                    'completion_date': '2024-01-12',
                    'notes': 'Yangi uy uchun internet ulanishi muvaffaqiyatli yakunlandi'
                },
                {
                    'id': 3,
                    'type': 'service',
                    'status': 'pending',
                    'created_at': '2024-01-12 09:15:00',
                    'description': 'TV signal yo\'q',
                    'region': 'Andijon',
                    'address': 'Andijon shahri, 8-uy',
                    'request_id': 'TX_11223344',
                    'priority': 'high',
                    'assigned_technician': 'Olimjon Toshmatov',
                    'estimated_completion': '2024-01-18',
                    'notes': 'TV signal to\'liq yo\'q, tezkor yordam kerak'
                }
            ]
            
            if not orders:
                await message.answer("📭 Sizda hali buyurtmalar mavjud emas.")
                return
            
            # Show first order
            await show_order_details(message, orders[0], orders, 0)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("order_"))
    async def handle_order_navigation(callback: CallbackQuery, state: FSMContext):
        """Handle order navigation"""
        try:
            await callback.answer()
            
            data = callback.data.split("_")
            action = data[1]
            
            if action == "next":
                current_index = int(data[2])
                await show_next_order(callback, current_index, 1)
            elif action == "prev":
                current_index = int(data[2])
                await show_previous_order(callback, current_index, 1)
            elif action == "back":
                await callback.message.edit_text("📋 Mening buyurtmalarim")
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    async def show_order_details(message_or_callback, order, orders, index):
        """Show detailed order information"""
        status_emoji = {
            'active': '🟡',
            'completed': '🟢',
            'pending': '🟠',
            'cancelled': '🔴'
        }
        
        type_emoji = {
            'service': '🔧',
            'connection': '🔌'
        }
        
        priority_emoji = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }
        
        status = status_emoji.get(order['status'], '⚪')
        order_type = type_emoji.get(order['type'], '📋')
        priority = priority_emoji.get(order['priority'], '⚪')
        
        details_text = f"""
{status} **Buyurtma #{order['id']}** {order_type}

📋 **Ma'lumotlar:**
• ID: `{order['request_id']}`
• Turi: {order['type'].title()}
• Holat: {order['status'].title()}
• Daraja: {priority} {order['priority'].title()}

📍 **Manzil:**
• Viloyat: {order['region']}
• Manzil: {order['address']}

📅 **Vaqt:**
• Yaratilgan: {order['created_at']}
"""
        
        if order['status'] == 'completed' and 'completion_date' in order:
            details_text += f"• Yakunlangan: {order['completion_date']}\n"
        elif 'estimated_completion' in order:
            details_text += f"• Taxminiy yakunlanish: {order['estimated_completion']}\n"
        
        if 'assigned_technician' in order:
            details_text += f"\n👨‍🔧 **Texnik:** {order['assigned_technician']}"
        
        if 'notes' in order:
            details_text += f"\n\n📝 **Izoh:** {order['notes']}"
        
        # Navigation keyboard
        keyboard = []
        nav_row = []
        
        if index > 0:
            nav_row.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"order_prev_{index}"))
        
        if index < len(orders) - 1:
            nav_row.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"order_next_{index}"))
        
        if nav_row:
            keyboard.append(nav_row)
        
        keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_menu")])
        
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(details_text, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            await message_or_callback.message.edit_text(details_text, reply_markup=reply_markup, parse_mode="Markdown")

    async def show_next_order(callback: CallbackQuery, current_index: int, current_page: int):
        """Show next order"""
        orders = [
            {
                'id': 1,
                'type': 'service',
                'status': 'active',
                'created_at': '2024-01-15 10:30:00',
                'description': 'Internet tezligi sekin',
                'region': 'Toshkent shahri',
                'address': 'Chilanzar tumani, 15-uy',
                'request_id': 'TX_12345678',
                'priority': 'high',
                'assigned_technician': 'Ahmad Karimov',
                'estimated_completion': '2024-01-20',
                'notes': 'Mijoz internet tezligi juda sekin ekanligini bildirdi'
            },
            {
                'id': 2,
                'type': 'connection',
                'status': 'completed',
                'created_at': '2024-01-10 14:20:00',
                'description': 'Yangi ulanish',
                'region': 'Toshkent viloyati',
                'address': 'Zangiota tumani, 25-uy',
                'request_id': 'UL_87654321',
                'priority': 'medium',
                'assigned_technician': 'Bekzod Rahimov',
                'completion_date': '2024-01-12',
                'notes': 'Yangi uy uchun internet ulanishi muvaffaqiyatli yakunlandi'
            },
            {
                'id': 3,
                'type': 'service',
                'status': 'pending',
                'created_at': '2024-01-12 09:15:00',
                'description': 'TV signal yo\'q',
                'region': 'Andijon',
                'address': 'Andijon shahri, 8-uy',
                'request_id': 'TX_11223344',
                'priority': 'high',
                'assigned_technician': 'Olimjon Toshmatov',
                'estimated_completion': '2024-01-18',
                'notes': 'TV signal to\'liq yo\'q, tezkor yordam kerak'
            }
        ]
        
        next_index = current_index + 1
        if next_index < len(orders):
            await show_order_details(callback, orders[next_index], orders, next_index)

    async def show_previous_order(callback: CallbackQuery, current_index: int, current_page: int):
        """Show previous order"""
        orders = [
            {
                'id': 1,
                'type': 'service',
                'status': 'active',
                'created_at': '2024-01-15 10:30:00',
                'description': 'Internet tezligi sekin',
                'region': 'Toshkent shahri',
                'address': 'Chilanzar tumani, 15-uy',
                'request_id': 'TX_12345678',
                'priority': 'high',
                'assigned_technician': 'Ahmad Karimov',
                'estimated_completion': '2024-01-20',
                'notes': 'Mijoz internet tezligi juda sekin ekanligini bildirdi'
            },
            {
                'id': 2,
                'type': 'connection',
                'status': 'completed',
                'created_at': '2024-01-10 14:20:00',
                'description': 'Yangi ulanish',
                'region': 'Toshkent viloyati',
                'address': 'Zangiota tumani, 25-uy',
                'request_id': 'UL_87654321',
                'priority': 'medium',
                'assigned_technician': 'Bekzod Rahimov',
                'completion_date': '2024-01-12',
                'notes': 'Yangi uy uchun internet ulanishi muvaffaqiyatli yakunlandi'
            },
            {
                'id': 3,
                'type': 'service',
                'status': 'pending',
                'created_at': '2024-01-12 09:15:00',
                'description': 'TV signal yo\'q',
                'region': 'Andijon',
                'address': 'Andijon shahri, 8-uy',
                'request_id': 'TX_11223344',
                'priority': 'high',
                'assigned_technician': 'Olimjon Toshmatov',
                'estimated_completion': '2024-01-18',
                'notes': 'TV signal to\'liq yo\'q, tezkor yordam kerak'
            }
        ]
        
        prev_index = current_index - 1
        if prev_index >= 0:
            await show_order_details(callback, orders[prev_index], orders, prev_index)

    return router
