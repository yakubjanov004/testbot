from typing import List

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


# =========================
# Main menu and language
# =========================

def get_warehouse_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Warehouse main reply keyboard (localized)."""
    inbox = "📥 Inbox"
    inventory = "📦 Inventarizatsiya" if lang == "uz" else "📦 Инвентаризация"
    orders = "📋 Buyurtmalar" if lang == "uz" else "📋 Заказы"
    statistics = "📊 Statistikalar" if lang == "uz" else "📊 Статистика"
    export = "📤 Export" if lang == "uz" else "📤 Экспорт"
    change_lang = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"

    keyboard = [
        [KeyboardButton(text=inbox), KeyboardButton(text=inventory)],
        [KeyboardButton(text=orders), KeyboardButton(text=statistics)],
        [KeyboardButton(text=export), KeyboardButton(text=change_lang)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def language_selection_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for language selection used in warehouse module."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="set_language_uz"),
                InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="set_language_ru"),
            ]
        ]
    )


def get_warehouse_back_to_main_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline back-to-main keyboard for warehouse flows."""
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=back, callback_data="warehouse_back_to_main")]]
    )


# =========================
# Inventory keyboards
# =========================

def warehouse_inventory_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard for inventory management menu."""
    all_items = "📋 Barcha mahsulotlar" if lang == "uz" else "📋 Все товары"
    add_item = "➕ Mahsulot qo'shish" if lang == "uz" else "➕ Добавить товар"
    update_item = "✏️ Mahsulotni yangilash" if lang == "uz" else "✏️ Обновить товар"
    search = "🔍 Qidirish" if lang == "uz" else "🔍 Поиск"
    low_stock = "⚠️ Kam zaxira" if lang == "uz" else "⚠️ Низкий остаток"
    out_of_stock = "❌ Tugagan mahsulotlar" if lang == "uz" else "❌ Закончились"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=all_items), KeyboardButton(text=add_item)],
        [KeyboardButton(text=update_item), KeyboardButton(text=search)],
        [KeyboardButton(text=low_stock), KeyboardButton(text=out_of_stock)],
        [KeyboardButton(text=back)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def inventory_actions_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Optional reply keyboard for quick inventory actions (unused but imported)."""
    increase = "➕ Kirim" if lang == "uz" else "➕ Приход"
    decrease = "➖ Chiqim" if lang == "uz" else "➖ Расход"
    delete = "🗑️ O'chirish" if lang == "uz" else "🗑️ Удалить"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=increase), KeyboardButton(text=decrease)],
        [KeyboardButton(text=delete)],
        [KeyboardButton(text=back)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def inventory_actions_inline(item_id: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline actions for inventory item increase/decrease/delete."""
    inc = "➕ Kirim" if lang == "uz" else "➕ Приход"
    dec = "➖ Chiqim" if lang == "uz" else "➖ Расход"
    delete = "🗑️ O'chirish" if lang == "uz" else "🗑️ Удалить"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=inc, callback_data=f"increase_{item_id}"),
                InlineKeyboardButton(text=dec, callback_data=f"decrease_{item_id}"),
            ],
            [InlineKeyboardButton(text=delete, callback_data=f"delete_{item_id}")],
            [InlineKeyboardButton(text=back, callback_data="warehouse_inventory")],
        ]
    )


def update_item_fields_inline(item_id: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard to pick which item field to update."""
    name_t = "📝 Nomi" if lang == "uz" else "📝 Название"
    qty_t = "🔢 Miqdor" if lang == "uz" else "🔢 Количество"
    price_t = "💰 Narx" if lang == "uz" else "💰 Цена"
    desc_t = "📝 Tavsif" if lang == "uz" else "📝 Описание"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name_t, callback_data=f"update_name_{item_id}")],
            [InlineKeyboardButton(text=qty_t, callback_data=f"update_quantity_{item_id}")],
            [InlineKeyboardButton(text=price_t, callback_data=f"update_price_{item_id}")],
            [InlineKeyboardButton(text=desc_t, callback_data=f"update_description_{item_id}")],
            [InlineKeyboardButton(text=back, callback_data="warehouse_inventory")],
        ]
    )


