"""
Junior Manager Workflow Management Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun workflow boshqaruvi funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter
from keyboards.junior_manager_buttons import (
    get_workflow_management_menu,
    get_application_tracking_menu,
    get_task_monitoring_menu
)

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

async def get_junior_manager_dashboard_stats(junior_manager_id: int):
    """Mock dashboard statistics"""
    return {
        'applications': {
            'total_applications': 150,
            'completed_applications': 120,
            'pending_applications': 30,
            'today_applications': 5
        },
        'clients': {
            'total_clients_served': 80
        }
    }

async def get_junior_manager_applications(junior_manager_id: int, limit: int = 50, status: str = None):
    """Mock junior manager applications"""
    from datetime import datetime
    applications = [
        {
            'id': 1,
            'client_name': 'Aziz Karimov',
            'client_phone': '+998901234567',
            'address': 'Tashkent, Chorsu',
            'description': 'Internet ulanish arizasi',
            'priority': 'medium',
            'status': 'new',
            'created_at': datetime.now()
        },
        {
            'id': 2,
            'client_name': 'Malika Toshmatova',
            'client_phone': '+998901234568',
            'address': 'Tashkent, Yunusabad',
            'description': 'TV signal muammosi',
            'priority': 'high',
            'status': 'in_progress',
            'created_at': datetime.now()
        },
        {
            'id': 3,
            'client_name': 'Jahongir Karimov',
            'client_phone': '+998901234569',
            'address': 'Tashkent, Sergeli',
            'description': 'Internet tezligi sekin',
            'priority': 'low',
            'status': 'completed',
            'created_at': datetime.now()
        }
    ]
    
    if status:
        return [app for app in applications if app['status'] == status]
    return applications[:limit]

async def get_junior_manager_workflow_metrics(junior_manager_id: int, days: int = 7):
    """Mock workflow metrics"""
    return {
        'daily_applications': 5,
        'weekly_applications': 25,
        'completion_rate': 85.5,
        'avg_processing_time': 2.5,
        'total_applications': 150,
        'completed_applications': 120
    }

async def update_application_status_as_junior_manager(application_id: int, status: str):
    """Mock update application status"""
    return True

# Mock keyboard functions
def get_workflow_management_menu(lang: str = 'uz'):
    """Mock workflow management menu keyboard"""
    from keyboards.junior_manager_buttons import get_workflow_management_menu as _k
    return _k(lang)

def get_application_tracking_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Mock application tracking menu keyboard"""
    from keyboards.junior_manager_buttons import get_application_tracking_menu as _k
    return _k(lang)

def get_task_monitoring_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Mock task monitoring menu keyboard"""
    from keyboards.junior_manager_buttons import get_task_monitoring_menu as _k
    return _k(lang)

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerWorkflowStates(StatesGroup):
    workflow_management = State()
    application_tracking = State()
    task_monitoring = State()

def get_junior_manager_workflow_router():
    """Get router for junior manager workflow management handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["⚙️ Workflow boshqaruvi"]))
    async def workflow_management_menu(message: Message, state: FSMContext):
        """Main workflow management menu for junior manager"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return

            lang = user.get('language', 'uz')
            
            # Get workflow statistics
            stats = await get_junior_manager_dashboard_stats(user['id'])
            app_stats = stats.get('applications', {})
            
            # Calculate basic metrics
            total_apps = app_stats.get('total_applications', 0)
            pending_apps = app_stats.get('pending_applications', 0)
            completed_apps = app_stats.get('completed_applications', 0)
            
            text = f"""⚙️ **Workflow Boshqaruvi**

📊 **Arizalar holati:**
• Jami arizalar: {total_apps}
• Kutilayotgan: {pending_apps}
• Bajarilgan: {completed_apps}

🎯 **Kichik menejer vazifalari:**
• Ulanish arizalarini yaratish
• Arizalar holatini kuzatish
• Mijozlar bilan ishlash
• Hisobotlar tayyorlash

