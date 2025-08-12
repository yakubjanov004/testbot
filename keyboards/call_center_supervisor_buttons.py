from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# ========= MAIN REPLY MENU =========
def get_call_center_supervisor_main_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Main reply keyboard for Call Center Supervisor (UZ/RU)."""
    if lang == 'ru':
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📝 Заказы")],
            [KeyboardButton(text="👥 Управление сотрудниками")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать техническую заявку")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📤 Экспорт")],
            [KeyboardButton(text="🌐 Изменить язык")],
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📝 Buyurtmalar")],
            [KeyboardButton(text="👥 Xodimlar boshqaruvi")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="📊 Statistikalar"), KeyboardButton(text="📤 Export")],
            [KeyboardButton(text="🌐 Tilni o'zgartirish")],
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# ========= INBOX SUPPORT KEYS =========
def get_supervisor_navigation_keyboard(current_index: int, total: int, application_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    prev_text = "⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущая"
    next_text = "Keyingi ➡️" if lang == 'uz' else "Следующая ➡️"
    assign_text = "📞 Operatorga yuborish" if lang == 'uz' else "📞 Отправить оператору"
    back_text = "📥 Inbox'ga qaytish" if lang == 'uz' else "📥 Вернуться в входящие"

    rows = []
    # actions
    rows.append([InlineKeyboardButton(text=assign_text, callback_data=f"supervisor_assign_operator_{application_id}")])
    # navigation
    nav = []
    if current_index > 0:
        nav.append(InlineKeyboardButton(text=prev_text, callback_data="supervisor_prev_application"))
    if current_index < total - 1:
        nav.append(InlineKeyboardButton(text=next_text, callback_data="supervisor_next_application"))
    if nav:
        rows.append(nav)
    # back
    rows.append([InlineKeyboardButton(text=back_text, callback_data="supervisor_back_to_inbox")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_supervisor_back_to_inbox_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    back_text = "📥 Inbox'ga qaytish" if lang == 'uz' else "📥 Вернуться в входящие"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=back_text, callback_data="supervisor_back_to_inbox")]])


def get_supervisor_operator_assignment_keyboard(operators: list, application_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = []
    for op in operators:
        status_emoji = "🟢" if op.get('status') == 'available' else "🔴"
        rows.append([
            InlineKeyboardButton(
                text=f"{status_emoji} {op.get('name', 'Operator')} ({op.get('active_calls', 0)} qo'ng'iroq)",
                callback_data=f"supervisor_select_operator_{application_id}_{op.get('id')}"
            )
        ])
    rows.append([InlineKeyboardButton(text=("❌ Bekor qilish" if lang == 'uz' else "❌ Отмена"), callback_data="supervisor_back_to_application")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ========= ORDERS KEYS =========
def get_orders_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    view_text = "📖 Ko'rish" if lang == 'uz' else "📖 Просмотр"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=view_text)], [KeyboardButton(text=back_text)]], resize_keyboard=True)


def get_order_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    confirm_text = "✅ Tasdiqlash" if lang == 'uz' else "✅ Подтверждение"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=confirm_text)], [KeyboardButton(text=back_text)]], resize_keyboard=True)


def get_supervisor_orders_keyboard(lang: str = 'uz', order_id: int = 0) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=("👨‍💼 Mas'ul tayinlash" if lang == 'uz' else "👨‍💼 Назначить ответственного"), callback_data=f"assign_supervisor_{order_id}")],
        [InlineKeyboardButton(text=("🔄 Status o'zgartirish" if lang == 'uz' else "🔄 Изменить статус"), callback_data=f"change_status_{order_id}")],
        [InlineKeyboardButton(text=("❌ Yopish" if lang == 'uz' else "❌ Закрыть"), callback_data="ccs_close_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ========= LANGUAGE =========
def get_language_selection_inline_menu() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang_uz"), InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_language")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ========= STATISTICS / ANALYTICS =========
def get_statistics_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    if lang == 'ru':
        rows = [
            [InlineKeyboardButton(text="📊 Ежедневная статистика", callback_data="ccs_stats_daily")],
            [InlineKeyboardButton(text="📈 Недельный отчет", callback_data="ccs_stats_weekly")],
            [InlineKeyboardButton(text="📉 Месячный отчет", callback_data="ccs_stats_monthly")],
            [InlineKeyboardButton(text="👥 Эффективность персонала", callback_data="ccs_stats_performance")],
            [InlineKeyboardButton(text="🧮 Аналитика заказов", callback_data="ccs_stats_analysis")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        ]
    else:
        rows = [
            [InlineKeyboardButton(text="📊 Kunlik statistika", callback_data="ccs_stats_daily")],
            [InlineKeyboardButton(text="📈 Haftalik hisobot", callback_data="ccs_stats_weekly")],
            [InlineKeyboardButton(text="📉 Oylik hisobot", callback_data="ccs_stats_monthly")],
            [InlineKeyboardButton(text="👥 Xodimlar samaradorligi", callback_data="ccs_stats_performance")],
            [InlineKeyboardButton(text="🧮 Buyurtmalar tahlili", callback_data="ccs_stats_analysis")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_analytics_dashboard_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=("📊 Grafiklar" if lang == 'uz' else "📊 Графики"), callback_data="analytics_charts")],
        [InlineKeyboardButton(text=("📤 Ma'lumot eksport" if lang == 'uz' else "📤 Экспорт данных"), callback_data="analytics_export")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_performance_dashboard_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=("🏆 Eng yaxshi xodimlar" if lang == 'uz' else "🏆 Лучшие сотрудники"), callback_data="perf_top")],
        [InlineKeyboardButton(text=("📈 Dinamika" if lang == 'uz' else "📈 Динамика"), callback_data="perf_dynamics")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def get_supervisor_statistics_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=("📑 Buyurtmalar (CSV)" if lang == 'uz' else "📑 Заказы (CSV)"), callback_data="ccs_export_orders_csv")],
        [InlineKeyboardButton(text=("👥 Xodimlar (CSV)" if lang == 'uz' else "👥 Сотрудники (CSV)"), callback_data="ccs_export_staff_csv")],
        [InlineKeyboardButton(text=("📊 Statistika (CSV)" if lang == 'uz' else "📊 Статистика (CSV)"), callback_data="ccs_export_stats_csv")],
        [InlineKeyboardButton(text=("🎯 KPI (CSV)" if lang == 'uz' else "🎯 KPI (CSV)"), callback_data="ccs_export_kpi_csv")],
        [InlineKeyboardButton(text=("❌ Yopish" if lang == 'uz' else "❌ Закрыть"), callback_data="ccs_close_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ========= EXPORT =========
def get_supervisor_export_types_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=("📑 Buyurtmalar" if lang == 'uz' else "📑 Заказы"), callback_data="ccs_export_main_orders")],
        [InlineKeyboardButton(text=("📊 Statistika" if lang == 'uz' else "📊 Статистика"), callback_data="ccs_export_main_statistics")],
        [InlineKeyboardButton(text=("👥 Xodimlar" if lang == 'uz' else "👥 Сотрудники"), callback_data="ccs_export_main_users")],
        [InlineKeyboardButton(text=("⭐ Fikr-mulohazalar" if lang == 'uz' else "⭐ Отзывы"), callback_data="ccs_export_main_feedback")],
        [InlineKeyboardButton(text=("⚙️ Workflow" if lang == 'uz' else "⚙️ Процессы"), callback_data="ccs_export_main_workflow")],
        [InlineKeyboardButton(text=("◀️ Orqaga" if lang == 'uz' else "◀️ Назад"), callback_data="ccs_export_main_back_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_supervisor_export_formats_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="CSV", callback_data="ccs_format_main_csv"), InlineKeyboardButton(text="Excel", callback_data="ccs_format_main_xlsx")],
        [InlineKeyboardButton(text="Word", callback_data="ccs_format_main_docx"), InlineKeyboardButton(text="PDF", callback_data="ccs_format_main_pdf")],
        [InlineKeyboardButton(text=("◀️ Turlarga qaytish" if lang == 'uz' else "◀️ К типам"), callback_data="ccs_export_main_back_types")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)



# ========= STAFF / MISC PLACEHOLDERS (imported by some handlers) =========
def get_staff_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    view_text = "📋 Xodimlar ro'yxati" if lang == 'uz' else "📋 Список сотрудников"
    performance_text = "📈 Samaradorlik" if lang == 'uz' else "📈 Эффективность"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    keyboard = [[KeyboardButton(text=view_text)], [KeyboardButton(text=performance_text)], [KeyboardButton(text=back_text)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_supervisor_staff_creation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=("📱 Telefon" if lang == 'uz' else "📱 Телефон"), callback_data="ccs_client_search_phone"),
         InlineKeyboardButton(text=("👤 Ism" if lang == 'uz' else "👤 Имя"), callback_data="ccs_client_search_name")],
        [InlineKeyboardButton(text="🆔 ID", callback_data="ccs_client_search_id"),
         InlineKeyboardButton(text=("➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент"), callback_data="ccs_client_search_new")],
        [InlineKeyboardButton(text=("❌ Bekor qilish" if lang == 'uz' else "❌ Отмена"), callback_data="ccs_cancel_application_creation")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)