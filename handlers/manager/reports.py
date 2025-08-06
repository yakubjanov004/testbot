"""
Menejer uchun hisobotlar handleri - Soddalashtirilgan versiya
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, date, timedelta

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

# Mock database functions
async def get_reports():
    """Mock get reports"""
    return {
        'daily': {
            'total_requests': 15,
            'completed': 12,
            'pending': 3,
            'technicians': 5,
            'avg_time': '2 soat 30 daqiqa'
        },
        'weekly': {
            'total_requests': 85,
            'completed': 78,
            'pending': 7,
            'technicians': 8,
            'avg_time': '2 soat 15 daqiqa'
        },
        'monthly': {
            'total_requests': 320,
            'completed': 295,
            'pending': 25,
            'technicians': 10,
            'avg_time': '2 soat 45 daqiqa'
        }
    }

# Mock keyboard function
def get_reports_keyboard(lang: str):
    """Mock reports keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📅 Kunlik hisobot",
                callback_data="report_daily"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Haftalik hisobot",
                callback_data="report_weekly"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Oylik hisobot",
                callback_data="report_monthly"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔧 Texnik xizmat hisoboti",
                callback_data="report_technician"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Status hisoboti",
                callback_data="report_status"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga",
                callback_data="manager_back_to_main"
            )
        ]
    ])

