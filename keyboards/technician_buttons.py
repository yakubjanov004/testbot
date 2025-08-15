from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_technician_main_menu_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Technician main menu with 4 reply buttons: Language, Inbox, Tasks, Reports"""
    change_language_text = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"
    inbox_text = "📥 Inbox"
    tasks_text = "📋 Vazifalarim" if lang == "uz" else "📋 Мои задачи"
    reports_text = "📊 Hisobotlarim" if lang == "uz" else "📊 Мои отчеты"

    keyboard = [
        [KeyboardButton(text=change_language_text)],
        [KeyboardButton(text=inbox_text)],
        [KeyboardButton(text=tasks_text)],
        [KeyboardButton(text=reports_text)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_technician_inbox_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Technician inbox navigation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📋 Barchasi" if lang == 'uz' else "📋 Все"), callback_data="tech_inbox_all"),
            InlineKeyboardButton(text=("🆕 Yangi" if lang == 'uz' else "🆕 Новые"), callback_data="tech_inbox_new"),
        ],
        [
            InlineKeyboardButton(text=("🔄 Jarayonda" if lang == 'uz' else "🔄 В процессе"), callback_data="tech_inbox_in_progress"),
            InlineKeyboardButton(text=("✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные"), callback_data="tech_inbox_completed"),
        ],
        [
            InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="tech_back_to_main")],
    ])


def get_technician_tasks_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Technician tasks navigation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📋 Barchasi" if lang == 'uz' else "📋 Все"), callback_data="tech_tasks_all"),
            InlineKeyboardButton(text=("🆕 Yangi" if lang == 'uz' else "🆕 Новые"), callback_data="tech_tasks_new"),
        ],
        [
            InlineKeyboardButton(text=("🔄 Jarayonda" if lang == 'uz' else "🔄 В процессе"), callback_data="tech_tasks_in_progress"),
            InlineKeyboardButton(text=("✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные"), callback_data="tech_tasks_completed"),
        ],
        [
            InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="tech_back_to_main")],
    ])


def get_technician_reports_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Technician reports navigation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📊 Kunlik" if lang == 'uz' else "📊 Ежедневный"), callback_data="tech_report_daily"),
            InlineKeyboardButton(text=("🗓 Haftalik" if lang == 'uz' else "🗓 Еженедельный"), callback_data="tech_report_weekly"),
        ],
        [
            InlineKeyboardButton(text=("📅 Oylik" if lang == 'uz' else "📅 Ежемесячный"), callback_data="tech_report_monthly"),
            InlineKeyboardButton(text=("📈 Natijalar" if lang == 'uz' else "📈 Показатели"), callback_data="tech_report_performance"),
        ],
        [
            InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="tech_back_to_main")],
    ])


def get_technician_back_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Technician back navigation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="tech_back_to_main")],
    ])


def get_back_technician_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard with a single 'Home' button"""
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=back_text)]], resize_keyboard=True)



def get_language_keyboard(role: str = "technician") -> InlineKeyboardMarkup:
    """Inline keyboard for language selection"""
    prefix = f"{role}_lang_" if role != "technician" else "tech_lang_"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data=f"{prefix}uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data=f"{prefix}ru")],
        ]
    )


def get_reports_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Reports menu keyboard (daily/weekly/monthly/performance + home)"""
    daily_text = "📈 Kunlik hisobot" if lang == "uz" else "📈 Ежедневный отчет"
    weekly_text = "🗓 Haftalik hisobot" if lang == "uz" else "🗓 Еженедельный отчет"
    monthly_text = "📅 Oylik hisobot" if lang == "uz" else "📅 Ежемесячный отчет"
    performance_text = "📊 Ish natijalari" if lang == "uz" else "📊 Показатели работы"
    home_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"

    keyboard = [
        [InlineKeyboardButton(text=daily_text, callback_data="tech_daily_report")],
        [InlineKeyboardButton(text=weekly_text, callback_data="tech_weekly_report")],
        [InlineKeyboardButton(text=monthly_text, callback_data="tech_monthly_report")],
        [InlineKeyboardButton(text=performance_text, callback_data="tech_performance_report")],
        [InlineKeyboardButton(text=home_text, callback_data="tech_main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Inbox flow inline keyboards (used by inbox handlers)
def get_diagnostic_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    diagnostic_text = "🔍 Diagnostika boshlash" if lang == "uz" else "🔍 Начать диагностику"
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=diagnostic_text, callback_data="tech_start_diagnostic")],
            [InlineKeyboardButton(text=back_text, callback_data="tech_back_to_application")],
        ]
    )


def get_cancel_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=cancel_text, callback_data="tech_cancel")]])


def get_warehouse_confirmation_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=yes_text, callback_data="tech_warehouse_yes")],
            [InlineKeyboardButton(text=no_text, callback_data="tech_warehouse_no")],
        ]
    )


def get_warehouse_items_keyboard(items: list, lang: str = "uz") -> InlineKeyboardMarkup:
    keyboard = []
    for item in items:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{item['name']} ({item['quantity']} dona)",
                callback_data=f"tech_select_item_{item['id']}",
            )
        ])
    custom_text = "✏️ Boshqa jihoz" if lang == "uz" else "✏️ Другое оборудование"
    keyboard.append([InlineKeyboardButton(text=custom_text, callback_data="tech_custom_warehouse_item")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_warehouse_quantity_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=cancel_text, callback_data="tech_cancel")]])


def get_work_completion_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    complete_text = "✅ Ishni yakunlash" if lang == "uz" else "✅ Завершить работу"
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=complete_text, callback_data="tech_complete_work")],
            [InlineKeyboardButton(text=back_text, callback_data="tech_back_to_application")],
        ]
    )


def get_work_notes_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=cancel_text, callback_data="tech_cancel")]])


def get_back_to_application_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    back_text = "⬅️ Ariza qaytish" if lang == "uz" else "⬅️ Вернуться к заявке"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=back_text, callback_data="tech_back_to_application")]])


def get_help_back_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=back_text, callback_data="tech_back_to_help")]])


def get_reports_back_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=back_text, callback_data="tech_back_to_reports")]])


def get_application_action_keyboard(application, current_index: int, total_applications: int, lang: str = "uz") -> InlineKeyboardMarkup:
    keyboard = []
    if total_applications > 1:
        if current_index > 0:
            prev_text = "⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий"
            keyboard.append([InlineKeyboardButton(text=prev_text, callback_data="tech_prev_application")])
        if current_index < total_applications - 1:
            next_text = "Keyingi ➡️" if lang == "uz" else "Следующий ➡️"
            keyboard.append([InlineKeyboardButton(text=next_text, callback_data="tech_next_application")])

    if application.get("current_status") == "assigned_to_technician":
        accept_text = "✅ Ishni qabul qilish" if lang == "uz" else "✅ Принять работу"
        keyboard.append([InlineKeyboardButton(text=accept_text, callback_data="tech_accept_work")])

    if application.get("work_started", False) and not application.get("work_completed", False):
        diagnostic_text = "🔍 Diagnostika" if lang == "uz" else "🔍 Диагностика"
        keyboard.append([InlineKeyboardButton(text=diagnostic_text, callback_data="tech_start_diagnostic")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


