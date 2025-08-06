"""
Controller uchun monitoring va nazorat handleri
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

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

async def get_controller_monitoring_data(db, user_id: int):
    """Mock monitoring data"""
    return {
        'today_total': 25,
        'today_assigned': 18,
        'today_completed': 15,
        'active_requests': 7,
        'total_technicians': 12,
        'active_technicians': 8
    }

async def get_available_technicians(db):
    """Mock available technicians"""
    return [
        {
            'id': 1,
            'full_name': 'Technician 1',
            'phone_number': '+998901234567',
            'is_active': True,
            'active_requests': 2
        },
        {
            'id': 2,
            'full_name': 'Technician 2',
            'phone_number': '+998901234568',
            'is_active': True,
            'active_requests': 0
        },
        {
            'id': 3,
            'full_name': 'Technician 3',
            'phone_number': '+998901234569',
            'is_active': False,
            'active_requests': 5
        }
    ]

async def get_technician_performance(db):
    """Mock technician performance data"""
    return [
        {
            'id': 1,
            'full_name': 'Technician 1',
            'completed_orders': 15,
            'avg_rating': 4.5
        },
        {
            'id': 2,
            'full_name': 'Technician 2',
            'completed_orders': 12,
            'avg_rating': 4.8
        },
        {
            'id': 3,
            'full_name': 'Technician 3',
            'completed_orders': 8,
            'avg_rating': 4.2
        }
    ]

async def get_role_router(role: str):
    """Mock role router"""
    from aiogram import Router
    return Router()

async def send_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock send and track"""
    return await message_func(text, **kwargs)

async def edit_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock edit and track"""
    return await message_func(text, **kwargs)

# Mock bot and database
class MockBot:
    async def send_message(self, chat_id, text, **kwargs):
        print(f"MockBot: Sending message to {chat_id}: {text}")
        return True
    async def edit_message_text(self, chat_id, message_id, text, **kwargs):
        print(f"MockBot: Editing message {message_id} in {chat_id}: {text}")
        return True

class MockDB:
    async def acquire(self):
        return self
    async def fetchrow(self, query, *args):
        """Mock database fetchrow"""
        return {
            'total_today': 25,
            'completed_today': 15,
            'avg_processing_hours': 2.5,
            'total_week': 150,
            'avg_processing_hours_week': 2.8
        }

bot = MockBot()
bot.db = MockDB()

def get_controller_monitoring_router():
    """Get controller monitoring router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["📊 Monitoring"]))
    async def show_monitoring_dashboard(message: Message, state: FSMContext):
        """Monitoring dashboard ko'rsatish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await send_and_track(
                    message.answer,
                    "Sizda controller huquqi yo'q.",
                    user_id
                )
                return

            lang = user.get('language', 'uz')
        
            # Monitoring ma'lumotlarini olish
            monitoring_data = await get_controller_monitoring_data(bot.db, user['id'])
            
            dashboard_text = f"""
📊 <b>Controller Monitoring Dashboard</b>

📈 <b>Bugungi statistika:</b>
• Jami ko'rilgan: {monitoring_data['today_total']}
• Texniklarga tayinlangan: {monitoring_data['today_assigned']}
• Yakunlangan: {monitoring_data['today_completed']}

🔄 <b>Faol zayavkalar:</b>
• Kutilayotgan: {monitoring_data['active_requests']}

👨‍🔧 <b>Texniklar holati:</b>
• Jami texniklar: {monitoring_data['total_technicians']}
• Faol texniklar: {monitoring_data['active_technicians']}

⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""

            # Monitoring tugmalari
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="👨‍🔧 Texniklar holati",
                        callback_data="ctrl_monitor_technicians"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📈 Samaradorlik",
                        callback_data="ctrl_monitor_performance"
                    ),
                    InlineKeyboardButton(
                        text="⏱️ Vaqt tahlili",
                        callback_data="ctrl_monitor_time"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Yangilash",
                        callback_data="ctrl_refresh_monitoring"
                    )
                ]
            ])

            await send_and_track(
                message.answer,
                dashboard_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

        except Exception as e:
            print(f"Error in monitoring dashboard: {e}")
            error_text = "Monitoring ma'lumotlarini olishda xatolik"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.callback_query(F.data == "ctrl_monitor_technicians")
    async def monitor_technicians(callback: CallbackQuery):
        """Texniklar holatini monitoring qilish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return

            lang = user.get('language', 'uz')

            technicians = await get_available_technicians(bot.db)
            
            if not technicians:
                no_tech_text = "Texniklar topilmadi"
                await callback.answer(no_tech_text, show_alert=True)
                return

            tech_text = "👨‍🔧 <b>Texniklar holati:</b>\n\n"

            for tech in technicians[:10]:  # Maksimal 10 ta
                status_emoji = "🟢" if tech['is_active'] else "🔴"
                workload_emoji = "🟢" if tech['active_requests'] == 0 else "🟡" if tech['active_requests'] < 3 else "🔴"
                
                tech_text += (
                    f"{status_emoji} <b>{tech['full_name']}</b>\n"
                    f"   {workload_emoji} Faol zayavkalar: {tech['active_requests']}\n"
                    f"   📞 {tech.get('phone_number', 'N/A')}\n\n"
                )

            # Legend
            legend_text = (
                "\n🟢 - Faol/Bo'sh  🟡 - O'rtacha yuklangan  🔴 - Nofaol/Ko'p yuklangan"
            )
            tech_text += legend_text

            # Back tugmasi
            back_text = "◀️ Orqaga"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=back_text, callback_data="ctrl_back_to_monitoring")]
            ])

            await edit_and_track(
                callback.message.edit_text,
                tech_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            await callback.answer()

        except Exception as e:
            print(f"Error monitoring technicians: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_monitor_performance")
    async def monitor_performance(callback: CallbackQuery):
        """Samaradorlik monitoring"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return

            lang = user.get('language', 'uz')

            # Texniklar samaradorligini olish
            performance_data = await get_technician_performance(bot.db)
            
            perf_text = "📈 <b>Texniklar samaradorligi:</b>\n\n"

            if performance_data:
                for i, perf in enumerate(performance_data[:10], 1):
                    rating = float(perf.get('avg_rating') or 0)
                    completed = perf.get('completed_orders', 0)
                    
                    rating_emoji = "⭐" * min(int(rating), 5) if rating > 0 else "❌"
                    
                    perf_text += (
                        f"{i}. <b>{perf['full_name']}</b>\n"
                        f"   ✅ Bajarilgan: {completed}\n"
                        f"   {rating_emoji} Reyting: {rating:.1f}/5.0\n\n"
                    )
            else:
                no_data_text = "Ma'lumotlar yo'q"
                perf_text += no_data_text

            # Back tugmasi
            back_text = "◀️ Orqaga"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=back_text, callback_data="ctrl_back_to_monitoring")]
            ])

            await edit_and_track(
                callback.message.edit_text,
                perf_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            await callback.answer()

        except Exception as e:
            print(f"Error monitoring performance: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_monitor_time")
    async def monitor_time_analysis(callback: CallbackQuery):
        """Vaqt tahlili monitoring"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return

            lang = user.get('language', 'uz')

            # Vaqt statistikasini olish
            async with bot.db.acquire() as conn:
                # Bugungi zayavkalar
                today_stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_today,
                        AVG(EXTRACT(EPOCH FROM (updated_at - created_at))/3600) as avg_processing_hours,
                        COUNT(CASE WHEN current_status = 'technician_completed' THEN 1 END) as completed_today
                    FROM service_requests 
                    WHERE DATE(created_at) = CURRENT_DATE
                """)
                
                # Haftalik statistika
                week_stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_week,
                        AVG(EXTRACT(EPOCH FROM (updated_at - created_at))/3600) as avg_processing_hours_week
                    FROM service_requests 
                    WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
                """)

            time_text = f"""
⏱️ <b>Vaqt tahlili:</b>

📅 <b>Bugungi ko'rsatkichlar:</b>
• Jami zayavkalar: {today_stats['total_today'] if today_stats else 0}
• Bajarilgan: {today_stats['completed_today'] if today_stats else 0}
• O'rtacha ishlov berish: {today_stats['avg_processing_hours']:.1f if today_stats and today_stats['avg_processing_hours'] else 0} soat

