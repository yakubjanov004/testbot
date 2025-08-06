"""
Controller Realtime Monitoring - Simplified Implementation

This module handles controller realtime monitoring functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.controller_buttons import get_realtime_monitoring_keyboard, get_controller_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_realtime_data():
    """Mock get realtime data"""
    return {
        'active_applications': 25,
        'pending_applications': 8,
        'in_progress_applications': 12,
        'completed_applications': 5,
        'active_technicians': 15,
        'available_technicians': 8,
        'busy_technicians': 7,
        'avg_response_time': '15 daqiqa',
        'system_uptime': '99.8%',
        'recent_activities': [
            {
                'type': 'new_application',
                'description': 'Yangi internet ulanish arizasi',
                'time': '2 daqiqa oldin',
                'priority': 'high'
            },
            {
                'type': 'technician_assigned',
                'description': 'Texnik tayinlandi - Ariza #12345',
                'time': '5 daqiqa oldin',
                'priority': 'normal'
            },
            {
                'type': 'application_completed',
                'description': 'Ariza bajarildi - #12340',
                'time': '10 daqiqa oldin',
                'priority': 'low'
            }
        ]
    }

def get_realtime_monitoring_router():
    """Router for realtime monitoring functionality"""
    router = Router()

    @router.message(F.text.in_(["📡 Real vaqtda kuzatish", "📡 Мониторинг в реальном времени"]))
    async def view_realtime_monitoring(message: Message, state: FSMContext):
        """Controller view realtime monitoring handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            
            # Get realtime data
            realtime_data = await get_realtime_data()
            
            monitoring_text = (
                "📡 <b>Real vaqtda kuzatish - To'liq ma'lumot</b>\n\n"
                "📊 <b>Joriy holat:</b>\n"
                f"• Faol arizalar: {realtime_data['active_applications']}\n"
                f"• Kutilmoqda: {realtime_data['pending_applications']}\n"
                f"• Jarayonda: {realtime_data['in_progress_applications']}\n"
                f"• Bajarilgan: {realtime_data['completed_applications']}\n\n"
                f"👨‍🔧 <b>Texniklar:</b>\n"
                f"• Faol texniklar: {realtime_data['active_technicians']}\n"
                f"• Mavjud texniklar: {realtime_data['available_technicians']}\n"
                f"• Band texniklar: {realtime_data['busy_technicians']}\n\n"
                f"⏰ <b>O'rtacha javob vaqti:</b> {realtime_data['avg_response_time']}\n"
                f"🖥️ <b>Tizim ishlashi:</b> {realtime_data['system_uptime']}\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "📡 <b>Мониторинг в реальном времени - Полная информация</b>\n\n"
                "📊 <b>Текущее состояние:</b>\n"
                f"• Активные заявки: {realtime_data['active_applications']}\n"
                f"• Ожидающие: {realtime_data['pending_applications']}\n"
                f"• В процессе: {realtime_data['in_progress_applications']}\n"
                f"• Завершенные: {realtime_data['completed_applications']}\n\n"
                f"👨‍🔧 <b>Техники:</b>\n"
                f"• Активные техники: {realtime_data['active_technicians']}\n"
                f"• Доступные техники: {realtime_data['available_technicians']}\n"
                f"• Занятые техники: {realtime_data['busy_technicians']}\n\n"
                f"⏰ <b>Среднее время ответа:</b> {realtime_data['avg_response_time']}\n"
                f"🖥️ <b>Работа системы:</b> {realtime_data['system_uptime']}\n\n"
                "Выберите один из разделов ниже:"
            )
            
            sent_message = await message.answer(
                text=monitoring_text,
                reply_markup=get_realtime_monitoring_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_recent_activities")
    async def view_recent_activities(callback: CallbackQuery, state: FSMContext):
        """View recent activities"""
        try:
            await callback.answer()
            
            # Get realtime data
            realtime_data = await get_realtime_data()
            
            activities_text = (
                "📋 <b>So'nggi faolliklar - To'liq ma'lumot</b>\n\n"
            )
            
            # Add recent activities
            for i, activity in enumerate(realtime_data['recent_activities'], 1):
                priority_emoji = {
                    'high': '🔴',
                    'normal': '🟡',
                    'low': '🟢'
                }.get(activity['priority'], '⚪')
                
                activity_type_emoji = {
                    'new_application': '📝',
                    'technician_assigned': '👨‍🔧',
                    'application_completed': '✅',
                    'application_cancelled': '❌'
                }.get(activity['type'], '📄')
                
                activities_text += (
                    f"{i}. {activity_type_emoji} {activity['description']}\n"
                    f"   {priority_emoji} {activity['time']}\n\n"
                )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_monitoring")]
            ])
            
            await callback.message.edit_text(activities_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_monitoring")
    async def back_to_monitoring(callback: CallbackQuery, state: FSMContext):
        """Back to monitoring menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get realtime data
            realtime_data = await get_realtime_data()
            
            monitoring_text = (
                "📡 <b>Real vaqtda kuzatish - To'liq ma'lumot</b>\n\n"
                "📊 <b>Joriy holat:</b>\n"
                f"• Faol arizalar: {realtime_data['active_applications']}\n"
                f"• Kutilmoqda: {realtime_data['pending_applications']}\n"
                f"• Jarayonda: {realtime_data['in_progress_applications']}\n"
                f"• Bajarilgan: {realtime_data['completed_applications']}\n\n"
                f"👨‍🔧 <b>Texniklar:</b>\n"
                f"• Faol texniklar: {realtime_data['active_technicians']}\n"
                f"• Mavjud texniklar: {realtime_data['available_technicians']}\n"
                f"• Band texniklar: {realtime_data['busy_technicians']}\n\n"
                f"⏰ <b>O'rtacha javob vaqti:</b> {realtime_data['avg_response_time']}\n"
                f"🖥️ <b>Tizim ishlashi:</b> {realtime_data['system_uptime']}\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "📡 <b>Мониторинг в реальном времени - Полная информация</b>\n\n"
                "📊 <b>Текущее состояние:</b>\n"
                f"• Активные заявки: {realtime_data['active_applications']}\n"
                f"• Ожидающие: {realtime_data['pending_applications']}\n"
                f"• В процессе: {realtime_data['in_progress_applications']}\n"
                f"• Завершенные: {realtime_data['completed_applications']}\n\n"
                f"👨‍🔧 <b>Техники:</b>\n"
                f"• Активные техники: {realtime_data['active_technicians']}\n"
                f"• Доступные техники: {realtime_data['available_technicians']}\n"
                f"• Занятые техники: {realtime_data['busy_technicians']}\n\n"
                f"⏰ <b>Среднее время ответа:</b> {realtime_data['avg_response_time']}\n"
                f"🖥️ <b>Работа системы:</b> {realtime_data['system_uptime']}\n\n"
                "Выберите один из разделов ниже:"
            )
            
            await callback.message.edit_text(
                text=monitoring_text,
                reply_markup=get_realtime_monitoring_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router 