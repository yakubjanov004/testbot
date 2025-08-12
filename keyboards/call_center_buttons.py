from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ========= MAIN MENUS =========

def get_call_center_main_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Call Center main reply keyboard with WebApp chat button (UZ/RU)."""
    if lang == 'ru':
        webapp_text = "💬 Онлайн Чат Web App"
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📝 Заказы")],
            [KeyboardButton(text="🔍 Поиск клиента")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать техническую заявку")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="🌐 Изменить язык")],
            [KeyboardButton(text=webapp_text, web_app=WebAppInfo(url="https://webapp-gamma-three.vercel.app/"))],
        ]
    else:
        webapp_text = "💬 Onlayn Chat Web App"
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📝 Buyurtmalar")],
            [KeyboardButton(text="🔍 Mijoz qidirish")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="📊 Statistikalar"), KeyboardButton(text="🌐 Tilni o'zgartirish")],
            [KeyboardButton(text=webapp_text, web_app=WebAppInfo(url="https://webapp-gamma-three.vercel.app/"))],
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def call_center_main_menu_reply(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Alias used by some handlers."""
    return get_call_center_main_keyboard(lang)


# ========= LANGUAGE =========

def get_language_selection_inline_menu() -> InlineKeyboardMarkup:
    """Language selection inline keyboard for Call Center role."""
    rows = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="cc_lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="cc_lang_ru"),
        ],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cc_cancel_lang")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ========= ORDERS MENUS =========

def get_orders_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    view_text = "📖 Ko'rish" if lang == 'uz' else "📖 Просмотр"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=view_text)], [KeyboardButton(text=back_text)]], resize_keyboard=True)


def get_order_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    confirm_text = "✅ Tasdiqlash" if lang == 'uz' else "✅ Подтверждение"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=confirm_text)], [KeyboardButton(text=back_text)]], resize_keyboard=True)


# ========= STATISTICS =========

def get_statistics_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    if lang == 'ru':
        rows = [
            [KeyboardButton(text="📅 Показатели за сегодня")],
            [KeyboardButton(text="📊 Еженедельный отчёт")],
            [KeyboardButton(text="📈 Месячный отчёт")],
            [KeyboardButton(text="🎯 Моя эффективность")],
            [KeyboardButton(text="📈 Конверсия")],
            [KeyboardButton(text="🔄 Назад")],
        ]
    else:
        rows = [
            [KeyboardButton(text="📅 Bugungi ko'rsatkichlar")],
            [KeyboardButton(text="📊 Haftalik hisobot")],
            [KeyboardButton(text="📈 Oylik hisobot")],
            [KeyboardButton(text="🎯 Mening samaradorligim")],
            [KeyboardButton(text="📈 Konversiya darajasi")],
            [KeyboardButton(text="🔄 Orqaga")],
        ]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def call_center_statistics_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Alias for compatibility."""
    return get_statistics_keyboard(lang)


# ========= INBOX OPERATOR KEYS =========

def get_operator_navigation_keyboard(current_index: int, total: int, application_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    prev_text = "⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущая"
    next_text = "Keyingi ➡️" if lang == 'uz' else "Следующая ➡️"
    call_text = "📞 Mijoz bilan bog'lanish" if lang == 'uz' else "📞 Связаться с клиентом"
    back_to_inbox_text = "📥 Inbox'ga qaytish" if lang == 'uz' else "📥 Вернуться во входящие"

    rows = []
    rows.append([InlineKeyboardButton(text=call_text, callback_data=f"operator_contact_client_{application_id}")])

    nav = []
    if current_index > 0:
        nav.append(InlineKeyboardButton(text=prev_text, callback_data="operator_prev_application"))
    if current_index < total - 1:
        nav.append(InlineKeyboardButton(text=next_text, callback_data="operator_next_application"))
    if nav:
        rows.append(nav)

    rows.append([InlineKeyboardButton(text=back_to_inbox_text, callback_data="operator_back_to_inbox")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_operator_resolve_keyboard(lang: str = 'uz', application_id: str = "") -> InlineKeyboardMarkup:
    resolve_text = "✅ Muammoni hal qilish" if lang == 'uz' else "✅ Решить проблему"
    back_text = "⬅️ Arizaga qaytish" if lang == 'uz' else "⬅️ Вернуться к заявке"
    rows = [
        [InlineKeyboardButton(text=resolve_text, callback_data=f"operator_resolve_issue_{application_id}")],
        [InlineKeyboardButton(text=back_text, callback_data="operator_back_to_application")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_operator_cancel_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    cancel_text = "❌ Bekor qilish" if lang == 'uz' else "❌ Отмена"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=cancel_text, callback_data="operator_back_to_application")]])


def get_operator_back_to_inbox_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    back_text = "📥 Inbox'ga qaytish" if lang == 'uz' else "📥 Вернуться во входящие"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=back_text, callback_data="operator_back_to_inbox")]])


# ========= CLIENT SEARCH (for CC flows) =========

def get_call_center_client_search_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=("📱 Telefon" if lang == 'uz' else "📱 Телефон"), callback_data="cc_client_search_phone"),
         InlineKeyboardButton(text=("👤 Ism" if lang == 'uz' else "👤 Имя"), callback_data="cc_client_search_name")],
        [InlineKeyboardButton(text="🆔 ID", callback_data="cc_client_search_id"),
         InlineKeyboardButton(text=("➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент"), callback_data="cc_client_search_new")],
        [InlineKeyboardButton(text=("❌ Bekor qilish" if lang == 'uz' else "❌ Отмена"), callback_data="cc_cancel_application_creation")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)