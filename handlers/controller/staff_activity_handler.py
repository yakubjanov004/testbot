from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.controllers_buttons import get_back_to_main_menu
from database.models import User, UserRole, Application
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta

router = Router()


@router.message(F.text.in_(['👥 Xodimlar faoliyati', '👥 Активность сотрудников']))
async def staff_activity_handler(message: Message, state: FSMContext, db_session, user: User):
    """Texniklar faoliyatini ko'rish"""
    lang = user.language if user else 'uz'
    
    # Faqat texniklarni olish
    query = select(User).where(User.role == UserRole.TECHNICIAN)
    result = await db_session.execute(query)
    technicians = result.scalars().all()
    
    if not technicians:
        text = {
            'uz': "👥 Texniklar topilmadi",
            'ru': "👥 Техники не найдены"
        }
        await message.answer(
            text.get(lang, text['uz']),
            reply_markup=get_back_to_main_menu(lang)
        )
        return
    
    # Faoliyat statistikasi
    text = {
        'uz': "👥 <b>Texniklar faoliyati:</b>\n\n",
        'ru': "👥 <b>Активность техников:</b>\n\n"
    }
    
    msg_text = text.get(lang, text['uz'])
    
    for tech in technicians:
        # Bugungi bajarilgan ishlar
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        today_completed_query = select(func.count(Application.id)).where(
            and_(
                Application.assigned_to_id == tech.id,
                Application.status == 'completed',
                Application.completed_at >= today_start,
                Application.completed_at <= today_end
            )
        )
        result = await db_session.execute(today_completed_query)
        today_count = result.scalar() or 0
        
        # Haftalik bajarilgan ishlar
        week_ago = datetime.now() - timedelta(days=7)
        week_completed_query = select(func.count(Application.id)).where(
            and_(
                Application.assigned_to_id == tech.id,
                Application.status == 'completed',
                Application.completed_at >= week_ago
            )
        )
        result = await db_session.execute(week_completed_query)
        week_count = result.scalar() or 0
        
        # Hozirda bajarayotgan ishlar
        active_apps_query = select(func.count(Application.id)).where(
            and_(
                Application.assigned_to_id == tech.id,
                Application.status == 'in_progress'
            )
        )
        result = await db_session.execute(active_apps_query)
        active_count = result.scalar() or 0
        
        status_emoji = "🟢" if tech.is_active else "🔴"
        
        msg_text += f"{status_emoji} <b>{tech.full_name}</b>\n"
        msg_text += f"📱 {tech.phone_number}\n"
        
        if lang == 'uz':
            msg_text += f"📅 Bugun: {today_count} ta bajarildi\n"
            msg_text += f"📊 Haftalik: {week_count} ta bajarildi\n"
            msg_text += f"🔄 Hozirda: {active_count} ta ish\n"
        else:
            msg_text += f"📅 Сегодня: {today_count} выполнено\n"
            msg_text += f"📊 За неделю: {week_count} выполнено\n"
            msg_text += f"🔄 Сейчас: {active_count} работ\n"
        
        msg_text += "➖➖➖➖➖➖➖➖➖\n"
    
    # Inline tugmalar
    builder = InlineKeyboardBuilder()
    
    for tech in technicians[:10]:  # Faqat birinchi 10 ta
        builder.button(
            text=f"🔧 {tech.full_name}",
            callback_data=f"tech_detail_{tech.id}"
        )
    
    builder.adjust(1)
    
    await message.answer(
        msg_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    
    # Orqaga tugmasi
    await message.answer(
        "Tanlang:",
        reply_markup=get_back_to_main_menu(lang)
    )