def get_manager_reports_router():
    logger = setup_logger('bot.manager.reports')
    router = get_role_router("manager")

    @router.message(F.text.in_(['📊 Hisobot yaratish', '📊 Создать отчет']))
    async def show_reports_menu(message: Message, state: FSMContext):
        """Manager reports menu handler with enhanced workflow tracking"""
        try:
            # Rate limiting
            if not await rate_limiter.check_rate_limit(message.from_user.id, "show_reports_menu"):
                return
            
            # Start enhanced time tracking for reports menu
            await enhanced_time_tracker.start_role_tracking(
                request_id=f"show_reports_menu_{message.from_user.id}",
                user_id=message.from_user.id,
                role='manager',
                workflow_stage="reports_menu_accessed"
            )
            
            # Track workflow transition for reports menu
            await workflow_manager.track_workflow_transition(
                request_id=f"show_reports_menu_{message.from_user.id}",
                from_role="manager_main_menu",
                to_role="reports_menu",
                user_id=message.from_user.id,
                notes='Manager accessing reports menu'
            )
            
            print(f"DEBUG: Reports handler triggered for user {message.from_user.id}")
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                print(f"DEBUG: Access denied - user role: {user.get('role') if user else 'None'}")
                return
            
            lang = user.get('language', 'uz')
            reports_text = "📊 Hisobot turini tanlang:" if lang == 'uz' else "📊 Выберите тип отчета:"
            
            print(f"DEBUG: Sending reports keyboard to user {message.from_user.id}")
            
            # Application tracking
            await application_tracker.track_application_handling(
                application_id=f"show_reports_menu_{message.from_user.id}",
                handler_id=message.from_user.id,
                action="reports_menu_accessed"
            )
            
            # Update enhanced statistics
            await enhanced_statistics_manager.generate_role_based_statistics('manager', 'daily')
            
            # Audit logging
            await audit_logger.log_user_action(
                user_id=message.from_user.id,
                action="reports_menu_accessed",
                details={"role": user.get('role'), "language": lang}
            )
            
            await message.answer(
                reports_text,
                reply_markup=get_reports_keyboard(lang)
            )
            
            print(f"DEBUG: Reports menu sent successfully")
            
            # End enhanced time tracking
            await enhanced_time_tracker.end_role_tracking(
                request_id=f"show_reports_menu_{message.from_user.id}",
                user_id=message.from_user.id,
                notes="Manager reports menu accessed successfully"
            )
            
        except Exception as e:
            print(f"DEBUG: Error in show_reports_menu: {e}")
            logger.error(f"Error in show_reports_menu: {str(e)}", exc_info=True)
            
            # System event logging
            await audit_logger.log_system_event(
                event_type="error",
                details={"function": "show_reports_menu", "error": str(e), "user_id": message.from_user.id}
            )
            
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка"
            await message.answer(error_text)

    @router.callback_query(F.data.startswith("report_"))
    async def generate_report(callback: CallbackQuery, state: FSMContext):
        """Generate different types of reports"""
        try:
            # Rate limiting
            if not await rate_limiter.check_rate_limit(callback.from_user.id, "generate_report"):
                return
            
            # Time tracking start
            await enhanced_time_tracker.start_tracking(callback.from_user.id, "generate_report")
            
            await answer_and_cleanup(callback, cleanup_after=True)
            report_type = callback.data.replace("report_", "")
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Application tracking
            await application_tracker.track_application_handling(callback.from_user.id, f"generate_report_{report_type}")
            
            # Statistics tracking
            await enhanced_statistics_manager.track_generate_report(callback.from_user.id, report_type)
            
            # Audit logging
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="generate_report",
                details={"report_type": report_type, "role": user.get('role'), "language": lang}
            )
            
            # Use bot's database pool
            async with bot.db.acquire() as conn:
                if report_type == "daily":
                    await generate_daily_report(callback, conn, lang)
                elif report_type == "weekly":
                    await generate_weekly_report(callback, conn, lang)
                elif report_type == "monthly":
                    await generate_monthly_report(callback, conn, lang)
                elif report_type == "technician":
                    await generate_technician_report(callback, conn, lang)
                elif report_type == "status":
                    await generate_status_report(callback, conn, lang)
                else:
                    unknown_text = "Noma'lum hisobot turi" if lang == 'uz' else "Неизвестный тип отчета"
                    await callback.message.edit_text(unknown_text)
            
            # Time tracking end
            await enhanced_time_tracker.end_tracking(callback.from_user.id, "generate_report")
            
        except Exception as e:
            logger.error(f"Error in generate_report: {str(e)}", exc_info=True)
            
            # System event logging
            await audit_logger.log_system_event(
                event_type="error",
                details={"function": "generate_report", "error": str(e), "user_id": callback.from_user.id}
            )
            
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def generate_daily_report(callback, conn, lang):
        """Generate daily report"""
        try:
            # Rate limiting
            if not await rate_limiter.check_rate_limit(callback.from_user.id, "generate_daily_report"):
                return
            
            # Time tracking start
            await enhanced_time_tracker.start_tracking(callback.from_user.id, "generate_daily_report")
            
            today = date.today()
            
            # Get today's statistics
            total_today = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE DATE(created_at) = $1',
                today
            )
            
            completed_today = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE DATE(completed_at) = $1',
                today
            )
            
            in_progress_today = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE status = $1 AND DATE(created_at) = $2',
                'in_progress', today
            )
            
            new_today = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE status = $1 AND DATE(created_at) = $2',
                'new', today
            )
            
            if lang == 'uz':
                report_text = (
                    f"📊 <b>Kunlik hisobot - {today.strftime('%d.%m.%Y')}</b>\n\n"
                    f"📋 <b>Jami arizalar:</b> {total_today}\n"
                    f"🆕 <b>Yangi:</b> {new_today}\n"
                    f"⏳ <b>Jarayonda:</b> {in_progress_today}\n"
                    f"✅ <b>Bajarilgan:</b> {completed_today}\n\n"
                    f"📈 <b>Bajarish foizi:</b> {round((completed_today / total_today * 100) if total_today > 0 else 0, 1)}%"
                )
            else:
                report_text = (
                    f"📊 <b>Дневной отчет - {today.strftime('%d.%m.%Y')}</b>\n\n"
                    f"📋 <b>Всего заявок:</b> {total_today}\n"
                    f"🆕 <b>Новых:</b> {new_today}\n"
                    f"⏳ <b>В процессе:</b> {in_progress_today}\n"
                    f"✅ <b>Выполнено:</b> {completed_today}\n\n"
                    f"📈 <b>Процент выполнения:</b> {round((completed_today / total_today * 100) if total_today > 0 else 0, 1)}%"
                )
            
            # Application tracking
            await application_tracker.track_application_handling(callback.from_user.id, "generate_daily_report")
            
            # Statistics tracking
            await enhanced_statistics_manager.track_generate_daily_report(callback.from_user.id)
            
            # Audit logging
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="generate_daily_report",
                details={"date": today.strftime('%Y-%m-%d'), "language": lang}
            )
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
            # Time tracking end
            await enhanced_time_tracker.end_tracking(callback.from_user.id, "generate_daily_report")
            
        except Exception as e:
            logger.error(f"Error in generate_daily_report: {str(e)}", exc_info=True)
            
            # System event logging
            await audit_logger.log_system_event(
                event_type="error",
                details={"function": "generate_daily_report", "error": str(e), "user_id": callback.from_user.id}
            )

    async def generate_weekly_report(callback, conn, lang):
        """Generate weekly report"""
        try:
            # Rate limiting
            if not await rate_limiter.check_rate_limit(callback.from_user.id, "generate_weekly_report"):
                return
            
            # Time tracking start
            await enhanced_time_tracker.start_tracking(callback.from_user.id, "generate_weekly_report")
            
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
            week_end = today
            
            # Get week's statistics
            total_week = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE DATE(created_at) BETWEEN $1 AND $2',
                week_start, week_end
            )
            
            completed_week = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE DATE(completed_at) BETWEEN $1 AND $2',
                week_start, week_end
            )
            
            # Get daily breakdown
            daily_stats = await conn.fetch(
                '''SELECT DATE(created_at) as day, COUNT(*) as count 
                   FROM zayavki 
                   WHERE DATE(created_at) BETWEEN $1 AND $2 
                   GROUP BY DATE(created_at) 
                   ORDER BY day''',
                week_start, week_end
            )
            
            if lang == 'uz':
                report_text = (
                    f"📊 <b>Haftalik hisobot</b>\n"
                    f"📅 {week_start.strftime('%d.%m.%Y')} - {week_end.strftime('%d.%m.%Y')}\n\n"
                    f"📋 <b>Jami arizalar:</b> {total_week}\n"
                    f"✅ <b>Bajarilgan:</b> {completed_week}\n"
                    f"📈 <b>Bajarish foizi:</b> {round((completed_week / total_week * 100) if total_week > 0 else 0, 1)}%\n\n"
                    f"📅 <b>Kunlik taqsimot:</b>\n"
                )
                
                days_uz = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
                for i in range(7):
                    day_date = week_start + timedelta(days=i)
                    day_count = 0
                    for stat in daily_stats:
                        if stat['day'] == day_date:
                            day_count = stat['count']
                            break
                    report_text += f"• {days_uz[i]} ({day_date.strftime('%d.%m')}): {day_count}\n"
            else:
                report_text = (
                    f"📊 <b>Недельный отчет</b>\n"
                    f"📅 {week_start.strftime('%d.%m.%Y')} - {week_end.strftime('%d.%m.%Y')}\n\n"
                    f"📋 <b>Всего заявок:</b> {total_week}\n"
                    f"✅ <b>Выполнено:</b> {completed_week}\n"
                    f"📈 <b>Процент выполнения:</b> {round((completed_week / total_week * 100) if total_week > 0 else 0, 1)}%\n\n"
                    f"📅 <b>Распределение по дням:</b>\n"
                )
                
                days_ru = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
                for i in range(7):
                    day_date = week_start + timedelta(days=i)
                    day_count = 0
                    for stat in daily_stats:
                        if stat['day'] == day_date:
                            day_count = stat['count']
                            break
                    report_text += f"• {days_ru[i]} ({day_date.strftime('%d.%m')}): {day_count}\n"
            
            # Application tracking
            await application_tracker.track_application_handling(callback.from_user.id, "generate_weekly_report")
            
            # Statistics tracking
            await enhanced_statistics_manager.track_generate_weekly_report(callback.from_user.id)
            
            # Audit logging
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="generate_weekly_report",
                details={"week_start": week_start.strftime('%Y-%m-%d'), "week_end": week_end.strftime('%Y-%m-%d'), "language": lang}
            )
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
            # Time tracking end
            await enhanced_time_tracker.end_tracking(callback.from_user.id, "generate_weekly_report")
            
        except Exception as e:
            logger.error(f"Error in generate_weekly_report: {str(e)}", exc_info=True)
            
            # System event logging
            await audit_logger.log_system_event(
                event_type="error",
                details={"function": "generate_weekly_report", "error": str(e), "user_id": callback.from_user.id}
            )

    async def generate_monthly_report(callback, conn, lang):
        """Generate monthly report"""
        try:
            # Rate limiting
            if not await rate_limiter.check_rate_limit(callback.from_user.id, "generate_monthly_report"):
                return
            
            # Time tracking start
            await enhanced_time_tracker.start_tracking(callback.from_user.id, "generate_monthly_report")
            
            today = date.today()
            month_start = today.replace(day=1)
            month_end = today
            
            # Get month's statistics
            total_month = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE DATE(created_at) BETWEEN $1 AND $2',
                month_start, month_end
            )
            
            completed_month = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE DATE(completed_at) BETWEEN $1 AND $2',
                month_start, month_end
            )
            
            cancelled_month = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE status = $1 AND DATE(created_at) BETWEEN $2 AND $3',
                'cancelled', month_start, month_end
            )
            
            in_progress_month = await conn.fetchval(
                'SELECT COUNT(*) FROM zayavki WHERE status = $1 AND DATE(created_at) BETWEEN $2 AND $3',
                'in_progress', month_start, month_end
            )
            
            # Get technician performance
            tech_stats = await conn.fetch(
                '''SELECT u.full_name, COUNT(z.id) as completed_count
                   FROM users u
                   LEFT JOIN zayavki z ON u.id = z.assigned_to AND z.status = 'completed' 
                   AND DATE(z.completed_at) BETWEEN $1 AND $2
                   WHERE u.role = 'technician'
                   GROUP BY u.id, u.full_name
                   ORDER BY completed_count DESC
                   LIMIT 5''',
                month_start, month_end
            )
            
            month_name = {
                1: {'uz': 'Yanvar', 'ru': 'Январь'},
                2: {'uz': 'Fevral', 'ru': 'Февраль'},
                3: {'uz': 'Mart', 'ru': 'Март'},
                4: {'uz': 'Aprel', 'ru': 'Апрель'},
                5: {'uz': 'May', 'ru': 'Май'},
                6: {'uz': 'Iyun', 'ru': 'Июнь'},
                7: {'uz': 'Iyul', 'ru': 'Июль'},
                8: {'uz': 'Avgust', 'ru': 'Август'},
                9: {'uz': 'Sentyabr', 'ru': 'Сентябрь'},
                10: {'uz': 'Oktyabr', 'ru': 'Октябрь'},
                11: {'uz': 'Noyabr', 'ru': 'Ноябрь'},
                12: {'uz': 'Dekabr', 'ru': 'Декабрь'}
            }.get(today.month, {'uz': 'Noma\'lum', 'ru': 'Неизвестно'})
            
            if lang == 'uz':
                report_text = (
                    f"📊 <b>Oylik hisobot - {month_name['uz']} {today.year}</b>\n\n"
                    f"📋 <b>Jami arizalar:</b> {total_month}\n"
                    f"✅ <b>Bajarilgan:</b> {completed_month}\n"
                    f"⏳ <b>Jarayonda:</b> {in_progress_month}\n"
                    f"❌ <b>Bekor qilingan:</b> {cancelled_month}\n"
                    f"📈 <b>Bajarish foizi:</b> {round((completed_month / total_month * 100) if total_month > 0 else 0, 1)}%\n\n"
                    f"🏆 <b>Eng faol texniklar:</b>\n"
                )
                
                for i, tech in enumerate(tech_stats, 1):
                    report_text += f"{i}. {tech['full_name']}: {tech['completed_count']} ta\n"
            else:
                report_text = (
                    f"📊 <b>Месячный отчет - {month_name['ru']} {today.year}</b>\n\n"
                    f"📋 <b>Всего заявок:</b> {total_month}\n"
                    f"✅ <b>Выполнено:</b> {completed_month}\n"
                    f"⏳ <b>В процессе:</b> {in_progress_month}\n"
                    f"❌ <b>Отменено:</b> {cancelled_month}\n"
                    f"📈 <b>Процент выполнения:</b> {round((completed_month / total_month * 100) if total_month > 0 else 0, 1)}%\n\n"
                    f"🏆 <b>Самые активные техники:</b>\n"
                )
                
                for i, tech in enumerate(tech_stats, 1):
                    report_text += f"{i}. {tech['full_name']}: {tech['completed_count']} шт\n"
            
            # Application tracking
            await application_tracker.track_application_handling(callback.from_user.id, "generate_monthly_report")
            
            # Statistics tracking
            await enhanced_statistics_manager.track_generate_monthly_report(callback.from_user.id)
            
            # Audit logging
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="generate_monthly_report",
                details={"month": f"{today.year}-{today.month:02d}", "language": lang}
            )
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
            # Time tracking end
            await enhanced_time_tracker.end_tracking(callback.from_user.id, "generate_monthly_report")
            
        except Exception as e:
            logger.error(f"Error in generate_monthly_report: {str(e)}", exc_info=True)
            
            # System event logging
            await audit_logger.log_system_event(
                event_type="error",
                details={"function": "generate_monthly_report", "error": str(e), "user_id": callback.from_user.id}
            )

    async def generate_technician_report(callback, conn, lang):
        """Generate technician performance report"""
        try:
            # Rate limiting
            if not await rate_limiter.check_rate_limit(callback.from_user.id, "generate_technician_report"):
                return
            
            # Time tracking start
            await enhanced_time_tracker.start_tracking(callback.from_user.id, "generate_technician_report")
            
            # Get all technicians with their statistics
            tech_stats = await conn.fetch(
                '''SELECT 
                       u.id, u.full_name, u.phone_number,
                       COUNT(CASE WHEN z.status = 'completed' THEN 1 END) as completed,
                       COUNT(CASE WHEN z.status = 'in_progress' THEN 1 END) as in_progress,
                       COUNT(CASE WHEN z.status = 'cancelled' THEN 1 END) as cancelled,
                       COUNT(z.id) as total_assigned
                   FROM users u
                   LEFT JOIN zayavki z ON u.id = z.assigned_to
                   WHERE u.role = 'technician'
                   GROUP BY u.id, u.full_name, u.phone_number
                   ORDER BY completed DESC, total_assigned DESC'''
            )
            
            if lang == 'uz':
                report_text = "👨‍🔧 <b>Texniklar bo'yicha hisobot:</b>\n\n"
                
                for i, tech in enumerate(tech_stats, 1):
                    efficiency = round((tech['completed'] / tech['total_assigned'] * 100) if tech['total_assigned'] > 0 else 0, 1)
                    report_text += (
                        f"{i}. <b>{tech['full_name']}</b>\n"
                        f"   📞 {tech['phone_number'] or 'Telefon yo\'q'}\n"
                        f"   📋 Jami: {tech['total_assigned']}\n"
                        f"   ✅ Bajarilgan: {tech['completed']}\n"
                        f"   ⏳ Jarayonda: {tech['in_progress']}\n"
                        f"   ❌ Bekor qilingan: {tech['cancelled']}\n"
                        f"   📈 Samaradorlik: {efficiency}%\n\n"
                    )
            else:
                report_text = "👨‍🔧 <b>Отчет по техникам:</b>\n\n"
                
                for i, tech in enumerate(tech_stats, 1):
                    efficiency = round((tech['completed'] / tech['total_assigned'] * 100) if tech['total_assigned'] > 0 else 0, 1)
                    report_text += (
                        f"{i}. <b>{tech['full_name']}</b>\n"
                        f"   📞 {tech['phone_number'] or 'Нет телефона'}\n"
                        f"   📋 Всего: {tech['total_assigned']}\n"
                        f"   ✅ Выполнено: {tech['completed']}\n"
                        f"   ⏳ В процессе: {tech['in_progress']}\n"
                        f"   ❌ Отменено: {tech['cancelled']}\n"
                        f"   📈 Эффективность: {efficiency}%\n\n"
                    )
            
            # Application tracking
            await application_tracker.track_application_handling(callback.from_user.id, "generate_technician_report")
            
            # Statistics tracking
            await enhanced_statistics_manager.track_generate_technician_report(callback.from_user.id)
            
            # Audit logging
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="generate_technician_report",
                details={"technician_count": len(tech_stats), "language": lang}
            )
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
            # Time tracking end
            await enhanced_time_tracker.end_tracking(callback.from_user.id, "generate_technician_report")
            
        except Exception as e:
            logger.error(f"Error in generate_technician_report: {str(e)}", exc_info=True)
            
            # System event logging
            await audit_logger.log_system_event(
                event_type="error",
                details={"function": "generate_technician_report", "error": str(e), "user_id": callback.from_user.id}
            )

    async def generate_status_report(callback, conn, lang):
        """Generate status distribution report"""
        try:
            # Rate limiting
            if not await rate_limiter.check_rate_limit(callback.from_user.id, "generate_status_report"):
                return
            
            # Time tracking start
            await enhanced_time_tracker.start_tracking(callback.from_user.id, "generate_status_report")
            
            # Get status statistics
            status_stats = await conn.fetch(
                '''SELECT status, COUNT(*) as count
                   FROM zayavki
                   GROUP BY status
                   ORDER BY count DESC'''
            )
            
            total_applications = sum(stat['count'] for stat in status_stats)
            
            status_emojis = {
                'new': '🆕',
                'confirmed': '✅',
                'in_progress': '⏳',
                'completed': '🏁',
                'cancelled': '❌'
            }
            
            if lang == 'uz':
                status_labels = {
                    'new': 'Yangi',
                    'confirmed': 'Tasdiqlangan',
                    'in_progress': 'Jarayonda',
                    'completed': 'Bajarilgan',
                    'cancelled': 'Bekor qilingan'
                }
                
                report_text = (
                    f"📊 <b>Status bo'yicha hisobot:</b>\n\n"
                    f"📋 <b>Jami arizalar:</b> {total_applications}\n\n"
                )
                
                for stat in status_stats:
                    status = stat['status']
                    count = stat['count']
                    percentage = round((count / total_applications * 100) if total_applications > 0 else 0, 1)
                    emoji = status_emojis.get(status, '📋')
                    label = status_labels.get(status, status)
                    
                    report_text += f"{emoji} <b>{label}:</b> {count} ({percentage}%)\n"
            else:
                status_labels = {
                    'new': 'Новые',
                    'confirmed': 'Подтвержденные',
                    'in_progress': 'В процессе',
                    'completed': 'Выполненные',
                    'cancelled': 'Отмененные'
                }
                
                report_text = (
                    f"📊 <b>Отчет по статусам:</b>\n\n"
                    f"📋 <b>Всего заявок:</b> {total_applications}\n\n"
                )
                
                for stat in status_stats:
                    status = stat['status']
                    count = stat['count']
                    percentage = round((count / total_applications * 100) if total_applications > 0 else 0, 1)
                    emoji = status_emojis.get(status, '📋')
                    label = status_labels.get(status, status)
                    
                    report_text += f"{emoji} <b>{label}:</b> {count} ({percentage}%)\n"
            
            # Application tracking
            await application_tracker.track_application_handling(callback.from_user.id, "generate_status_report")
            
            # Statistics tracking
            await enhanced_statistics_manager.track_generate_status_report(callback.from_user.id)
            
            # Audit logging
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="generate_status_report",
                details={"total_applications": total_applications, "status_count": len(status_stats), "language": lang}
            )
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
            # Time tracking end
            await enhanced_time_tracker.end_tracking(callback.from_user.id, "generate_status_report")
            
        except Exception as e:
            logger.error(f"Error in generate_status_report: {str(e)}", exc_info=True)
            
            # System event logging
            await audit_logger.log_system_event(
                event_type="error",
                details={"function": "generate_status_report", "error": str(e), "user_id": callback.from_user.id}
            )

    @router.callback_query(F.data == "manager_back_to_main")
    async def back_to_main_menu(callback: CallbackQuery):
        """Handle back to main menu button"""
        try:
            # Rate limiting
            if not await rate_limiter.check_rate_limit(callback.from_user.id, "back_to_main_menu"):
                return
            
            # Time tracking start
            await enhanced_time_tracker.start_tracking(callback.from_user.id, "back_to_main_menu")
            
            await callback.message.delete()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz') if user else 'uz'
            
            from keyboards.manager_buttons import get_manager_main_keyboard
            
            welcome_text = (
                f"🏠 <b>Asosiy menyu</b>\n\n"
                f"Kerakli bo'limni tanlang:"
            ) if lang == 'uz' else (
                f"🏠 <b>Главное меню</b>\n\n"
                f"Выберите нужный раздел:"
            )
            
            # Application tracking
            await application_tracker.track_application_handling(callback.from_user.id, "back_to_main_menu")
            
            # Statistics tracking
            await enhanced_statistics_manager.track_back_to_main_menu(callback.from_user.id)
            
            # Audit logging
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="back_to_main_menu",
                details={"role": user.get('role') if user else None, "language": lang}
            )
            
            await callback.message.answer(
                welcome_text,
                parse_mode='HTML',
                reply_markup=get_manager_main_keyboard(lang)
            )
            await callback.answer()
            
            # Time tracking end
            await enhanced_time_tracker.end_tracking(callback.from_user.id, "back_to_main_menu")
            
        except Exception as e:
            logger.error(f"Error in back_to_main_menu: {e}", exc_info=True)
            
            # System event logging
            await audit_logger.log_system_event(
                event_type="error",
                details={"function": "back_to_main_menu", "error": str(e), "user_id": callback.from_user.id}
            )
            
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router
