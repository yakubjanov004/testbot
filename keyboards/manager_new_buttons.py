from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_manager_main_keyboard(lang='uz'):
    """Generate main keyboard for manager with locale support, 2 buttons per row"""
    # 1-qator: 📥 Inbox | 📋 Arizalarni ko'rish
    inbox_text = "📥 Inbox"
    view_applications_text = "📋 Arizalarni ko'rish" if lang == "uz" else "📋 Просмотр заявок"
    
    # 2-qator: 🔌 Ulanish arizasi yaratish | 🔧 Texnik xizmat yaratish
    create_connection_text = "🔌 Ulanish arizasi yaratish" if lang == "uz" else "🔌 Создать заявку на подключение"
    create_technical_text = "🔧 Texnik xizmat yaratish" if lang == "uz" else "🔧 Создать техническую заявку"
    
    # 3-qator: 🕐 Real vaqtda kuzatish | 📊 Monitoring
    realtime_monitoring_text = "🕐 Real vaqtda kuzatish" if lang == "uz" else "🕐 Мониторинг в реальном времени"
    monitoring_text = "📊 Monitoring" if lang == "uz" else "📊 Мониторинг"
    
    # 4-qator: 👥 Xodimlar faoliyati | 🔄 Status o'zgartirish
    staff_activity_text = "👥 Xodimlar faoliyati" if lang == "uz" else "👥 Активность сотрудников"
    change_status_text = "🔄 Status o'zgartirish" if lang == "uz" else "🔄 Изменить статус"
    
    # 5-qator: 📤 Export | 🌐 Tilni o'zgartirish
    export_text = "📤 Export" if lang == "uz" else "📤 Экспорт"
    change_language_text = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"
    
    keyboard = [
        [KeyboardButton(text=inbox_text), KeyboardButton(text=view_applications_text)],
        [KeyboardButton(text=create_connection_text), KeyboardButton(text=create_technical_text)],
        [KeyboardButton(text=realtime_monitoring_text), KeyboardButton(text=monitoring_text)],
        [KeyboardButton(text=staff_activity_text), KeyboardButton(text=change_status_text)],
        [KeyboardButton(text=export_text), KeyboardButton(text=change_language_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_back_keyboard(lang='uz'):
    """Orqaga qaytish tugmasi"""
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [[KeyboardButton(text=back_text)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_status_keyboard(statuses: list, application_id: int, lang='uz') -> InlineKeyboardMarkup:
    """Get status selection keyboard with application_id in callback and locale support"""
    status_texts = {
        'new': '🆕 Yangi' if lang == "uz" else '🆕 Новый',
        'in_progress': '⏳ Jarayonda' if lang == "uz" else '⏳ В процессе',
        'completed': '✅ Bajarilgan' if lang == "uz" else '✅ Выполнено',
        'cancelled': '❌ Bekor qilingan' if lang == "uz" else '❌ Отменено',
        'pending': '⏸️ Kutilmoqda' if lang == "uz" else '⏸️ Ожидает',
        'rejected': '🚫 Rad etilgan' if lang == "uz" else '🚫 Отклонено'
    }
    
    buttons = []
    for status in statuses:
        buttons.append(
            InlineKeyboardButton(
                text=status_texts.get(status, status),
                callback_data=f"status_{status}_{application_id}"
            )
        )
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons[:-1], [buttons[-1]]]  # Last button on separate row
    )
    return keyboard

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
    """Xodimlar faoliyati filtri uchun keyboard"""
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