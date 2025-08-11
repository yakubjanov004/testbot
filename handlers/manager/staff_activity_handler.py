from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.manager_buttons import get_back_to_main_menu
from database.models import User, UserRole, Application
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta

router = Router()


@router.message(F.text.in_(['👥 Xodimlar faoliyati', '👥 Активность сотрудников']))
async def staff_activity_handler(message: Message, state: FSMContext, db_session, user: User):
    """Kichik menejerlar faoliyatini ko'rish"""
    lang = user.language if user else 'uz'
    
    # Faqat kichik menejerlarni olish
    query = select(User).where(User.role == UserRole.JUNIOR_MANAGER)
    result = await db_session.execute(query)
    junior_managers = result.scalars().all()
    
    if not junior_managers:
        text = {
            'uz': "👥 Kichik menejerlar topilmadi",
            'ru': "👥 Младшие менеджеры не найдены"
        }
        await message.answer(
            text.get(lang, text['uz']),
            reply_markup=get_back_to_main_menu(lang)
        )
        return
    
    # Faoliyat statistikasi
    text = {
        'uz': "👥 <b>Kichik menejerlar faoliyati:</b>\n\n",
        'ru': "👥 <b>Активность младших менеджеров:</b>\n\n"
    }
    
    msg_text = text.get(lang, text['uz'])
    
    for jm in junior_managers:
        # Bugungi arizalar soni
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        today_apps_query = select(func.count(Application.id)).where(
            and_(
                Application.created_by_id == jm.id,
                Application.created_at >= today_start,
                Application.created_at <= today_end
            )
        )
        result = await db_session.execute(today_apps_query)
        today_count = result.scalar() or 0
        
        # Haftalik arizalar soni
        week_ago = datetime.now() - timedelta(days=7)
        week_apps_query = select(func.count(Application.id)).where(
            and_(
                Application.created_by_id == jm.id,
                Application.created_at >= week_ago
            )
        )
        result = await db_session.execute(week_apps_query)
        week_count = result.scalar() or 0
        
        # Aktiv arizalar soni
        active_apps_query = select(func.count(Application.id)).where(
            and_(
                Application.assigned_to_id == jm.id,
                Application.status.in_(['pending', 'in_progress'])
            )
        )
        result = await db_session.execute(active_apps_query)
        active_count = result.scalar() or 0
        
        status_emoji = "🟢" if jm.is_active else "🔴"
        
        msg_text += f"{status_emoji} <b>{jm.full_name}</b>\n"
        msg_text += f"📱 {jm.phone_number}\n"
        
        if lang == 'uz':
            msg_text += f"📅 Bugun: {today_count} ta ariza\n"
            msg_text += f"📊 Haftalik: {week_count} ta ariza\n"
            msg_text += f"🔄 Aktiv: {active_count} ta ariza\n"
        else:
            msg_text += f"📅 Сегодня: {today_count} заявок\n"
            msg_text += f"📊 За неделю: {week_count} заявок\n"
            msg_text += f"🔄 Активные: {active_count} заявок\n"
        
        msg_text += "➖➖➖➖➖➖➖➖➖\n"
    
    # Inline tugmalar
    builder = InlineKeyboardBuilder()
    
    for jm in junior_managers[:10]:  # Faqat birinchi 10 ta
        builder.button(
            text=f"👤 {jm.full_name}",
            callback_data=f"jm_detail_{jm.id}"
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