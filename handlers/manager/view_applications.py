from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.manager_buttons import get_back_to_main_menu
from database.models import User, Application, ApplicationType
from sqlalchemy import select, desc
from datetime import datetime

router = Router()


@router.message(F.text.in_(['📋 Arizalarni ko\'rish', '📋 Просмотр заявок']))
async def view_applications_handler(message: Message, state: FSMContext, db_session, user: User):
    """Barcha arizalarni ko'rish"""
    lang = user.language if user else 'uz'
    
    # Arizalarni olish
    query = select(Application).order_by(desc(Application.created_at)).limit(20)
    result = await db_session.execute(query)
    applications = result.scalars().all()
    
    if not applications:
        text = {
            'uz': "📋 Hozircha arizalar yo'q",
            'ru': "📋 Пока нет заявок"
        }
        await message.answer(
            text.get(lang, text['uz']),
            reply_markup=get_back_to_main_menu(lang)
        )
        return
    
    # Arizalar ro'yxatini ko'rsatish
    text = {
        'uz': "📋 <b>Barcha arizalar:</b>\n\n",
        'ru': "📋 <b>Все заявки:</b>\n\n"
    }
    
    msg_text = text.get(lang, text['uz'])
    
    for app in applications:
        status_emoji = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'cancelled': '❌'
        }.get(app.status, '❓')
        
        app_type_text = {
            'uz': {
                ApplicationType.CONNECTION: '🔌 Ulanish',
                ApplicationType.TECHNICAL_SERVICE: '🔧 Texnik xizmat'
            },
            'ru': {
                ApplicationType.CONNECTION: '🔌 Подключение',
                ApplicationType.TECHNICAL_SERVICE: '🔧 Тех. обслуживание'
            }
        }
        
        app_type = app_type_text.get(lang, app_type_text['uz']).get(app.application_type, '❓')
        
        msg_text += f"{status_emoji} <b>#{app.id}</b> - {app_type}\n"
        msg_text += f"📍 {app.address}\n"
        msg_text += f"👤 {app.client_name}\n"
        msg_text += f"📅 {app.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        msg_text += "➖➖➖➖➖➖➖➖➖\n"
    
    # Inline tugmalar
    builder = InlineKeyboardBuilder()
    
    for app in applications[:10]:  # Faqat birinchi 10 ta
        builder.button(
            text=f"#{app.id} - {app.client_name[:20]}",
            callback_data=f"view_app_{app.id}"
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