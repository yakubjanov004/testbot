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
from keyboards.controllers_buttons import get_realtime_monitoring_keyboard

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
        'system_uptime': '99.8%',
        'active_applications': 18,
        'pending_applications': 5,
        'in_progress_applications': 12,
        'completed_applications': 8,
        'available_technicians': 4,
        'busy_technicians': 6,
        'recent_activities': [
            {
                'id': 1,
                'type': 'order_created',
                'description': 'Yangi buyurtma yaratildi',
                'time': datetime.now() - timedelta(minutes=5),
                'user': 'Test Client',
                'priority': 'normal'
            },
            {
                'id': 2,
                'type': 'order_assigned',
                'description': 'Buyurtma texnikka tayinlandi',
                'time': datetime.now() - timedelta(minutes=12),
                'user': 'Aziz Karimov',
                'priority': 'high'
            },
            {
                'id': 3,
                'type': 'order_completed',
                'description': 'Buyurtma bajarildi',
                'time': datetime.now() - timedelta(minutes=25),
                'user': 'Malika Yusupova',
                'priority': 'normal'
            },
            {
                'id': 4,
                'type': 'technician_assigned',
                'description': 'Texnik tayinlandi',
                'time': datetime.now() - timedelta(minutes=35),
                'user': 'Umar Azimov',
                'priority': 'high'
            },
            {
                'id': 5,
                'type': 'application_urgent',
                'description': 'Shoshilinch ariza yaratildi',
                'time': datetime.now() - timedelta(minutes=45),
                'user': 'Dilfuza Karimova',
                'priority': 'urgent'
            }
        ],
        'system_alerts': [
            {
                'id': 1,
                'type': 'warning',
                'message': 'Tizim yuklama 85% ga yetdi',
                'time': datetime.now() - timedelta(minutes=10)
            },
            {
                'id': 2,
                'type': 'info',
                'message': 'Yangi texnik qo\'shildi',
                'time': datetime.now() - timedelta(minutes=30)
            }
        ],
        'performance_metrics': {
            'response_time_avg': '1.8 soat',
            'completion_rate': '92%',
            'satisfaction_score': '4.7/5',
            'active_sessions': 45
        }
    }

