from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_controller_main_keyboard(lang='uz'):
    """Generate main keyboard for controller with locale support, 2 buttons per row"""
    # 1-qator: 📥 Inbox | 📋 Arizalarni ko'rish
    inbox_text = "📥 Inbox"
    view_applications_text = "📋 Arizalarni ko'rish" if lang == "uz" else "📋 Просмотр заявок"
    
    # 2-qator: 🔌 Ulanish arizasi yaratish | 🔧 Texnik xizmat yaratish
    create_connection_text = "🔌 Ulanish arizasi yaratish" if lang == "uz" else "🔌 Создать заявку на подключение"
    create_technical_text = "🔧 Texnik xizmat yaratish" if lang == "uz" else "🔧 Создать техническую заявку"
    
    # 3-qator: 🕐 Real vaqtda kuzatish | 📊 Monitoring
    realtime_monitoring_text = "🕐 Real vaqtda kuzatish" if lang == "uz" else "🕐 Мониторинг в реальном времени"
    monitoring_text = "📊 Monitoring" if lang == "uz" else "📊 Мониторинг"
    
    # 4-qator: 👥 Xodimlar faoliyati | 📤 Export
    staff_activity_text = "👥 Xodimlar faoliyati" if lang == "uz" else "👥 Активность сотрудников"
    export_text = "📤 Export" if lang == "uz" else "📤 Экспорт"
    
    # 5-qator: 🌐 Tilni o'zgartirish
    change_language_text = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"
    
    keyboard = [
        [KeyboardButton(text=inbox_text), KeyboardButton(text=view_applications_text)],
        [KeyboardButton(text=create_connection_text), KeyboardButton(text=create_technical_text)],
        [KeyboardButton(text=realtime_monitoring_text), KeyboardButton(text=monitoring_text)],
        [KeyboardButton(text=staff_activity_text), KeyboardButton(text=export_text)],
        [KeyboardButton(text=change_language_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_back_keyboard(lang='uz'):
    """Orqaga qaytish tugmasi"""
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [[KeyboardButton(text=back_text)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_application_actions_keyboard(application_id: int, lang='uz') -> InlineKeyboardMarkup:
    """Application uchun action tugmalari"""
    view_text = "👁️ Ko'rish" if lang == "uz" else "👁️ Просмотр"
    edit_text = "✏️ Tahrirlash" if lang == "uz" else "✏️ Редактировать"
    delete_text = "🗑️ O'chirish" if lang == "uz" else "🗑️ Удалить"
    
    keyboard = [
        [InlineKeyboardButton(text=view_text, callback_data=f"view_app_{application_id}")],
        [InlineKeyboardButton(text=edit_text, callback_data=f"edit_app_{application_id}")],
        [InlineKeyboardButton(text=delete_text, callback_data=f"delete_app_{application_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_pagination_keyboard(page: int, total_pages: int, lang='uz') -> InlineKeyboardMarkup:
    """Pagination uchun keyboard"""
    prev_text = "◀️ Oldingi" if lang == "uz" else "◀️ Предыдущая"
    next_text = "Keyingi ▶️" if lang == "uz" else "Следующая ▶️"
    
    keyboard = []
    if page > 1:
        keyboard.append(InlineKeyboardButton(text=prev_text, callback_data=f"page_{page-1}"))
    if page < total_pages:
        keyboard.append(InlineKeyboardButton(text=next_text, callback_data=f"page_{page+1}"))
    
    return InlineKeyboardMarkup(inline_keyboard=[keyboard])

def get_confirmation_keyboard(action_type="confirm", lang='uz') -> InlineKeyboardMarkup:
    """Tasdiqlash uchun keyboard"""
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"
    
    keyboard = [
        [InlineKeyboardButton(text=yes_text, callback_data=f"{action_type}_yes")],
        [InlineKeyboardButton(text=no_text, callback_data=f"{action_type}_no")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_language_keyboard(lang='uz') -> InlineKeyboardMarkup:
    """Til tanlash uchun keyboard"""
    uz_text = "🇺🇿 O'zbekcha" if lang == "uz" else "🇺🇿 Узбекский"
    ru_text = "🇷🇺 Русский" if lang == "uz" else "🇷🇺 Русский"
    
    keyboard = [
        [InlineKeyboardButton(text=uz_text, callback_data="lang_uz")],
        [InlineKeyboardButton(text=ru_text, callback_data="lang_ru")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_export_format_keyboard(lang='uz') -> InlineKeyboardMarkup:
    """Export format tanlash uchun keyboard"""
    excel_text = "📊 Excel" if lang == "uz" else "📊 Excel"
    pdf_text = "📄 PDF" if lang == "uz" else "📄 PDF"
    word_text = "📝 Word" if lang == "uz" else "📝 Word"
    
    keyboard = [
        [InlineKeyboardButton(text=excel_text, callback_data="export_excel")],
        [InlineKeyboardButton(text=pdf_text, callback_data="export_pdf")],
        [InlineKeyboardButton(text=word_text, callback_data="export_word")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_staff_activity_filter_keyboard(lang='uz') -> InlineKeyboardMarkup:
    """Xodimlar faoliyati filtri uchun keyboard (faqat texniklar uchun)"""
    today_text = "📅 Bugun" if lang == "uz" else "📅 Сегодня"
    week_text = "📅 Hafta" if lang == "uz" else "📅 Неделя"
    month_text = "📅 Oy" if lang == "uz" else "📅 Месяц"
    all_text = "📅 Hammasi" if lang == "uz" else "📅 Все"
    
    keyboard = [
        [InlineKeyboardButton(text=today_text, callback_data="staff_today")],
        [InlineKeyboardButton(text=week_text, callback_data="staff_week")],
        [InlineKeyboardButton(text=month_text, callback_data="staff_month")],
        [InlineKeyboardButton(text=all_text, callback_data="staff_all")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_realtime_refresh_keyboard(lang='uz') -> InlineKeyboardMarkup:
    """Real vaqtda yangilash uchun keyboard"""
    refresh_text = "🔄 Yangilash" if lang == "uz" else "🔄 Обновить"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=refresh_text, callback_data="realtime_refresh")],
        [InlineKeyboardButton(text=back_text, callback_data="realtime_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_technician_assignment_keyboard(technicians: list, application_id: int, lang='uz') -> InlineKeyboardMarkup:
    """Texnik tayinlash uchun keyboard"""
    keyboard = []
    
    for tech in technicians:
        workload_emoji = "🟢" if tech.get('active_requests', 0) == 0 else "🟡" if tech.get('active_requests', 0) < 3 else "🔴"
        button_text = f"{workload_emoji} {tech['full_name']} ({tech.get('active_requests', 0)})"
        
        keyboard.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"assign_tech_{application_id}_{tech['id']}"
            )
        ])
    
    # Cancel button
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    keyboard.append([
        InlineKeyboardButton(text=cancel_text, callback_data=f"cancel_assign_{application_id}")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_priority_keyboard(application_id: int, lang='uz') -> InlineKeyboardMarkup:
    """Muhimlik darajasini tanlash uchun keyboard"""
    low_text = "🟢 Past" if lang == "uz" else "🟢 Низкий"
    medium_text = "🟡 O'rta" if lang == "uz" else "🟡 Средний"
    high_text = "🟠 Yuqori" if lang == "uz" else "🟠 Высокий"
    urgent_text = "🔴 Shoshilinch" if lang == "uz" else "🔴 Срочно"
    
    keyboard = [
        [InlineKeyboardButton(text=low_text, callback_data=f"priority_low_{application_id}")],
        [InlineKeyboardButton(text=medium_text, callback_data=f"priority_medium_{application_id}")],
        [InlineKeyboardButton(text=high_text, callback_data=f"priority_high_{application_id}")],
        [InlineKeyboardButton(text=urgent_text, callback_data=f"priority_urgent_{application_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)