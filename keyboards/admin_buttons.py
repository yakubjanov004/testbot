from typing import Optional
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# ===============
# Main menu (reply)
# ===============

def get_admin_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Admin main reply keyboard (Uzbek/Russian)."""
    statistics_text = "📊 Statistika" if lang == "uz" else "📊 Статистика"
    users_text = "👥 Foydalanuvchilar" if lang == "uz" else "👥 Пользователи"
    orders_text = "📝 Zayavkalar" if lang == "uz" else "📝 Заявки"
    settings_text = "⚙️ Sozlamalar" if lang == "uz" else "⚙️ Настройки"
    export_text = "📤 Export" if lang == "uz" else "📤 Экспорт"
    language_text = "🌐 Til sozlamalari" if lang == "uz" else "🌐 Языковые настройки"
    help_text = "ℹ️ Yordam" if lang == "uz" else "ℹ️ Помощь"

    keyboard = [
        [KeyboardButton(text=statistics_text), KeyboardButton(text=users_text)],
        [KeyboardButton(text=orders_text), KeyboardButton(text=settings_text)],
        [KeyboardButton(text=export_text), KeyboardButton(text=language_text)],
        [KeyboardButton(text=help_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)


def get_admin_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Alias expected by role system."""
    return get_admin_main_menu(lang)


# =================
# Statistics section
# =================

