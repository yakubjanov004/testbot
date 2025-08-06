"""
Menejer uchun hisobotlar handleri - Soddalashtirilgan versiya
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, date, timedelta
from filters.role_filter import RoleFilter

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
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(['📊 Hisobot yaratish', '📊 Создать отчет']))
    async def show_reports_menu(message: Message, state: FSMContext):
        """Manager reports menu handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            reports_text = "📊 Hisobot turini tanlang:" if lang == 'uz' else "📊 Выберите тип отчета:"
            
            await message.answer(
                reports_text,
                reply_markup=get_reports_keyboard(lang)
            )
            
        except Exception as e:
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка"
            await message.answer(error_text)

    @router.callback_query(F.data.startswith("report_"))
    async def generate_report(callback: CallbackQuery, state: FSMContext):
        """Generate different types of reports"""
        try:
            report_type = callback.data.replace("report_", "")
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Mock database connection
            conn = None
            
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
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def generate_daily_report(callback, conn, lang):
        """Generate daily report"""
        try:
            today = date.today()
            
            # Mock statistics
            total_today = 15
            completed_today = 12
            in_progress_today = 2
            new_today = 1
            
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
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def generate_weekly_report(callback, conn, lang):
        """Generate weekly report"""
        try:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
            week_end = today
            
            # Mock statistics
            total_week = 85
            completed_week = 78
            
            if lang == 'uz':
                report_text = (
                    f"📊 <b>Haftalik hisobot</b>\n"
                    f"📅 {week_start.strftime('%d.%m.%Y')} - {week_end.strftime('%d.%m.%Y')}\n\n"
                    f"📋 <b>Jami arizalar:</b> {total_week}\n"
                    f"✅ <b>Bajarilgan:</b> {completed_week}\n"
                    f"📈 <b>Bajarish foizi:</b> {round((completed_week / total_week * 100) if total_week > 0 else 0, 1)}%\n\n"
                    f"📅 <b>Kunlik taqsimot:</b>\n"
                    f"• Dushanba: 12\n"
                    f"• Seshanba: 15\n"
                    f"• Chorshanba: 18\n"
                    f"• Payshanba: 14\n"
                    f"• Juma: 16\n"
                    f"• Shanba: 8\n"
                    f"• Yakshanba: 2\n"
                )
            else:
                report_text = (
                    f"📊 <b>Недельный отчет</b>\n"
                    f"📅 {week_start.strftime('%d.%m.%Y')} - {week_end.strftime('%d.%m.%Y')}\n\n"
                    f"📋 <b>Всего заявок:</b> {total_week}\n"
                    f"✅ <b>Выполнено:</b> {completed_week}\n"
                    f"📈 <b>Процент выполнения:</b> {round((completed_week / total_week * 100) if total_week > 0 else 0, 1)}%\n\n"
                    f"📅 <b>Распределение по дням:</b>\n"
                    f"• Понедельник: 12\n"
                    f"• Вторник: 15\n"
                    f"• Среда: 18\n"
                    f"• Четверг: 14\n"
                    f"• Пятница: 16\n"
                    f"• Суббота: 8\n"
                    f"• Воскресенье: 2\n"
                )
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def generate_monthly_report(callback, conn, lang):
        """Generate monthly report"""
        try:
            today = date.today()
            month_start = today.replace(day=1)
            month_end = today
            
            # Mock statistics
            total_month = 320
            completed_month = 295
            cancelled_month = 5
            in_progress_month = 20
            
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
                    f"1. Umar Toshmatov: 45 ta\n"
                    f"2. Aziz Karimov: 38 ta\n"
                    f"3. Malik Azimov: 32 ta\n"
                    f"4. Jahongir Karimov: 28 ta\n"
                    f"5. Ahmad Toshmatov: 25 ta\n"
                )
            else:
                report_text = (
                    f"📊 <b>Месячный отчет - {month_name['ru']} {today.year}</b>\n\n"
                    f"📋 <b>Всего заявок:</b> {total_month}\n"
                    f"✅ <b>Выполнено:</b> {completed_month}\n"
                    f"⏳ <b>В процессе:</b> {in_progress_month}\n"
                    f"❌ <b>Отменено:</b> {cancelled_month}\n"
                    f"📈 <b>Процент выполнения:</b> {round((completed_month / total_month * 100) if total_month > 0 else 0, 1)}%\n\n"
                    f"🏆 <b>Самые активные техники:</b>\n"
                    f"1. Умар Тошматов: 45 шт\n"
                    f"2. Азиз Каримов: 38 шт\n"
                    f"3. Малик Азимов: 32 шт\n"
                    f"4. Жахонгир Каримов: 28 шт\n"
                    f"5. Ахмад Тошматов: 25 шт\n"
                )
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def generate_technician_report(callback, conn, lang):
        """Generate technician performance report"""
        try:
            # Mock technician statistics
            tech_stats = [
                {'full_name': 'Umar Toshmatov', 'phone_number': '+998901234567', 'total_assigned': 50, 'completed': 45, 'in_progress': 3, 'cancelled': 2},
                {'full_name': 'Aziz Karimov', 'phone_number': '+998901234568', 'total_assigned': 42, 'completed': 38, 'in_progress': 2, 'cancelled': 2},
                {'full_name': 'Malik Azimov', 'phone_number': '+998901234569', 'total_assigned': 38, 'completed': 32, 'in_progress': 4, 'cancelled': 2},
                {'full_name': 'Jahongir Karimov', 'phone_number': '+998901234570', 'total_assigned': 35, 'completed': 28, 'in_progress': 5, 'cancelled': 2},
                {'full_name': 'Ahmad Toshmatov', 'phone_number': '+998901234571', 'total_assigned': 30, 'completed': 25, 'in_progress': 3, 'cancelled': 2}
            ]
            
            if lang == 'uz':
                report_text = "👨‍🔧 <b>Texniklar bo'yicha hisobot:</b>\n\n"
                
                for i, tech in enumerate(tech_stats, 1):
                    efficiency = round((tech['completed'] / tech['total_assigned'] * 100) if tech['total_assigned'] > 0 else 0, 1)
                    report_text += (
                        f"{i}. <b>{tech['full_name']}</b>\n"
                        f"   📞 {tech['phone_number']}\n"
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
                        f"   📞 {tech['phone_number']}\n"
                        f"   📋 Всего: {tech['total_assigned']}\n"
                        f"   ✅ Выполнено: {tech['completed']}\n"
                        f"   ⏳ В процессе: {tech['in_progress']}\n"
                        f"   ❌ Отменено: {tech['cancelled']}\n"
                        f"   📈 Эффективность: {efficiency}%\n\n"
                    )
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def generate_status_report(callback, conn, lang):
        """Generate status distribution report"""
        try:
            # Mock status statistics
            status_stats = [
                {'status': 'completed', 'count': 295},
                {'status': 'in_progress', 'count': 20},
                {'status': 'new', 'count': 15},
                {'status': 'cancelled', 'count': 5}
            ]
            
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
            
            await callback.message.edit_text(report_text, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "manager_back_to_main")
    async def back_to_main_menu(callback: CallbackQuery):
        """Handle back to main menu button"""
        try:
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
            
            await callback.message.answer(
                welcome_text,
                parse_mode='HTML',
                reply_markup=get_manager_main_keyboard(lang)
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router
