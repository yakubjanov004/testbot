"""
Client Orders Handler - Simplified Implementation

This module handles viewing client orders with pagination.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from states.client_states import OrderStates
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

async def get_user_orders(user_id: int, page: int = 1, limit: int = 5):
    """Mock user orders"""
    # Mock orders data
    orders = [
        {
            'id': 1,
            'type': 'service',
            'status': 'active',
            'created_at': '2024-01-15 10:30:00',
            'description': 'Internet tezligi sekin',
            'region': 'Toshkent shahri',
            'address': 'Chilanzar tumani, 15-uy',
            'request_id': 'TX_12345678'
        },
        {
            'id': 2,
            'type': 'connection',
            'status': 'completed',
            'created_at': '2024-01-10 14:20:00',
            'description': 'Yangi ulanish',
            'region': 'Toshkent viloyati',
            'address': 'Zangiota tumani, 25-uy',
            'request_id': 'UL_87654321'
        },
        {
            'id': 3,
            'type': 'service',
            'status': 'pending',
            'created_at': '2024-01-12 09:15:00',
            'description': 'TV signal yo\'q',
            'region': 'Andijon',
            'address': 'Andijon shahri, 8-uy',
            'request_id': 'TX_11223344'
        },
        {
            'id': 4,
            'type': 'connection',
            'status': 'active',
            'created_at': '2024-01-08 16:45:00',
            'description': 'Uy internet ulanishi',
            'region': 'Farg\'ona',
            'address': 'Farg\'ona shahri, 12-uy',
            'request_id': 'UL_55667788'
        },
        {
            'id': 5,
            'type': 'service',
            'status': 'completed',
            'created_at': '2024-01-05 11:30:00',
            'description': 'Router muammosi',
            'region': 'Samarqand',
            'address': 'Samarqand shahri, 30-uy',
            'request_id': 'TX_99887766'
        }
    ]
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_orders = orders[start:end]
    
    return {
        'orders': paginated_orders,
        'total': len(orders),
        'page': page,
        'total_pages': (len(orders) + limit - 1) // limit
    }

async def get_order_details(order_id: int):
    """Mock order details"""
    return {
        'id': order_id,
        'type': 'service' if order_id % 2 == 1 else 'connection',
        'status': 'active',
        'created_at': '2024-01-15 10:30:00',
        'description': 'Internet tezligi sekin',
        'region': 'Toshkent shahri',
        'address': 'Chilanzar tumani, 15-uy',
        'request_id': f"{'TX' if order_id % 2 == 1 else 'UL'}_{order_id}",
        'technician': 'Ahmad Karimov',
        'estimated_time': '2-3 kun',
        'priority': 'normal'
    }

def get_orders_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["📋 Mening buyurtmalarim"]))
    async def show_my_orders(message: Message, state: FSMContext):
        """Show user orders with pagination"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi. Iltimos, qaytadan kiriting.")
                return
            
            # Get first page of orders
            orders_data = await get_user_orders(message.from_user.id, page=1)
            
            if not orders_data['orders']:
                await message.answer("Sizda hali buyurtmalar yo'q.")
                return
            
            # Show first order
            await show_order_details(message, orders_data['orders'][0], orders_data, 0)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("order_"))
    async def handle_order_navigation(callback: CallbackQuery, state: FSMContext):
        """Handle order navigation (next/previous)"""
        try:
            await callback.answer()
            
            action = callback.data.split("_")[1]
            
            if action == "next":
                current_index = int(callback.data.split("_")[2])
                page = int(callback.data.split("_")[3])
                await show_next_order(callback, current_index, page)
            elif action == "prev":
                current_index = int(callback.data.split("_")[2])
                page = int(callback.data.split("_")[3])
                await show_previous_order(callback, current_index, page)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    async def show_order_details(message_or_callback, order, orders_data, index):
        """Show order details with navigation"""
        try:
            # Format order type
            order_type_emoji = "🔧" if order['type'] == 'service' else "🔌"
            order_type_text = "Texnik xizmat" if order['type'] == 'service' else "Ulanish"
            
            # Format status
            status_emoji = {
                'active': '🟡',
                'pending': '🟠', 
                'completed': '🟢',
                'cancelled': '🔴'
            }.get(order['status'], '⚪')
            
            status_text = {
                'active': 'Faol',
                'pending': 'Kutilmoqda',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }.get(order['status'], 'Noma\'lum')
            
            # Format date
            created_date = datetime.strptime(order['created_at'], '%Y-%m-%d %H:%M:%S')
            formatted_date = created_date.strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"{order_type_emoji} <b>{order_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {order['request_id']}\n"
                f"📅 <b>Sana:</b> {formatted_date}\n"
                f"🏛️ <b>Hudud:</b> {order['region']}\n"
                f"🏠 <b>Manzil:</b> {order['address']}\n"
                f"📝 <b>Tavsif:</b> {order['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"👨‍🔧 <b>Texnik:</b> Ahmad Karimov\n"
                f"⏰ <b>Taxminiy vaqt:</b> 2-3 kun\n"
                f"⚡ <b>Ustuvorlik:</b> Normal\n\n"
                f"📊 <b>Buyurtma #{index + 1} / {len(orders_data['orders'])}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_orders_navigation_keyboard(
                index, orders_data['page'], orders_data['total_pages'], 
                len(orders_data['orders']), order['id']
            )
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    async def show_next_order(callback: CallbackQuery, current_index: int, current_page: int):
        """Show next order"""
        try:
            orders_data = await get_user_orders(callback.from_user.id, page=current_page)
            
            if current_index + 1 < len(orders_data['orders']):
                # Next order on same page
                await show_order_details(callback, orders_data['orders'][current_index + 1], orders_data, current_index + 1)
            elif current_page < orders_data['total_pages']:
                # Next page
                next_page_data = await get_user_orders(callback.from_user.id, page=current_page + 1)
                await show_order_details(callback, next_page_data['orders'][0], next_page_data, 0)
            else:
                await callback.answer("Bu oxirgi buyurtma")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    async def show_previous_order(callback: CallbackQuery, current_index: int, current_page: int):
        """Show previous order"""
        try:
            if current_index > 0:
                # Previous order on same page
                orders_data = await get_user_orders(callback.from_user.id, page=current_page)
                await show_order_details(callback, orders_data['orders'][current_index - 1], orders_data, current_index - 1)
            elif current_page > 1:
                # Previous page
                prev_page_data = await get_user_orders(callback.from_user.id, page=current_page - 1)
                last_index = len(prev_page_data['orders']) - 1
                await show_order_details(callback, prev_page_data['orders'][last_index], prev_page_data, last_index)
            else:
                await callback.answer("Bu birinchi buyurtma")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

def get_orders_navigation_keyboard(current_index: int, current_page: int, total_pages: int, orders_on_page: int, order_id: int):
    """Create navigation keyboard for orders"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0 or current_page > 1:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data=f"order_prev_{current_index}_{current_page}"
        ))
    
    # Next button
    if current_index < orders_on_page - 1 or current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data=f"order_next_{current_index}_{current_page}"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifaclientorders", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
