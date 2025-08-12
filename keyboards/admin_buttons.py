from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional


def get_admin_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    """
    Admin uchun asosiy reply menyu (O'zbek va Rus tillarida).
    This is the primary reply keyboard for admin as requested.
    """
    statistics_text = "📊 Statistika" if lang == "uz" else "📊 Статистика"
    users_text = "👥 Foydalanuvchilar" if lang == "uz" else "👥 Пользователи"
    orders_text = "📝 Zayavkalar" if lang == "uz" else "📝 Заявки"
    settings_text = "⚙️ Sozlamalar" if lang == "uz" else "⚙️ Настройки"
    export_text = "📤 Export" if lang == "uz" else "📤 Экспорт"

    home_text = "🏠 Bosh sahifa" if lang == "uz" else "🏠 Главная"
    help_text = "ℹ️ Yordam" if lang == "uz" else "ℹ️ Помощь"
    language_text = "🌐 Til sozlamalari" if lang == "uz" else "🌐 Языковые настройки"

    keyboard = [
        [KeyboardButton(text=statistics_text), KeyboardButton(text=users_text)],
        [KeyboardButton(text=orders_text), KeyboardButton(text=settings_text)],
        [KeyboardButton(text=export_text), KeyboardButton(text=language_text)],
        [KeyboardButton(text=home_text), KeyboardButton(text=help_text)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_admin_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Compatibility alias used by utils.role_system.show_admin_menu"""
    return get_admin_main_menu(lang)


# Language settings inline keyboard

def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="lang_ru"),
        ]
    ])


# Statistics section keyboard (reply)

def get_statistics_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    general = "📈 Umumiy statistika" if lang == "uz" else "📈 Общая статистика"
    orders = "📊 Zayavkalar statistikasi" if lang == "uz" else "📊 Статистика заявок"
    users = "👥 Foydalanuvchilar statistikasi" if lang == "uz" else "👥 Статистика пользователей"
    techs = "🔧 Texniklar statistikasi" if lang == "uz" else "🔧 Статистика техников"
    kpi = "📈 KPI ko'rsatkichlari" if lang == "uz" else "📈 KPI показатели"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=general)],
        [KeyboardButton(text=orders), KeyboardButton(text=users)],
        [KeyboardButton(text=techs), KeyboardButton(text=kpi)],
        [KeyboardButton(text=back)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Users section keyboard (reply)

def get_users_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    search = "🔍 Foydalanuvchi qidirish" if lang == "uz" else "🔍 Поиск пользователя"
    list_users = "📋 Foydalanuvchilar ro'yxati" if lang == "uz" else "📋 Список пользователей"
    add_user = "➕ Yangi foydalanuvchi qo'shish" if lang == "uz" else "➕ Добавить пользователя"
    profile = "👤 Foydalanuvchi profili" if lang == "uz" else "👤 Профиль пользователя"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=search)],
        [KeyboardButton(text=list_users)],
        [KeyboardButton(text=add_user)],
        [KeyboardButton(text=profile)],
        [KeyboardButton(text=back)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Settings section keyboard (reply)

def get_settings_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    system = "🔧 Tizim sozlamalari" if lang == "uz" else "🔧 Системные настройки"
    templates = "📢 Bildirishnoma shablonlari" if lang == "uz" else "📢 Шаблоны уведомлений"
    security = "🔐 Xavfsizlik sozlamalari" if lang == "uz" else "🔐 Настройки безопасности"
    backup = "🔄 Backup va tiklash" if lang == "uz" else "🔄 Резервное копирование"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=system)],
        [KeyboardButton(text=templates)],
        [KeyboardButton(text=security)],
        [KeyboardButton(text=backup)],
        [KeyboardButton(text=back)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Orders (Zayavkalar) main keyboard (reply)

def get_zayavka_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    by_status = "📂 Holat bo'yicha" if lang == "uz" else "📂 По статусу"
    search_filter = "🔍 Qidirish / Filtrlash" if lang == "uz" else "🔍 Поиск / Фильтр"
    search_by_id = "🔍 Zayavka qidirish" if lang == "uz" else "🔍 Поиск заявки"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=by_status), KeyboardButton(text=search_filter)],
        [KeyboardButton(text=search_by_id)],
        [KeyboardButton(text=back)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Orders section selection keyboard (reply)

def get_zayavka_section_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    by_status = "📂 Holat bo'yicha" if lang == "uz" else "📂 По статусу"
    search_filter = "🔍 Qidirish / Filtrlash" if lang == "uz" else "🔍 Поиск / Фильтр"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=by_status)],
        [KeyboardButton(text=search_filter)],
        [KeyboardButton(text=back)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Orders filters (inline)

def get_zayavka_status_filter_keyboard(lang: str = "uz", page: int = 1, total_pages: int = 1) -> InlineKeyboardMarkup:
    """Inline keyboard for status filtering with pagination callbacks."""
    labels = {
        'uz': {
            'new': "🆕 Yangi",
            'in_progress': "🔄 Jarayonda",
            'completed': "✅ Bajarilgan",
            'cancelled': "❌ Bekor qilingan",
            'pending': "⏳ Kutilmoqda",
            'prev': "⬅️ Oldingi",
            'next': "Keyingi ➡️",
        },
        'ru': {
            'new': "🆕 Новые",
            'in_progress': "🔄 В процессе",
            'completed': "✅ Выполненные",
            'cancelled': "❌ Отмененные",
            'pending': "⏳ Ожидающие",
            'prev': "⬅️ Предыдущая",
            'next': "Следующая ➡️",
        }
    }[lang]

    rows = [
        [InlineKeyboardButton(text=labels['new'], callback_data="zayavka:status:select:new"),
         InlineKeyboardButton(text=labels['in_progress'], callback_data="zayavka:status:select:in_progress")],
        [InlineKeyboardButton(text=labels['completed'], callback_data="zayavka:status:select:completed"),
         InlineKeyboardButton(text=labels['cancelled'], callback_data="zayavka:status:select:cancelled")],
        [InlineKeyboardButton(text=labels['pending'], callback_data="zayavka:status:select:pending")],
    ]

    # Pagination row if needed
    if total_pages > 1:
        rows.append([
            InlineKeyboardButton(text=labels['prev'], callback_data=f"zayavka:status:prev:{page}"),
            InlineKeyboardButton(text=labels['next'], callback_data=f"zayavka:status:next:{page}"),
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_zayavka_filter_menu_keyboard(
    lang: str = "uz",
    page: int = 1,
    total_pages: int = 1,
    active_filter: Optional[str] = None,
    admin: bool = False,
) -> InlineKeyboardMarkup:
    """Inline keyboard for filter type selection with pagination."""
    names = {
        'uz': {
            'username': "🔤 FIO / Username",
            'id': "🔢 Zayavka ID",
            'date': "📆 Sana oraliq",
            'category': "🏷 Kategoriya",
            'technician': "👨‍🔧 Texnik",
            'prev': "⬅️ Oldingi",
            'next': "Keyingi ➡️",
        },
        'ru': {
            'username': "🔤 ФИО / Username",
            'id': "🔢 ID Заявки",
            'date': "📆 Диапазон дат",
            'category': "🏷 Категория",
            'technician': "👨‍🔧 Техник",
            'prev': "⬅️ Предыдущая",
            'next': "Следующая ➡️",
        }
    }[lang]

    def label(key: str) -> str:
        base = names.get(key, key)
        if active_filter and key == active_filter:
            return f"✅ {base}"
        return base

    rows = [
        [InlineKeyboardButton(text=label('username'), callback_data="zayavka:filter:username")],
        [InlineKeyboardButton(text=label('id'), callback_data="zayavka:filter:id")],
        [InlineKeyboardButton(text=label('date'), callback_data="zayavka:filter:date")],
        [InlineKeyboardButton(text=label('category'), callback_data="zayavka:filter:category")],
        [InlineKeyboardButton(text=label('technician'), callback_data="zayavka:filter:technician")],
    ]

    if total_pages > 1:
        rows.append([
            InlineKeyboardButton(text=names['prev'], callback_data=f"zayavka:filter:prev:{page}"),
            InlineKeyboardButton(text=names['next'], callback_data=f"zayavka:filter:next:{page}"),
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)