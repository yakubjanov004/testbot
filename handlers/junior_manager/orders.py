"""
Junior Manager Orders - Simplified Implementation

This module handles junior manager orders functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.junior_manager_buttons import get_orders_keyboard, get_junior_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_junior_manager_orders(user_id: int):
    """Mock get junior manager orders"""
    return [
        {
            'id': 'ord_001_2024_01_15',
            'client_name': 'Aziz Karimov',
            'client_phone': '+998901234567',
            'order_type': 'connection',
            'status': 'pending',
            'description': 'Yangi internet ulanish',
            'address': 'Tashkent, Chorsu',
            'priority': 'high',
            'created_at': datetime.now(),
            'estimated_completion': '2-3 kun'
        },
        {
            'id': 'ord_002_2024_01_16',
            'client_name': 'Malika Toshmatova',
            'client_phone': '+998901234568',
            'order_type': 'technical_service',
            'status': 'in_progress',
            'description': 'Internet tezligi sekin',
            'address': 'Tashkent, Yunusabad',
            'priority': 'normal',
            'created_at': datetime.now(),
            'estimated_completion': '1 kun'
        },
        {
            'id': 'ord_003_2024_01_17',
            'client_name': 'Jahongir Azimov',
            'client_phone': '+998901234569',
            'order_type': 'tv_service',
            'status': 'completed',
            'description': 'TV signal muammosi',
            'address': 'Tashkent, Sergeli',
            'priority': 'low',
            'created_at': datetime.now(),
            'estimated_completion': 'Yakunlangan'
        }
    ]

def get_junior_manager_orders_router():
    """Router for junior manager orders functionality"""
    router = Router()

    @router.message(F.text.in_(["📋 Buyurtmalar", "📋 Заказы"]))
    async def view_orders(message: Message, state: FSMContext):
        """Junior manager view orders handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return
            
            lang = user.get('language', 'uz')
            
            # Get junior manager orders
            orders = await get_junior_manager_orders(message.from_user.id)
            
            if not orders:
                no_orders_text = (
                    "📭 Hozircha buyurtmalar yo'q."
                    if lang == 'uz' else
                    "📭 Пока нет заказов."
                )
                
                await message.answer(
                    text=no_orders_text,
                    reply_markup=get_junior_manager_back_keyboard(lang)
                )
                return
            
            # Show first order
            await show_order_details(message, orders[0], orders, 0)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_order_details(message_or_callback, order, orders, index):
        """Show order details with navigation"""
        try:
            # Format order type
            order_type_emoji = {
                'connection': '🔌',
                'technical_service': '🔧',
                'tv_service': '📺',
                'phone_service': '📞'
            }.get(order['order_type'], '📄')
            
            order_type_text = {
                'connection': 'Ulanish',
                'technical_service': 'Texnik xizmat',
                'tv_service': 'TV xizmat',
                'phone_service': 'Telefon xizmat'
            }.get(order['order_type'], 'Boshqa')
            
            # Format status
            status_emoji = {
                'pending': '🟡',
                'in_progress': '🟠',
                'completed': '🟢',
                'cancelled': '🔴'
            }.get(order['status'], '⚪')
            
            status_text = {
                'pending': 'Kutilmoqda',
                'in_progress': 'Jarayonda',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }.get(order['status'], 'Noma\'lum')
            
            # Format priority
            priority_emoji = {
                'high': '🔴',
                'normal': '🟡',
                'low': '🟢'
            }.get(order.get('priority', 'normal'), '🟡')
            
            priority_text = {
                'high': 'Yuqori',
                'normal': 'O\'rtacha',
                'low': 'Past'
            }.get(order.get('priority', 'normal'), 'O\'rtacha')
            
            # Format date
            created_date = order['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"{order_type_emoji} <b>{order_type_text} buyurtmasi - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Buyurtma ID:</b> {order['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {order['client_name']}\n"
                f"📞 <b>Telefon:</b> {order['client_phone']}\n"
                f"🏠 <b>Manzil:</b> {order['address']}\n"
                f"📝 <b>Tavsif:</b> {order['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n"
                f"⏰ <b>Taxminiy vaqt:</b> {order['estimated_completion']}\n\n"
                f"📊 <b>Buyurtma #{index + 1} / {len(orders)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_orders_navigation_keyboard(index, len(orders))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_prev_order")
    async def show_previous_order(callback: CallbackQuery, state: FSMContext):
        """Show previous order"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_order_index', 0)
            
            orders = await get_junior_manager_orders(callback.from_user.id)
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_order_index=new_index)
                await show_order_details(callback, orders[new_index], orders, new_index)
            else:
                await callback.answer("Bu birinchi buyurtma")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_next_order")
    async def show_next_order(callback: CallbackQuery, state: FSMContext):
        """Show next order"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_order_index', 0)
            
            orders = await get_junior_manager_orders(callback.from_user.id)
            
            if current_index < len(orders) - 1:
                new_index = current_index + 1
                await state.update_data(current_order_index=new_index)
                await show_order_details(callback, orders[new_index], orders, new_index)
            else:
                await callback.answer("Bu oxirgi buyurtma")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

def get_orders_navigation_keyboard(current_index: int, total_orders: int):
    """Create navigation keyboard for orders"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="jm_prev_order"
        ))
    
    # Next button
    if current_index < total_orders - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="jm_next_order"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 