def get_statistics_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard for statistics section options."""
    general_text = "📈 Umumiy statistika" if lang == "uz" else "📈 Общая статистика"
    orders_stat_text = "📊 Zayavkalar statistikasi" if lang == "uz" else "📊 Статистика заявок"
    users_stat_text = "👥 Foydalanuvchilar statistikasi" if lang == "uz" else "👥 Статистика пользователей"
    technicians_stat_text = "🔧 Texniklar statistikasi" if lang == "uz" else "🔧 Статистика техников"
    kpi_text = "📈 KPI ko'rsatkichlari" if lang == "uz" else "📈 KPI показатели"
    home_text = "🏠 Bosh sahifa" if lang == "uz" else "🏠 Главная"

    keyboard = [
        [KeyboardButton(text=general_text)],
        [KeyboardButton(text=orders_stat_text)],
        [KeyboardButton(text=users_stat_text)],
        [KeyboardButton(text=technicians_stat_text)],
        [KeyboardButton(text=kpi_text)],
        [KeyboardButton(text=home_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# ==============
# Users section
# ==============

def get_users_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard for user management options."""
    search_text = "🔍 Foydalanuvchi qidirish" if lang == "uz" else "🔍 Поиск пользователя"
    list_text = "📋 Foydalanuvchilar ro'yxati" if lang == "uz" else "📋 Список пользователей"
    add_text = "➕ Yangi foydalanuvchi qo'shish" if lang == "uz" else "➕ Добавить пользователя"
    profile_text = "👤 Foydalanuvchi profili" if lang == "uz" else "👤 Профиль пользователя"
    home_text = "🏠 Bosh sahifa" if lang == "uz" else "🏠 Главная"

    keyboard = [
        [KeyboardButton(text=search_text), KeyboardButton(text=list_text)],
        [KeyboardButton(text=add_text), KeyboardButton(text=profile_text)],
        [KeyboardButton(text=home_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# ================
# Settings section
# ================

def get_settings_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard for settings section options."""
    system_text = "🔧 Tizim sozlamalari" if lang == "uz" else "🔧 Системные настройки"
    templates_text = "📢 Bildirishnoma shablonlari" if lang == "uz" else "📢 Шаблоны уведомлений"
    security_text = "🔐 Xavfsizlik sozlamalari" if lang == "uz" else "🔐 Настройки безопасности"
    backup_text = "🔄 Backup va tiklash" if lang == "uz" else "🔄 Резервное копирование"
    home_text = "🏠 Bosh sahifa" if lang == "uz" else "🏠 Главная"

    keyboard = [
        [KeyboardButton(text=system_text)],
        [KeyboardButton(text=templates_text)],
        [KeyboardButton(text=security_text)],
        [KeyboardButton(text=backup_text)],
        [KeyboardButton(text=home_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# ==============
# Orders section
# ==============

def get_zayavka_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard for the orders main menu (admin)."""
    by_status_text = "📂 Holat bo'yicha" if lang == "uz" else "📂 По статусу"
    search_filter_text = "🔍 Qidirish / Filtrlash" if lang == "uz" else "🔍 Поиск / Фильтр"
    search_order_text = "🔍 Zayavka qidirish" if lang == "uz" else "🔍 Поиск заявки"
    home_text = "🏠 Bosh sahifa" if lang == "uz" else "🏠 Главная"

    keyboard = [
        [KeyboardButton(text=by_status_text), KeyboardButton(text=search_filter_text)],
        [KeyboardButton(text=search_order_text)],
        [KeyboardButton(text=home_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_zayavka_section_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard for navigating order sections (status/filter)."""
    by_status_text = "📂 Holat bo'yicha" if lang == "uz" else "📂 По статусу"
    search_filter_text = "🔍 Qidirish / Filtrlash" if lang == "uz" else "🔍 Поиск / Фильтр"
    home_text = "🏠 Bosh sahifa" if lang == "uz" else "🏠 Главная"

    keyboard = [
        [KeyboardButton(text=by_status_text), KeyboardButton(text=search_filter_text)],
        [KeyboardButton(text=home_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_zayavka_status_filter_keyboard(
    lang: str = "uz",
    page: int = 1,
    total_pages: int = 1,
) -> InlineKeyboardMarkup:
    """Inline keyboard to select order status with pagination controls."""
    # Status labels
    status_labels = {
        "uz": {
            "new": "🆕 Yangi",
            "in_progress": "🔄 Jarayonda",
            "completed": "✅ Bajarilgan",
            "cancelled": "❌ Bekor qilingan",
            "pending": "⏳ Kutilmoqda",
        },
        "ru": {
            "new": "🆕 Новые",
            "in_progress": "🔄 В процессе",
            "completed": "✅ Выполненные",
            "cancelled": "❌ Отмененные",
            "pending": "⏳ Ожидают",
        },
    }

    # A simple static list (could be paginated if many statuses)
    statuses = ["new", "in_progress", "completed", "cancelled", "pending"]

    rows = []
    for st in statuses:
        rows.append([
            InlineKeyboardButton(
                text=status_labels[lang].get(st, st),
                callback_data=f"zayavka:status:selected:{st}",
            )
        ])

    # Pagination row (shown only if needed)
    if total_pages > 1:
        prev_btn = InlineKeyboardButton(
            text="⬅️", callback_data=f"zayavka:status:prev:{page}"
        )
        next_btn = InlineKeyboardButton(
            text="➡️", callback_data=f"zayavka:status:next:{page}"
        )
        rows.append([prev_btn, next_btn])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_zayavka_filter_menu_keyboard(
    lang: str = "uz",
    page: int = 1,
    total_pages: int = 2,
    active_filter: Optional[str] = None,
    admin: bool = False,
) -> InlineKeyboardMarkup:
    """Inline keyboard for selecting filter criteria with pagination.

    The handlers expect callback_data of the form:
    - zayavka:filter:username | id | date | category | technician
    - zayavka:filter:prev:<page> or zayavka:filter:next:<page>
    """
    labels = {
        "uz": {
            "username": "🔤 FIO / Username",
            "id": "🔢 Zayavka ID",
            "date": "📆 Sana oraliq",
            "category": "🏷 Kategoriya",
            "technician": "👨‍🔧 Texnik",
        },
        "ru": {
            "username": "🔤 ФИО / Username",
            "id": "🔢 ID заявки",
            "date": "📆 Диапазон дат",
            "category": "🏷 Категория",
            "technician": "👨‍🔧 Техник",
        },
    }

    filter_keys_page_1 = ["username", "id", "date"]
    filter_keys_page_2 = ["category", "technician"]

    use_keys = filter_keys_page_1 if page == 1 else filter_keys_page_2

    rows = []
    for key in use_keys:
        title = labels[lang].get(key, key)
        if active_filter == key:
            title = f"✅ {title}"
        rows.append([
            InlineKeyboardButton(text=title, callback_data=f"zayavka:filter:{key}")
        ])

    # Pagination controls
    prev_btn = None
    next_btn = None
    if page > 1:
        prev_btn = InlineKeyboardButton(text="⬅️", callback_data=f"zayavka:filter:prev:{page}")
    if page < total_pages:
        next_btn = InlineKeyboardButton(text="➡️", callback_data=f"zayavka:filter:next:{page}")

    if prev_btn or next_btn:
        nav_row = []
        if prev_btn:
            nav_row.append(prev_btn)
        if next_btn:
            nav_row.append(next_btn)
        rows.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=rows)


# ==================
# Language selection
# ==================

def language_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard to choose admin panel language."""
    uz_text = "🇺🇿 O'zbek tili" if lang == "uz" else "🇺🇿 Узбекский"
    ru_text = "🇷🇺 Rus tili" if lang == "uz" else "🇷🇺 Русский"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=uz_text, callback_data="lang_uz")],
            [InlineKeyboardButton(text=ru_text, callback_data="lang_ru")],
        ]
    )