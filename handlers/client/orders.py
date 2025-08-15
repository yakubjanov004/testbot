"""
Client Orders Handler - Simplified Implementation

This module handles viewing client orders with pagination.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from states.client_states import OrderStates
from filters.role_filter import RoleFilter
from keyboards.client_buttons import (
    get_orders_menu_keyboard,
    get_back_to_orders_menu_keyboard,
    get_client_orders_navigation_keyboard
)
from utils.db import get_user_by_telegram_id, get_user_orders, get_order_details


def get_orders_router():
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📋 Mening buyurtmalarim"]))
    async def show_my_orders(message: Message, state: FSMContext):
        """Show user orders"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.")
                return
            
            # Get user orders
            orders_data = await get_user_orders(message.from_user.id, page=1)
            
            if not orders_data['orders']:
                await message.answer("📋 Sizda hali buyurtmalar mavjud emas.")
                return
            
            # Show first order
            await show_order_details(message, orders_data['orders'][0], orders_data, 0)
            
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
                current_page = int(data[3])
                await show_next_order(callback, current_index, current_page)
            elif action == "prev":
                current_index = int(data[2])
                current_page = int(data[3])
                await show_previous_order(callback, current_index, current_page)
            elif action == "details":
                order_id = int(data[2])
                order = await get_order_details(order_id)
                if order:
                    await show_order_details(callback, order, None, 0)
                else:
                    await callback.answer("Topilmadi", show_alert=True)
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

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
            created_date = datetime.strptime(order['created_at'], '%Y-%m-%d %H:%M:%S') if isinstance(order['created_at'], str) else order['created_at']
            formatted_date = created_date.strftime('%d.%m.%Y %H:%M') if isinstance(created_date, datetime) else '-'
            
            # To'liq ma'lumot
            text = (
                f"{order_type_emoji} <b>{order_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {order['request_id']}\n"
                f"📅 <b>Sana:</b> {formatted_date}\n"
                f"🏛️ <b>Hudud:</b> {order.get('region','')}\n"
                f"🏠 <b>Manzil:</b> {order.get('address','')}\n"
                f"📝 <b>Tavsif:</b> {order.get('description','')}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"👨‍🔧 <b>Texnik:</b> {order.get('assigned_to','Tayinlanmagan') if isinstance(order, dict) else 'Tayinlanmagan'}\n"
                f"⏰ <b>Taxminiy vaqt:</b> 2-3 kun\n"
                f"⚡ <b>Ustuvorlik:</b> Normal\n\n"
                f"📊 <b>Buyurtma #{(index + 1) if orders_data else 1} / {(len(orders_data['orders'])) if orders_data else 1}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_client_orders_navigation_keyboard(
                index if orders_data else 0,
                (orders_data['page'] if orders_data else 1),
                (orders_data['total_pages'] if orders_data else 1), 
                (len(orders_data['orders']) if orders_data else 1), order['id']
            ) if orders_data else get_client_orders_navigation_keyboard(0, 1, 1, 1, order['id'])
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    async def show_next_order(callback: CallbackQuery, current_index: int, current_page: int, order_id: int = None):
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

    async def show_previous_order(callback: CallbackQuery, current_index: int, current_page: int, order_id: int = None):
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