📊 <b>Haftalik ko'rsatkichlar:</b>
• Jami zayavkalar: {week_stats['total_week'] if week_stats else 0}
• O'rtacha ishlov berish: {week_stats['avg_processing_hours_week']:.1f if week_stats and week_stats['avg_processing_hours_week'] else 0} soat

⏰ <b>Tahlil vaqti:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""

            # Back tugmasi
            back_text = "◀️ Orqaga"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=back_text, callback_data="ctrl_back_to_monitoring")]
            ])

            await edit_and_track(
                callback.message.edit_text,
                time_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            await callback.answer()

        except Exception as e:
            print(f"Error in time analysis: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_refresh_monitoring")
    async def refresh_monitoring(callback: CallbackQuery):
        """Monitoring ma'lumotlarini yangilash"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return

            lang = user.get('language', 'uz')

            # Monitoring ma'lumotlarini qayta olish
            monitoring_data = await get_controller_monitoring_data(bot.db, user['id'])
            
            dashboard_text = f"""
📊 <b>Controller Monitoring Dashboard</b>

📈 <b>Bugungi statistika:</b>
• Jami ko'rilgan: {monitoring_data['today_total']}
• Texniklarga tayinlangan: {monitoring_data['today_assigned']}
• Yakunlangan: {monitoring_data['today_completed']}

🔄 <b>Faol zayavkalar:</b>
• Kutilayotgan: {monitoring_data['active_requests']}

👨‍🔧 <b>Texniklar holati:</b>
• Jami texniklar: {monitoring_data['total_technicians']}
• Faol texniklar: {monitoring_data['active_technicians']}

⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""

            # Monitoring tugmalari
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="👨‍🔧 Texniklar holati",
                        callback_data="ctrl_monitor_technicians"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📈 Samaradorlik",
                        callback_data="ctrl_monitor_performance"
                    ),
                    InlineKeyboardButton(
                        text="⏱️ Vaqt tahlili",
                        callback_data="ctrl_monitor_time"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Yangilash",
                        callback_data="ctrl_refresh_monitoring"
                    )
                ]
            ])

            await edit_and_track(
                callback.message.edit_text,
                dashboard_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            refresh_msg = "Ma'lumotlar yangilandi"
            await callback.answer(refresh_msg)

        except Exception as e:
            print(f"Error refreshing monitoring: {e}")
            error_text = "Yangilashda xatolik"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_back_to_monitoring")
    async def back_to_monitoring(callback: CallbackQuery):
        """Monitoring dashboardga qaytish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return

            lang = user.get('language', 'uz')

            # Monitoring ma'lumotlarini olish
            monitoring_data = await get_controller_monitoring_data(bot.db, user['id'])
            
            dashboard_text = f"""
📊 <b>Controller Monitoring Dashboard</b>

📈 <b>Bugungi statistika:</b>
• Jami ko'rilgan: {monitoring_data['today_total']}
• Texniklarga tayinlangan: {monitoring_data['today_assigned']}
• Yakunlangan: {monitoring_data['today_completed']}

🔄 <b>Faol zayavkalar:</b>
• Kutilayotgan: {monitoring_data['active_requests']}

👨‍🔧 <b>Texniklar holati:</b>
• Jami texniklar: {monitoring_data['total_technicians']}
• Faol texniklar: {monitoring_data['active_technicians']}

⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""

            # Monitoring tugmalari
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="👨‍🔧 Texniklar holati",
                        callback_data="ctrl_monitor_technicians"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📈 Samaradorlik",
                        callback_data="ctrl_monitor_performance"
                    ),
                    InlineKeyboardButton(
                        text="⏱️ Vaqt tahlili",
                        callback_data="ctrl_monitor_time"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Yangilash",
                        callback_data="ctrl_refresh_monitoring"
                    )
                ]
            ])

            await edit_and_track(
                callback.message.edit_text,
                dashboard_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            await callback.answer()

        except Exception as e:
            print(f"Error returning to monitoring: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    return router