Boshqaruv turini tanlang:"""
            
            # Create keyboard
            keyboard = get_workflow_management_menu(lang)
            
            # Send message
            await message.answer(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
            # Set state
            await state.set_state(JuniorManagerWorkflowStates.workflow_management)
            
        except Exception as e:
            print(f"Error in workflow_management_menu: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("jm_workflow_"))
    async def handle_workflow_actions(callback: CallbackQuery, state: FSMContext):
        """Handle workflow management actions"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            action = callback.data.split("_")[-1]
            
            if action == "tracking":
                await _show_application_tracking(callback, user['id'], lang)
            elif action == "monitoring":
                await _show_task_monitoring(callback, user['id'], lang)
            elif action == "reports":
                await _show_workflow_reports(callback, user['id'], lang)
            elif action == "analytics":
                await _show_workflow_analytics(callback, user['id'], lang)
            else:
                await callback.answer("Noto'g'ri amal", show_alert=True)
                
        except Exception as e:
            print(f"Error in handle_workflow_actions: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_track_"))
    async def handle_tracking_actions(callback: CallbackQuery, state: FSMContext):
        """Handle application tracking actions"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            track_type = callback.data.split("_")[-1]
            
            if track_type == "pending":
                await _show_pending_applications(callback, user['id'], lang)
            elif track_type == "progress":
                await _show_in_progress_applications(callback, user['id'], lang)
            elif track_type == "completed":
                await _show_completed_applications(callback, user['id'], lang)
            elif track_type == "all":
                await _show_all_applications(callback, user['id'], lang)
            else:
                await callback.answer("Noto'g'ri tracking turi", show_alert=True)
                
        except Exception as e:
            print(f"Error in handle_tracking_actions: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_monitor_"))
    async def handle_monitoring_actions(callback: CallbackQuery, state: FSMContext):
        """Handle task monitoring actions"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            monitor_type = callback.data.split("_")[-1]
            
            if monitor_type == "daily":
                await _show_daily_monitoring(callback, user['id'], lang)
            elif monitor_type == "weekly":
                await _show_weekly_monitoring(callback, user['id'], lang)
            elif monitor_type == "performance":
                await _show_performance_monitoring(callback, user['id'], lang)
            else:
                await callback.answer("Noto'g'ri monitoring turi", show_alert=True)
                
        except Exception as e:
            print(f"Error in handle_monitoring_actions: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_application_tracking(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show application tracking dashboard"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, limit=20)
            
            # Count applications by status
            status_counts = {}
            for app in applications:
                status = app['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            text = f"""📋 **Arizalar kuzatuvi**

📊 **Holat bo'yicha:**
• Yangi: {status_counts.get('new', 0)}
• Jarayonda: {status_counts.get('in_progress', 0)}
• Bajarilgan: {status_counts.get('completed', 0)}
• Bekor qilingan: {status_counts.get('cancelled', 0)}

📅 **Oxirgi arizalar:**"""
            
            # Show recent applications
            for app in applications[:5]:
                status_emoji = _get_status_emoji(app['status'])
                client_name = app.get('client_name', 'Noma\'lum')
                created_date = app['created_at'].strftime('%d.%m.%Y')
                text += f"\n{status_emoji} #{app['id']} - {client_name} ({created_date})"
            
            text += "\n\nBatafsil ko'rish uchun kategoriya tanlang:"
            
            keyboard = get_application_tracking_menu(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_application_tracking: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_task_monitoring(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show task monitoring dashboard"""
        try:
            metrics = await get_junior_manager_workflow_metrics(junior_manager_id, days=7)
            
            daily_apps = metrics.get('daily_applications', 0)
            weekly_apps = metrics.get('weekly_applications', 0)
            completion_rate = metrics.get('completion_rate', 0)
            avg_processing_time = metrics.get('avg_processing_time', 0)
            
            text = f"""📊 **Vazifalar monitoringi**

📈 **Haftalik natijalar:**
• Bugungi arizalar: {daily_apps}
• Haftalik arizalar: {weekly_apps}
• Bajarish foizi: {completion_rate:.1f}%
• O'rtacha vaqt: {avg_processing_time:.1f} soat

🎯 **Samaradorlik:**
• {'🟢 Yaxshi' if completion_rate >= 80 else '🟡 O\'rtacha' if completion_rate >= 60 else '🔴 Past'}

Batafsil monitoring tanlang:"""
            
            keyboard = get_task_monitoring_menu(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_task_monitoring: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_workflow_reports(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show workflow reports"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, limit=50)
            
            # Generate report data
            today = datetime.now().date()
            today_apps = len([a for a in applications if a['created_at'].date() == today])
            
            # Application types
            connection_apps = len([a for a in applications if a.get('application_type') == 'connection_request'])
            
            text = f"""📊 **Workflow hisobotlari**

📅 **Vaqt bo'yicha:**
• Bugun: {today_apps} ta ariza
• Bu hafta: {len(applications)} ta ariza
• Bu oy: {len(applications)} ta ariza

📋 **Tur bo'yicha:**
• Ulanish arizalari: {connection_apps}

📈 **Tendentsiyalar:**
• Kunlik o'rtacha: {len(applications)/7:.1f}
• Haftalik o'sish: {'📈' if len(applications) > 0 else '📉'}

Hisobot {today.strftime('%d.%m.%Y')} sanasida yaratilgan."""
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="📄 PDF yuklab olish", callback_data="jm_download_workflow_pdf"),
                    InlineKeyboardButton(text="📊 Excel yuklab olish", callback_data="jm_download_workflow_excel")
                ],
                [
                    InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_workflow")
                ]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_workflow_reports: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_workflow_analytics(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show workflow analytics"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, limit=100)
            
            if not applications:
                text = "Tahlil uchun ma'lumotlar yo'q."
                await callback.message.edit_text(text)
                return
            
            # Analyze patterns
            hourly_distribution = {}
            daily_distribution = {}
            
            for app in applications:
                hour = app['created_at'].hour
                day = app['created_at'].weekday()
                
                hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1
                daily_distribution[day] = daily_distribution.get(day, 0) + 1
            
            # Find peak times
            peak_hour = max(hourly_distribution.items(), key=lambda x: x[1]) if hourly_distribution else (9, 0)
            peak_day = max(daily_distribution.items(), key=lambda x: x[1]) if daily_distribution else (0, 0)
            
            weekdays = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
            peak_day_name = weekdays[peak_day[0]] if peak_day[0] < 7 else 'Noma\'lum'
            
            text = f"""📈 **Workflow analitikasi**

⏰ **Faollik naqshlari:**
• Eng faol soat: {peak_hour[0]:02d}:00 ({peak_hour[1]} ariza)
• Eng faol kun: {peak_day_name} ({peak_day[1]} ariza)

📊 **Soatlik taqsimot:**"""
            
            # Show hourly distribution
            for hour in range(9, 18):  # Working hours
                count = hourly_distribution.get(hour, 0)
                bar = "█" * min(count, 10)
                text += f"\n{hour:02d}:00 {bar} {count}"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="📈 Batafsil", callback_data="jm_detailed_analytics"),
                    InlineKeyboardButton(text="📊 Grafik", callback_data="jm_analytics_chart")
                ],
                [
                    InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_workflow")
                ]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_workflow_analytics: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Helper functions for specific application views
    async def _show_pending_applications(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show pending applications"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, status='new')
            
            if not applications:
                text = "Kutilayotgan arizalar yo'q."
                await callback.message.edit_text(text)
                return
            
            text = f"⏳ **Kutilayotgan arizalar ({len(applications)})**\n\n"
            
            for app in applications[:10]:
                client_name = app.get('client_name', 'Noma\'lum')
                created_date = app['created_at'].strftime('%d.%m %H:%M')
                text += f"🆕 **#{app['id']}** - {client_name}\n   📅 {created_date}\n\n"
            
            if len(applications) > 10:
                text += f"... va yana {len(applications) - 10} ta ariza"
            
            keyboard = get_application_tracking_menu(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_pending_applications: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_in_progress_applications(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show in progress applications"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, status='in_progress')
            
            if not applications:
                text = "Jarayondagi arizalar yo'q."
                await callback.message.edit_text(text)
                return
            
            text = f"🔄 **Jarayondagi arizalar ({len(applications)})**\n\n"
            
            for app in applications[:10]:
                client_name = app.get('client_name', 'Noma\'lum')
                assigned_to = app.get('assigned_to_name', 'Tayinlanmagan')
                created_date = app['created_at'].strftime('%d.%m %H:%M')
                text += f"🔄 **#{app['id']}** - {client_name}\n   👤 {assigned_to}\n   📅 {created_date}\n\n"
            
            if len(applications) > 10:
                text += f"... va yana {len(applications) - 10} ta ariza"
            
            keyboard = get_application_tracking_menu(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_in_progress_applications: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_completed_applications(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show completed applications"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, status='completed')
            
            if not applications:
                text = "Bajarilgan arizalar yo'q."
                await callback.message.edit_text(text)
                return
            
            text = f"✅ **Bajarilgan arizalar ({len(applications)})**\n\n"
            
            for app in applications[:10]:
                client_name = app.get('client_name', 'Noma\'lum')
                completed_date = app.get('updated_at', app['created_at']).strftime('%d.%m %H:%M')
                text += f"✅ **#{app['id']}** - {client_name}\n   📅 {completed_date}\n\n"
            
            if len(applications) > 10:
                text += f"... va yana {len(applications) - 10} ta ariza"
            
            keyboard = get_application_tracking_menu(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_completed_applications: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_all_applications(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show all applications"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, limit=20)
            
            if not applications:
                text = "Arizalar yo'q."
                await callback.message.edit_text(text)
                return
            
            text = f"📋 **Barcha arizalar ({len(applications)})**\n\n"
            
            for app in applications[:10]:
                status_emoji = _get_status_emoji(app['status'])
                client_name = app.get('client_name', 'Noma\'lum')
                created_date = app['created_at'].strftime('%d.%m')
                text += f"{status_emoji} **#{app['id']}** - {client_name} ({created_date})\n"
            
            if len(applications) > 10:
                text += f"\n... va yana {len(applications) - 10} ta ariza"
            
            keyboard = get_application_tracking_menu(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_all_applications: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Monitoring helper functions
    async def _show_daily_monitoring(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show daily monitoring"""
        try:
            today = datetime.now().date()
            applications = await get_junior_manager_applications(junior_manager_id)
            today_apps = [a for a in applications if a['created_at'].date() == today]
            
            # Hourly breakdown
            hourly_stats = {}
            for app in today_apps:
                hour = app['created_at'].hour
                hourly_stats[hour] = hourly_stats.get(hour, 0) + 1
            
            text = f"""📊 **Bugungi monitoring ({today.strftime('%d.%m.%Y')})**

📈 **Umumiy:**
• Jami arizalar: {len(today_apps)}
• Faol soatlar: {len(hourly_stats)}

⏰ **Soatlik taqsimot:**"""
            
            for hour in range(9, 19):  # Working hours
                count = hourly_stats.get(hour, 0)
                bar = "█" * min(count, 10)
                text += f"\n{hour:02d}:00 {bar} {count}"
            
            keyboard = get_task_monitoring_menu(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_daily_monitoring: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_weekly_monitoring(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show weekly monitoring"""
        try:
            today = datetime.now().date()
            applications = await get_junior_manager_applications(junior_manager_id)
            week_apps = applications  # Mock data
            
            # Daily breakdown
            daily_stats = {i: len(applications)//7 for i in range(7)}
            
            weekdays = ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya']
            
            text = f"""📊 **Haftalik monitoring**

📈 **Umumiy:**
• Jami arizalar: {len(week_apps)}
• Kunlik o'rtacha: {len(week_apps)/7:.1f}

📅 **Kunlik taqsimot:**"""
            
            for i, (day, count) in enumerate(daily_stats.items()):
                weekday = weekdays[i]
                bar = "█" * min(count, 15)
                text += f"\n{weekday} {today.strftime('%d.%m')}: {count} {bar}"
            
            keyboard = get_task_monitoring_menu(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_weekly_monitoring: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_performance_monitoring(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show performance monitoring"""
        try:
            metrics = await get_junior_manager_workflow_metrics(junior_manager_id, days=30)
            
            total_apps = metrics.get('total_applications', 0)
            completed_apps = metrics.get('completed_applications', 0)
            completion_rate = metrics.get('completion_rate', 0)
            avg_processing_time = metrics.get('avg_processing_time', 0)
            
            # Performance rating
            if completion_rate >= 90:
                performance_rating = "🟢 A'lo"
            elif completion_rate >= 80:
                performance_rating = "🟡 Yaxshi"
            elif completion_rate >= 70:
                performance_rating = "🟠 O'rtacha"
            else:
                performance_rating = "🔴 Past"
            
            text = f"""📈 **Samaradorlik monitoringi (30 kun)**

🎯 **Asosiy ko'rsatkichlar:**
• Jami arizalar: {total_apps}
• Bajarilgan: {completed_apps}
• Bajarish foizi: {completion_rate:.1f}%
• O'rtacha vaqt: {avg_processing_time:.1f} soat

⭐ **Baho:** {performance_rating}

📊 **Tavsiyalar:**
• {'Ajoyib natija!' if completion_rate >= 90 else 'Yaxshilash mumkin' if completion_rate >= 70 else 'Ko\'proq harakat qiling'}"""
            
            keyboard = get_task_monitoring_menu(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_performance_monitoring: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    def _get_status_emoji(status: str) -> str:
        """Get emoji for application status"""
        status_emojis = {
            'new': '🆕',
            'assigned': '👤',
            'in_progress': '⏳',
            'completed': '✅',
            'cancelled': '❌',
            'on_hold': '⏸️',
            'issue': '🔴'
        }
        return status_emojis.get(status, '❓')

    return router