# =========================
# Orders keyboards
# =========================

def warehouse_orders_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard for warehouse orders section."""
    pending = "⏳ Kutilayotgan buyurtmalar" if lang == "uz" else "⏳ Ожидающие"
    in_progress = "🔄 Jarayondagi buyurtmalar" if lang == "uz" else "🔄 В процессе"
    completed = "✅ Bajarilgan buyurtmalar" if lang == "uz" else "✅ Выполненные"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=pending)],
        [KeyboardButton(text=in_progress)],
        [KeyboardButton(text=completed)],
        [KeyboardButton(text=back)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def order_status_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard to filter orders by status."""
    new_t = "🆕 Yangi" if lang == "uz" else "🆕 Новые"
    conf_t = "✅ Tasdiqlangan" if lang == "uz" else "✅ Подтвержденные"
    prog_t = "🔄 Jarayonda" if lang == "uz" else "🔄 В процессе"
    comp_t = "✅ Bajarilgan" if lang == "uz" else "✅ Выполненные"
    canc_t = "❌ Bekor qilingan" if lang == "uz" else "❌ Отмененные"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=new_t, callback_data="filter_orders_new"),
                InlineKeyboardButton(text=conf_t, callback_data="filter_orders_confirmed"),
            ],
            [
                InlineKeyboardButton(text=prog_t, callback_data="filter_orders_in_progress"),
                InlineKeyboardButton(text=comp_t, callback_data="filter_orders_completed"),
            ],
            [InlineKeyboardButton(text=canc_t, callback_data="filter_orders_cancelled")],
            [InlineKeyboardButton(text=back, callback_data="warehouse_back")],
        ]
    )


# =========================
# Inbox keyboards
# =========================

def get_warehouse_inbox_navigation_keyboard(
    current_index: int, total_items: int, lang: str = "uz"
) -> InlineKeyboardMarkup:
    """Inline navigation for inbox requests list (prev/next)."""
    prev_t = "⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущая"
    next_t = "Keyingisi ➡️" if lang == "uz" else "Следующая ➡️"
    rows: List[List[InlineKeyboardButton]] = []
    nav_row: List[InlineKeyboardButton] = []
    if current_index > 0:
        nav_row.append(InlineKeyboardButton(text=prev_t, callback_data="wh_prev"))
    if current_index < max(0, total_items - 1):
        nav_row.append(InlineKeyboardButton(text=next_t, callback_data="wh_next"))
    if nav_row:
        rows.append(nav_row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_warehouse_request_actions_keyboard(request_id: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline actions for a technician-to-warehouse request."""
    approve = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    reject = "❌ Rad etish" if lang == "uz" else "❌ Отклонить"
    prepare = "📦 Tayyorlash" if lang == "uz" else "📦 Подготовить"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=approve, callback_data=f"wh_approve_{request_id}"),
                InlineKeyboardButton(text=reject, callback_data=f"wh_reject_{request_id}"),
            ],
            [InlineKeyboardButton(text=prepare, callback_data=f"wh_prepare_{request_id}")],
        ]
    )


def get_warehouse_back_to_inbox_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard: back to warehouse inbox list."""
    back = "📥 Inbox'ga qaytish" if lang == "uz" else "📥 Вернуться в inbox"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=back, callback_data="wh_back_to_inbox")]]
    )


def get_warehouse_cancel_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline cancel keyboard used while entering rejection reason."""
    cancel = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=cancel, callback_data="wh_back_to_inbox")]]
    )


def get_warehouse_application_actions_keyboard(app_id: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline actions for a warehouse application (detailed view)."""
    complete = "✅ Yakunlash" if lang == "uz" else "✅ Завершить"
    return_to_tech = "🔧 Texnikka qaytarish" if lang == "uz" else "🔧 Вернуть технику"
    prepare = "📦 Tayyorlash" if lang == "uz" else "📦 Подготовить"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=complete, callback_data=f"wh_complete_{app_id}")],
            [InlineKeyboardButton(text=return_to_tech, callback_data=f"wh_return_tech_{app_id}")],
            [InlineKeyboardButton(text=prepare, callback_data=f"wh_prepare_{app_id}")],
        ]
    )


