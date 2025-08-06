"""
Manager Notifications Handler - Simplified Implementation

This module handles manager notifications functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_notifications_keyboard, get_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_manager_notifications(user_id: int):
    """Mock get manager notifications"""
    return [
        {
            'id': 1,
            'type': 'new_application',
            'title': 'Yangi ariza',
            'message': 'Aziz Karimov tomonidan yangi ulanish arizasi yuborildi',
            'created_at': datetime.now(),
            'is_read': False,
            'priority': 'high'
        },
        {
            'id': 2,
            'type': 'technician_assigned',
            'title': 'Texnik tayinlandi',
            'message': 'Ahmad Karimov TX_12345678 arizasiga tayinlandi',
            'created_at': datetime.now(),
            'is_read': True,
            'priority': 'normal'
        },
        {
            'id': 3,
            'type': 'application_completed',
            'title': 'Ariza bajarildi',
            'message': 'TX_87654321 arizasi muvaffaqiyatli yakunlandi',
            'created_at': datetime.now(),
            'is_read': False,
            'priority': 'low'
        }
    ]

def get_manager_notifications_router():
    """Router for notifications functionality"""
    router = Router()

    @router.message(F.text.in_(["🔔 Bildirishnomalar", "🔔 Уведомления"]))
    async def view_notifications(message: Message, state: FSMContext):
        """Manager view notifications handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            
            # Get notifications
            notifications = await get_manager_notifications(message.from_user.id)
            
            if not notifications:
                no_notifications_text = (
                    "📭 Hozircha bildirishnomalar yo'q."
                    if lang == 'uz' else
                    "📭 Пока нет уведомлений."
                )
                
                await message.answer(
                    text=no_notifications_text,
                    reply_markup=get_manager_back_keyboard(lang)
                )
                return
            
            # Show first notification
            await show_notification_details(message, notifications[0], notifications, 0)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_notification_details(message_or_callback, notification, notifications, index):
        """Show notification details with navigation"""
        try:
            # Format notification type
            type_emoji = {
                'new_application': '🆕',
                'technician_assigned': '👨‍🔧',
                'application_completed': '✅',
                'urgent': '🚨',
                'reminder': '⏰'
            }.get(notification['type'], '📢')
            
            type_text = {
                'new_application': 'Yangi ariza',
                'technician_assigned': 'Texnik tayinlandi',
                'application_completed': 'Ariza bajarildi',
                'urgent': 'Shoshilinch',
                'reminder': 'Eslatma'
            }.get(notification['type'], 'Boshqa')
            
            # Format priority
            priority_emoji = {
                'high': '🔴',
                'normal': '🟡',
                'low': '🟢'
            }.get(notification.get('priority', 'normal'), '🟡')
            
            priority_text = {
                'high': 'Yuqori',
                'normal': 'O\'rtacha',
                'low': 'Past'
            }.get(notification.get('priority', 'normal'), 'O\'rtacha')
            
            # Format date
            created_date = notification['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # Format read status
            read_status = "✅ O'qilgan" if notification['is_read'] else "❌ O'qilmagan"
            
            # To'liq ma'lumot
            text = (
                f"{type_emoji} <b>{type_text} - To'liq ma'lumot</b>\n\n"
                f"📋 <b>Sarlavha:</b> {notification['title']}\n"
                f"📝 <b>Xabar:</b> {notification['message']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n"
                f"📊 <b>Holat:</b> {read_status}\n"
                f"🆔 <b>ID:</b> {notification['id']}\n\n"
                f"📊 <b>Bildirishnoma #{index + 1} / {len(notifications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_notifications_navigation_keyboard(index, len(notifications))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_prev_notification")
    async def show_previous_notification(callback: CallbackQuery, state: FSMContext):
        """Show previous notification"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_notification_index', 0)
            
            notifications = await get_manager_notifications(callback.from_user.id)
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_notification_index=new_index)
                await show_notification_details(callback, notifications[new_index], notifications, new_index)
            else:
                await callback.answer("Bu birinchi bildirishnoma")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_next_notification")
    async def show_next_notification(callback: CallbackQuery, state: FSMContext):
        """Show next notification"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_notification_index', 0)
            
            notifications = await get_manager_notifications(callback.from_user.id)
            
            if current_index < len(notifications) - 1:
                new_index = current_index + 1
                await state.update_data(current_notification_index=new_index)
                await show_notification_details(callback, notifications[new_index], notifications, new_index)
            else:
                await callback.answer("Bu oxirgi bildirishnoma")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

def get_notifications_navigation_keyboard(current_index: int, total_notifications: int):
    """Create navigation keyboard for notifications"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="mgr_prev_notification"
        ))
    
    # Next button
    if current_index < total_notifications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="mgr_next_notification"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 

 