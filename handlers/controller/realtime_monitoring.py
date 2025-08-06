"""
Controller Real-time Monitoring Handler
Manages real-time monitoring for controller
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from filters.role_filter import RoleFilter

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
    """Mock get real-time data"""
    return {
        'active_orders': 25,
        'pending_orders': 8,
        'completed_today': 15,
        'active_technicians': 6,
        'total_technicians': 10,
        'avg_response_time': '1.8 soat',
        'system_status': 'online',
        'recent_activities': [
            {
                'id': 1,
                'type': 'order_created',
                'description': 'Yangi buyurtma yaratildi',
                'time': datetime.now() - timedelta(minutes=5),
                'user': 'Test Client'
            },
            {
                'id': 2,
                'type': 'order_assigned',
                'description': 'Buyurtma texnikka tayinlandi',
                'time': datetime.now() - timedelta(minutes=12),
                'user': 'Aziz Karimov'
            },
            {
                'id': 3,
                'type': 'order_completed',
                'description': 'Buyurtma bajarildi',
                'time': datetime.now() - timedelta(minutes=25),
                'user': 'Malika Yusupova'
            }
        ]
    }

def get_realtime_monitoring_router():
    """Get controller real-time monitoring router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🕐 Real vaqtda kuzatish", "📡 Мониторинг в реальном времени"]))
    async def view_realtime_monitoring(message: Message, state: FSMContext):
        """Handle real-time monitoring view"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            realtime_data = await get_realtime_data()
            
            monitoring_text = (
                "🕐 <b>Real vaqtda kuzatish</b>\n\n"
                "📊 <b>Joriy holat:</b>\n"
                f"• Faol buyurtmalar: {realtime_data['active_orders']}\n"
                f"• Kutilayotgan: {realtime_data['pending_orders']}\n"
                f"• Bugun bajarilgan: {realtime_data['completed_today']}\n"
                f"• Faol texniklar: {realtime_data['active_technicians']}/{realtime_data['total_technicians']}\n"
                f"• O'rtacha javob vaqti: {realtime_data['avg_response_time']}\n\n"
                f"🟢 <b>Tizim holati:</b> {realtime_data['system_status'].title()}\n\n"
                "Kerakli bo'limni tanlang:"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="📊 Batafsil statistika", callback_data="view_detailed_realtime"),
                    InlineKeyboardButton(text="⚡ So'nggi faoliyatlar", callback_data="view_recent_activities")
                ],
                [
                    InlineKeyboardButton(text="🔄 Yangilash", callback_data="refresh_realtime"),
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_monitoring")
                ]
            ])
            
            await message.answer(
                monitoring_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in view_realtime_monitoring: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

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