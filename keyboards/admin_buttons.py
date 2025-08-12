from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Admin uchun asosiy reply menyu.

    Buttons (UZ/RU):
    - 📊 Statistika / 📊 Статистика
    - 👥 Foydalanuvchilar / 👥 Пользователи
    - 📝 Zayavkalar / 📝 Заявки
    - ⚙️ Sozlamalar / ⚙️ Настройки
    - 📤 Export / 📤 Экспорт
    """
    statistics_text = "📊 Statistika" if lang == "uz" else "📊 Статистика"
    users_text = "👥 Foydalanuvchilar" if lang == "uz" else "👥 Пользователи"
    orders_text = "📝 Zayavkalar" if lang == "uz" else "📝 Заявки"
    settings_text = "⚙️ Sozlamalar" if lang == "uz" else "⚙️ Настройки"
    export_text = "📤 Export" if lang == "uz" else "📤 Экспорт"

    keyboard = [
        [KeyboardButton(text=statistics_text), KeyboardButton(text=users_text)],
        [KeyboardButton(text=orders_text), KeyboardButton(text=settings_text)],
        [KeyboardButton(text=export_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)


# Backward compatibility for role_system.show_admin_menu
def get_admin_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    return get_admin_main_menu(lang)


def get_statistics_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Statistika bo'limi uchun reply klaviatura."""
    general_text = "📈 Umumiy statistika" if lang == "uz" else "📈 Общая статистика"
    orders_text = "📊 Zayavkalar statistikasi" if lang == "uz" else "📊 Статистика заявок"
    users_text = "👥 Foydalanuvchilar statistikasi" if lang == "uz" else "👥 Статистика пользователей"
    technicians_text = "🔧 Texniklar statistikasi" if lang == "uz" else "🔧 Статистика техников"
    kpi_text = "📈 KPI ko'rsatkichlari" if lang == "uz" else "📈 KPI показатели"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=general_text)],
        [KeyboardButton(text=orders_text)],
        [KeyboardButton(text=users_text)],
        [KeyboardButton(text=technicians_text)],
        [KeyboardButton(text=kpi_text)],
        [KeyboardButton(text=back_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_users_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Foydalanuvchilar bo'limi uchun reply klaviatura."""
    search_text = "🔍 Foydalanuvchi qidirish" if lang == "uz" else "🔍 Поиск пользователя"
    list_text = "📋 Foydalanuvchilar ro'yxati" if lang == "uz" else "📋 Список пользователей"
    add_text = "➕ Yangi foydalanuvchi qo'shish" if lang == "uz" else "➕ Добавить пользователя"
    profile_text = "👤 Foydalanuvchi profili" if lang == "uz" else "👤 Профиль пользователя"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=search_text), KeyboardButton(text=list_text)],
        [KeyboardButton(text=add_text), KeyboardButton(text=profile_text)],
        [KeyboardButton(text=back_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_settings_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Sozlamalar bo'limi uchun reply klaviatura."""
    system_text = "🔧 Tizim sozlamalari" if lang == "uz" else "🔧 Системные настройки"
    templates_text = "📢 Bildirishnoma shablonlari" if lang == "uz" else "📢 Шаблоны уведомлений"
    security_text = "🔐 Xavfsizlik sozlamalari" if lang == "uz" else "🔐 Настройки безопасности"
    backup_text = "🔄 Backup va tiklash" if lang == "uz" else "🔄 Резервное копирование"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=system_text)],
        [KeyboardButton(text=templates_text)],
        [KeyboardButton(text=security_text)],
        [KeyboardButton(text=backup_text)],
        [KeyboardButton(text=back_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def language_keyboard() -> InlineKeyboardMarkup:
    """Admin til sozlamalari uchun inline klaviatura."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
    ])


# Orders (Zayavka) keyboards

def get_zayavka_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Zayavkalar bo'limi uchun asosiy reply klaviatura."""
    by_status_text = "📂 Holat bo'yicha" if lang == "uz" else "📂 По статусу"
    filter_text = "🔍 Qidirish / Filtrlash" if lang == "uz" else "🔍 Поиск / Фильтр"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=by_status_text), KeyboardButton(text=filter_text)],
        [KeyboardButton(text=back_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_zayavka_section_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Zayavkalar bo'limi ichidagi bo'lim tanlash uchun reply klaviatura."""
    by_status_text = "📂 Holat bo'yicha" if lang == "uz" else "📂 По статусу"
    filter_text = "🔍 Qidirish / Filtrlash" if lang == "uz" else "🔍 Поиск / Фильтр"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=by_status_text)],
        [KeyboardButton(text=filter_text)],
        [KeyboardButton(text=back_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_zayavka_status_filter_keyboard(lang: str = "uz", page: int = 1, total_pages: int = 1) -> InlineKeyboardMarkup:
    """Holat bo'yicha filtrlash uchun inline klaviatura (sahifalash bilan)."""
    statuses_uz = ["🆕 Yangi", "🔄 Jarayonda", "✅ Bajarilgan", "❌ Bekor qilingan"]
    statuses_ru = ["🆕 Новые", "🔄 В процессе", "✅ Выполненные", "❌ Отмененные"]
    statuses = statuses_uz if lang == "uz" else statuses_ru

    # Map clean status value for callback
    status_map = {
        statuses[0]: "new" if lang == "uz" else "new",
        statuses[1]: "in_progress",
        statuses[2]: "completed",
        statuses[3]: "cancelled",
    }

    rows = []
    for label in statuses:
        rows.append([
            InlineKeyboardButton(
                text=label,
                callback_data=f"zayavka:status:select:{status_map[label]}"
            )
        ])

    # Pagination row
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"zayavka:status:prev:{page}"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"zayavka:status:next:{page}"))
    if nav_row:
        rows.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_zayavka_filter_menu_keyboard(
    lang: str = "uz",
    page: int = 1,
    total_pages: int = 1,
    active_filter: str | None = None,
    admin: bool = False,
) -> InlineKeyboardMarkup:
    """Qidirish/filtrlash uchun inline klaviatura (sahifalash bilan)."""
    labels_uz = {
        "username": "🔤 FIO / Username",
        "id": "🔢 Zayavka ID",
        "date": "📆 Sana oraliq",
        "category": "🏷 Kategoriya",
        "technician": "👨‍🔧 Texnik",
    }
    labels_ru = {
        "username": "🔤 ФИО / Username",
        "id": "🔢 ID заявки",
        "date": "📆 Диапазон дат",
        "category": "🏷 Категория",
        "technician": "👨‍🔧 Техник",
    }
    labels = labels_uz if lang == "uz" else labels_ru

    rows = []
    for key in ["username", "id", "date", "category", "technician"]:
        text = labels[key]
        if active_filter and key == active_filter:
            text = f"✅ {text}"
        rows.append([InlineKeyboardButton(text=text, callback_data=f"zayavka:filter:{key}")])

    # Pagination row
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"zayavka:filter:prev:{page}"))
    if total_pages and page < total_pages:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"zayavka:filter:next:{page}"))
    if nav_row:
        rows.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=rows)