# =========================
# Export keyboards
# =========================

def get_warehouse_export_types_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard to pick export type for warehouse module."""
    inv = "📦 Inventarizatsiya" if lang == "uz" else "📦 Инвентаризация"
    issued = "📋 Berilgan materiallar" if lang == "uz" else "📋 Выданные материалы"
    orders = "📑 Buyurtmalar" if lang == "uz" else "📑 Заказы"
    stats = "📊 Statistika" if lang == "uz" else "📊 Статистика"
    back_main = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=inv, callback_data="warehouse_export_inventory")],
            [InlineKeyboardButton(text=issued, callback_data="warehouse_export_issued_items")],
            [InlineKeyboardButton(text=orders, callback_data="warehouse_export_orders")],
            [InlineKeyboardButton(text=stats, callback_data="warehouse_export_statistics")],
            [InlineKeyboardButton(text=back_main, callback_data="warehouse_export_back_main")],
        ]
    )


def get_warehouse_export_formats_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard to pick export format."""
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="CSV", callback_data="warehouse_format_csv")],
            [InlineKeyboardButton(text="Excel", callback_data="warehouse_format_xlsx")],
            [InlineKeyboardButton(text="Word", callback_data="warehouse_format_docx")],
            [InlineKeyboardButton(text="PDF", callback_data="warehouse_format_pdf")],
            [InlineKeyboardButton(text=back, callback_data="warehouse_export_back_types")],
        ]
    )


def get_warehouse_export_back_types_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Same as types keyboard, used when returning from format selection to type selection."""
    return get_warehouse_export_types_keyboard(lang)


# =========================
# Statistics keyboards
# =========================

def warehouse_statistics_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard for statistics main section."""
    inv_stats = "📦 Inventarizatsiya statistikasi" if lang == "uz" else "📦 Статистика инвентаря"
    order_stats = "📋 Buyurtmalar statistikasi" if lang == "uz" else "📋 Статистика заказов"
    low_stock = "⚠️ Kam zaxira statistikasi" if lang == "uz" else "⚠️ Низкие остатки"
    finance = "💰 Moliyaviy hisobot" if lang == "uz" else "💰 Финансовый отчет"
    period = "📆 Vaqt oralig'idagi statistika" if lang == "uz" else "📆 Статистика по периоду"
    daily = "📅 Kunlik statistika" if lang == "uz" else "📅 Ежедневная статистика"
    weekly = "📊 Haftalik statistika" if lang == "uz" else "📊 Еженедельная статистика"
    monthly = "📈 Oylik statistika" if lang == "uz" else "📈 Ежемесячная статистика"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=daily), KeyboardButton(text=weekly)],
        [KeyboardButton(text=monthly), KeyboardButton(text=period)],
        [KeyboardButton(text=inv_stats), KeyboardButton(text=order_stats)],
        [KeyboardButton(text=low_stock), KeyboardButton(text=finance)],
        [KeyboardButton(text=back)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def statistics_period_menu(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard for picking a statistics period."""
    daily = "📅 Kunlik" if lang == "uz" else "📅 Ежедневно"
    weekly = "📊 Haftalik" if lang == "uz" else "📊 Еженедельно"
    monthly = "📈 Oylik" if lang == "uz" else "📈 Ежемесячно"
    turnover = "🔄 Aylanma" if lang == "uz" else "🔄 Оборот"
    perf = "📈 Samaradorlik" if lang == "uz" else "📈 Эффективность"
    back = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=daily, callback_data="daily_statistics")],
            [InlineKeyboardButton(text=weekly, callback_data="weekly_statistics")],
            [InlineKeyboardButton(text=monthly, callback_data="monthly_statistics")],
            [InlineKeyboardButton(text=turnover, callback_data="turnover_statistics")],
            [InlineKeyboardButton(text=perf, callback_data="performance_report")],
            [InlineKeyboardButton(text=back, callback_data="back")],
        ]
    )