async def get_detailed_realtime_data():
    """Mock get detailed real-time data"""
    return {
        'system_overview': {
            'total_requests': 156,
            'active_requests': 23,
            'completed_today': 18,
            'pending_requests': 7,
            'urgent_requests': 3
        },
        'technician_status': {
            'total_technicians': 12,
            'available_technicians': 5,
            'busy_technicians': 4,
            'offline_technicians': 3,
            'avg_workload': '2.3 requests'
        },
        'performance_metrics': {
            'avg_response_time': '1.8 soat',
            'avg_completion_time': '3.2 soat',
            'satisfaction_rate': '94%',
            'system_uptime': '99.8%'
        },
        'recent_activities': [
            {
                'id': 1,
                'type': 'new_application',
                'description': 'Yangi ulanish arizasi',
                'time': datetime.now() - timedelta(minutes=5),
                'user': 'Aziz Karimov',
                'priority': 'high',
                'status': 'in_progress'
            },
            {
                'id': 2,
                'type': 'technician_assigned',
                'description': 'Texnik tayinlandi',
                'time': datetime.now() - timedelta(minutes=12),
                'user': 'Umar Azimov',
                'priority': 'normal',
                'status': 'assigned'
            },
            {
                'id': 3,
                'type': 'application_completed',
                'description': 'Ariza bajarildi',
                'time': datetime.now() - timedelta(minutes=25),
                'user': 'Malika Yusupova',
                'priority': 'normal',
                'status': 'completed'
            },
            {
                'id': 4,
                'type': 'application_cancelled',
                'description': 'Ariza bekor qilindi',
                'time': datetime.now() - timedelta(minutes=35),
                'user': 'Jasur Rahimov',
                'priority': 'low',
                'status': 'cancelled'
            },
            {
                'id': 5,
                'type': 'urgent_request',
                'description': 'Shoshilinch ariza',
                'time': datetime.now() - timedelta(minutes=45),
                'user': 'Dilfuza Karimova',
                'priority': 'urgent',
                'status': 'urgent'
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
                "Kerakli bo'limni tanlang:"
            )
            
            keyboard = get_realtime_monitoring_keyboard(lang)
            
            await message.answer(
                monitoring_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in view_realtime_monitoring: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data == "ctrl_realtime_status")
    async def view_live_status(callback: CallbackQuery, state: FSMContext):
        """View live system status"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            realtime_data = await get_realtime_data()
            
            status_text = (
                "🟢 <b>Jonli tizim holati</b>\n\n"
                "📊 <b>Umumiy ma'lumot:</b>\n"
                f"• Jami arizalar: {realtime_data['active_applications'] + realtime_data['completed_applications']}\n"
                f"• Faol arizalar: {realtime_data['active_applications']}\n"
                f"• Bugun bajarilgan: {realtime_data['completed_applications']}\n\n"
                f"👨‍🔧 <b>Texniklar holati:</b>\n"
                f"• Jami texniklar: {realtime_data['total_technicians']}\n"
                f"• Mavjud texniklar: {realtime_data['available_technicians']}\n"
                f"• Band texniklar: {realtime_data['busy_technicians']}\n\n"
                f"📈 <b>Samaradorlik:</b>\n"
                f"• O'rtacha javob vaqti: {realtime_data['avg_response_time']}\n"
                f"• Tizim ishlashi: {realtime_data['system_uptime']}\n"
                f"• Mijozlar mamnuniyati: {realtime_data['performance_metrics']['satisfaction_score']}\n\n"
                f"⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Yangilash", callback_data="ctrl_refresh_status"),
                    InlineKeyboardButton(text="📊 Batafsil", callback_data="ctrl_detailed_status")
                ],
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ctrl_back_to_realtime")
                ]
            ])
            
            await callback.message.edit_text(status_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_realtime_activities")
    async def view_recent_activities(callback: CallbackQuery, state: FSMContext):
        """View recent activities"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            realtime_data = await get_realtime_data()
            
            activities_text = (
                "📋 <b>So'nggi faolliklar</b>\n\n"
            )
            
            # Add recent activities
            for i, activity in enumerate(realtime_data['recent_activities'], 1):
                priority_emoji = {
                    'urgent': '🔴',
                    'high': '🟠',
                    'normal': '🟡',
                    'low': '🟢'
                }.get(activity.get('priority', 'normal'), '⚪')
                
                activity_type_emoji = {
                    'new_application': '📝',
                    'technician_assigned': '👨‍🔧',
                    'application_completed': '✅',
                    'application_cancelled': '❌',
                    'order_created': '📋',
                    'order_assigned': '👨‍🔧',
                    'order_completed': '✅',
                    'application_urgent': '🚨'
                }.get(activity['type'], '📄')
                
                time_diff = datetime.now() - activity['time']
                if time_diff.total_seconds() < 3600:  # Less than 1 hour
                    time_text = f"{int(time_diff.total_seconds() // 60)} daqiqa oldin"
                elif time_diff.total_seconds() < 86400:  # Less than 1 day
                    time_text = f"{int(time_diff.total_seconds() // 3600)} soat oldin"
                else:
                    time_text = f"{int(time_diff.total_seconds() // 86400)} kun oldin"
                
                activities_text += (
                    f"{i}. {activity_type_emoji} {activity['description']}\n"
                    f"   {priority_emoji} {activity['user']} - {time_text}\n\n"
                )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Yangilash", callback_data="ctrl_refresh_activities"),
                    InlineKeyboardButton(text="📊 Batafsil", callback_data="ctrl_detailed_activities")
                ],
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ctrl_back_to_realtime")
                ]
            ])
            
            await callback.message.edit_text(activities_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_realtime_alerts")
    async def view_system_alerts(callback: CallbackQuery, state: FSMContext):
        """View system alerts"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            realtime_data = await get_realtime_data()
            
            alerts_text = (
                "🚨 <b>Tizim ogohlantirishlari</b>\n\n"
            )
            
            if realtime_data.get('system_alerts'):
                for i, alert in enumerate(realtime_data['system_alerts'], 1):
                    alert_emoji = {
                        'warning': '⚠️',
                        'error': '❌',
                        'info': 'ℹ️',
                        'success': '✅'
                    }.get(alert['type'], '📢')
                    
                    time_diff = datetime.now() - alert['time']
                    if time_diff.total_seconds() < 3600:
                        time_text = f"{int(time_diff.total_seconds() // 60)} daqiqa oldin"
                    else:
                        time_text = f"{int(time_diff.total_seconds() // 3600)} soat oldin"
                    
                    alerts_text += (
                        f"{i}. {alert_emoji} {alert['message']}\n"
                        f"   ⏰ {time_text}\n\n"
                    )
            else:
                alerts_text += "✅ Hozircha ogohlantirishlar yo'q\n\n"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Yangilash", callback_data="ctrl_refresh_alerts"),
                    InlineKeyboardButton(text="📊 Batafsil", callback_data="ctrl_detailed_alerts")
                ],
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ctrl_back_to_realtime")
                ]
            ])
            
            await callback.message.edit_text(alerts_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_realtime_performance")
    async def view_performance_metrics(callback: CallbackQuery, state: FSMContext):
        """View performance metrics"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            realtime_data = await get_realtime_data()
            
            performance_text = (
                "📈 <b>Samaradorlik ko'rsatkichlari</b>\n\n"
                "⏰ <b>Vaqt ko'rsatkichlari:</b>\n"
                f"• O'rtacha javob vaqti: {realtime_data['avg_response_time']}\n"
                f"• Tizim ishlashi: {realtime_data['system_uptime']}\n\n"
                "📊 <b>Bajarish ko'rsatkichlari:</b>\n"
                f"• Mijozlar mamnuniyati: {realtime_data['performance_metrics']['satisfaction_score']}\n"
                f"• Faol sessiyalar: {realtime_data['performance_metrics']['active_sessions']}\n"
                f"• Bajarish darajasi: {realtime_data['performance_metrics']['completion_rate']}\n\n"
                "👨‍🔧 <b>Texniklar samaradorligi:</b>\n"
                f"• Faol texniklar: {realtime_data['active_technicians']}/{realtime_data['total_technicians']}\n"
                f"• O'rtacha ish yuki: {realtime_data['performance_metrics']['response_time_avg']}\n\n"
                f"⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Yangilash", callback_data="ctrl_refresh_performance"),
                    InlineKeyboardButton(text="📊 Batafsil", callback_data="ctrl_detailed_performance")
                ],
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ctrl_back_to_realtime")
                ]
            ])
            
            await callback.message.edit_text(performance_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_back_to_realtime")
    async def back_to_realtime_monitoring(callback: CallbackQuery, state: FSMContext):
        """Back to real-time monitoring menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get realtime data
            realtime_data = await get_realtime_data()
            
            monitoring_text = (
                "🕐 <b>Real vaqtda kuzatish</b>\n\n"
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
                "Kerakli bo'limni tanlang:"
            )
            
            keyboard = get_realtime_monitoring_keyboard(lang)
            
            await callback.message.edit_text(
                text=monitoring_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    # Refresh handlers
    @router.callback_query(F.data.startswith("ctrl_refresh_"))
    async def refresh_realtime_data(callback: CallbackQuery, state: FSMContext):
        """Refresh real-time data"""
        try:
            await callback.answer("🔄 Yangilandi")
            
            # Determine which section to refresh based on callback data
            refresh_type = callback.data.replace("ctrl_refresh_", "")
            
            if refresh_type == "status":
                await view_live_status(callback, state)
            elif refresh_type == "activities":
                await view_recent_activities(callback, state)
            elif refresh_type == "alerts":
                await view_system_alerts(callback, state)
            elif refresh_type == "performance":
                await view_performance_metrics(callback, state)
            
        except Exception as e:
            await callback.answer("❌ Yangilashda xatolik")

    # Detailed view handlers
    @router.callback_query(F.data.startswith("ctrl_detailed_"))
    async def view_detailed_data(callback: CallbackQuery, state: FSMContext):
        """View detailed data"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            detailed_data = await get_detailed_realtime_data()
            
            detail_type = callback.data.replace("ctrl_detailed_", "")
            
            if detail_type == "status":
                detailed_text = (
                    "📊 <b>Batafsil tizim holati</b>\n\n"
                    "📈 <b>Umumiy ko'rsatkichlar:</b>\n"
                    f"• Jami arizalar: {detailed_data['system_overview']['total_requests']}\n"
                    f"• Faol arizalar: {detailed_data['system_overview']['active_requests']}\n"
                    f"• Bugun bajarilgan: {detailed_data['system_overview']['completed_today']}\n"
                    f"• Kutilmoqda: {detailed_data['system_overview']['pending_requests']}\n"
                    f"• Shoshilinch: {detailed_data['system_overview']['urgent_requests']}\n\n"
                    "👨‍🔧 <b>Texniklar holati:</b>\n"
                    f"• Jami texniklar: {detailed_data['technician_status']['total_technicians']}\n"
                    f"• Mavjud texniklar: {detailed_data['technician_status']['available_technicians']}\n"
                    f"• Band texniklar: {detailed_data['technician_status']['busy_technicians']}\n"
                    f"• Oflayn texniklar: {detailed_data['technician_status']['offline_technicians']}\n"
                    f"• O'rtacha ish yuki: {detailed_data['technician_status']['avg_workload']}\n\n"
                    "📈 <b>Samaradorlik:</b>\n"
                    f"• O'rtacha javob vaqti: {detailed_data['performance_metrics']['avg_response_time']}\n"
                    f"• O'rtacha bajarish vaqti: {detailed_data['performance_metrics']['avg_completion_time']}\n"
                    f"• Mijozlar mamnuniyati: {detailed_data['performance_metrics']['satisfaction_rate']}\n"
                    f"• Tizim ishlashi: {detailed_data['performance_metrics']['system_uptime']}"
                )
            else:
                detailed_text = "📊 Batafsil ma'lumotlar ko'rsatilmoqda..."
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ctrl_back_to_realtime")
                ]
            ])
            
            await callback.message.edit_text(detailed_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router 