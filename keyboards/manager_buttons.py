from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_manager_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """
    Manager uchun asosiy reply menyu (O'zbek va Rus tillarida).
    """
    if lang == "uz":
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📋 Arizalarni ko'rish")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="🕐 Real vaqtda kuzatish"), KeyboardButton(text="📊 Monitoring")],
            [KeyboardButton(text="👥 Xodimlar faoliyati"), KeyboardButton(text="🔄 Status o'zgartirish")],
            [KeyboardButton(text="📤 Export"), KeyboardButton(text="🌐 Tilni o'zgartirish")],
        ]
    else:  # ruscha
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📋 Все заявки")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать заявку на тех. обслуживание")],
            [KeyboardButton(text="🕐 Мониторинг в реальном времени"), KeyboardButton(text="📊 Мониторинг")],
            [KeyboardButton(text="👥 Активность сотрудников"), KeyboardButton(text="🔄 Изменить статус")],
            [KeyboardButton(text="📤 Экспорт"), KeyboardButton(text="🌐 Изменить язык")],
        ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


# Inline keyboards required by handlers

def get_manager_realtime_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Manager realtime monitoring keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("🔄 Yangilash" if lang == 'uz' else "🔄 Обновить"), callback_data="realtime_refresh"),
            InlineKeyboardButton(text=("📊 Batafsil" if lang == 'uz' else "📊 Детально"), callback_data="realtime_details"),
        ],
        [
            InlineKeyboardButton(text=("🔴 Shoshilinch" if lang == 'uz' else "🔴 Срочно"), callback_data="realtime_urgent"),
            InlineKeyboardButton(text=("🟠 Yuqori" if lang == 'uz' else "🟠 Высокий"), callback_data="realtime_high"),
        ],
        [
            InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_main_menu")],
    ])


def get_realtime_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Realtime navigation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📋 Barchasi" if lang == 'uz' else "📋 Все"), callback_data="realtime_all"),
            InlineKeyboardButton(text=("🔴 Shoshilinch" if lang == 'uz' else "🔴 Срочно"), callback_data="realtime_urgent"),
        ],
        [
            InlineKeyboardButton(text=("🟠 Yuqori" if lang == 'uz' else "🟠 Высокий"), callback_data="realtime_high"),
            InlineKeyboardButton(text=("🟡 O'rtacha" if lang == 'uz' else "🟡 Средний"), callback_data="realtime_normal"),
        ],
        [
            InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_realtime")],
    ])


def get_realtime_refresh_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Realtime refresh keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("🔄 Yangilash" if lang == 'uz' else "🔄 Обновить"), callback_data="realtime_refresh"),
            InlineKeyboardButton(text=("⏸️ To'xtatish" if lang == 'uz' else "⏸️ Остановить"), callback_data="realtime_pause"),
        ],
        [
            InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_realtime")],
    ])


def get_application_actions_keyboard(app_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Application actions keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("👁️ Ko'rish" if lang == 'uz' else "👁️ Просмотр"), callback_data=f"view_app_{app_id}"),
            InlineKeyboardButton(text=("✏️ Tahrirlash" if lang == 'uz' else "✏️ Редактировать"), callback_data=f"edit_app_{app_id}"),
        ],
        [
            InlineKeyboardButton(text=("🔄 Status" if lang == 'uz' else "🔄 Статус"), callback_data=f"status_app_{app_id}"),
            InlineKeyboardButton(text=("👤 Tayinlash" if lang == 'uz' else "👤 Назначить"), callback_data=f"assign_app_{app_id}"),
        ],
        [
            InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_applications_list")],
    ])


def get_application_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Application navigation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📋 Barchasi" if lang == 'uz' else "📋 Все"), callback_data="apps_all"),
            InlineKeyboardButton(text=("🆕 Yangi" if lang == 'uz' else "🆕 Новые"), callback_data="apps_new"),
        ],
        [
            InlineKeyboardButton(text=("🔄 Jarayonda" if lang == 'uz' else "🔄 В процессе"), callback_data="apps_in_progress"),
            InlineKeyboardButton(text=("✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные"), callback_data="apps_completed"),
        ],
        [
            InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_main_menu")],
    ])


def get_inbox_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Inbox navigation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📋 Barchasi" if lang == 'uz' else "📋 Все"), callback_data="inbox_all"),
            InlineKeyboardButton(text=("🆕 Yangi" if lang == 'uz' else "🆕 Новые"), callback_data="inbox_new"),
        ],
        [
            InlineKeyboardButton(text=("🔄 Jarayonda" if lang == 'uz' else "🔄 В процессе"), callback_data="inbox_in_progress"),
            InlineKeyboardButton(text=("✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные"), callback_data="inbox_completed"),
        ],
        [
            InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_main_menu")],
    ])


def get_junior_assignment_keyboard(juniors, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Junior manager assignment keyboard"""
    rows = []
    for junior in juniors:
        rows.append([
            InlineKeyboardButton(
                text=junior['full_name'], 
                callback_data=f"assign_junior_{junior['id']}"
            )
        ])
    rows.append([
        InlineKeyboardButton(
            text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), 
            callback_data="back_to_inbox"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_junior_confirmation_keyboard(junior_id: int, request_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Junior assignment confirmation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=("✅ Tasdiqlash" if lang == 'uz' else "✅ Подтвердить"), 
                callback_data=f"confirm_junior_{junior_id}_{request_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), 
                callback_data="back_to_inbox"
            )
        ]
    ])


def get_manager_client_search_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📱 Telefon" if lang == 'uz' else "📱 Телефон"), callback_data="mgr_search_phone"),
            InlineKeyboardButton(text=("👤 Ism" if lang == 'uz' else "👤 Имя"), callback_data="mgr_search_name"),
        ],
        [
            InlineKeyboardButton(text=("🆔 ID" if lang == 'uz' else "🆔 ID"), callback_data="mgr_search_id"),
            InlineKeyboardButton(text=("➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент"), callback_data="mgr_search_new"),
        ],
        [
            InlineKeyboardButton(text=("❌ Bekor qilish" if lang == 'uz' else "❌ Отменить"), callback_data="mgr_cancel_creation"),
        ],
    ])


def get_manager_confirmation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    confirm_text = "✅ Tasdiqlash" if lang == 'uz' else "✅ Подтвердить"
    resend_text = "🔄 Qayta yuborish" if lang == 'uz' else "🔄 Отправить заново"
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data="mgr_confirm_zayavka"),
            InlineKeyboardButton(text=resend_text, callback_data="mgr_resend_zayavka"),
        ]
    ])


def get_manager_view_applications_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    all_text = "📋 Hammasi" if lang == 'uz' else "📋 Все"
    active_text = "⏳ Faol" if lang == 'uz' else "⏳ Активные"
    completed_text = "✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=all_text, callback_data="mgr_apps_all")],
        [InlineKeyboardButton(text=active_text, callback_data="mgr_apps_active")],
        [InlineKeyboardButton(text=completed_text, callback_data="mgr_apps_completed")],
        [InlineKeyboardButton(text="⬅️ Orqaga" if lang=='uz' else "⬅️ Назад", callback_data="back_to_main_menu")],
    ])


def get_manager_back_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_main_menu")]
    ])


def get_manager_search_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("🔍 Qidirish" if lang == 'uz' else "🔍 Поиск"), callback_data="mgr_search_start")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_main_menu")],
    ])


def get_manager_filters_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("🆕 Yangi" if lang=='uz' else "🆕 Новые"), callback_data="mgr_filter_new"),
         InlineKeyboardButton(text=("🔄 Jarayonda" if lang=='uz' else "🔄 В процессе"), callback_data="mgr_filter_in_progress")],
        [InlineKeyboardButton(text=("✅ Bajarilgan" if lang=='uz' else "✅ Выполненные"), callback_data="mgr_filter_completed"),
         InlineKeyboardButton(text=("❌ Bekor qilingan" if lang=='uz' else "❌ Отмененные"), callback_data="mgr_filter_cancelled")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_main_menu")]
    ])


def get_status_management_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("📋 Barchasi" if lang=='uz' else "📋 Все"), callback_data="status_view_all_applications")],
        [InlineKeyboardButton(text=("🆕 Yangi" if lang=='uz' else "🆕 Новые"), callback_data="status_view_new_applications")],
        [InlineKeyboardButton(text=("🔄 Jarayonda" if lang=='uz' else "🔄 В процессе"), callback_data="status_view_progress_applications")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_status_main")],
    ])


def get_status_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("📋 Barchasi" if lang=='uz' else "📋 Все"), callback_data="status_view_all_applications"),
         InlineKeyboardButton(text=("🆕 Yangi" if lang=='uz' else "🆕 Новые"), callback_data="status_view_new_applications"),
         InlineKeyboardButton(text=("🔄 Jarayonda" if lang=='uz' else "🔄 В процессе"), callback_data="status_view_progress_applications")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_status_main")],
    ])


def get_status_keyboard(available_statuses, app_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = []
    labels = {
        'new': '🆕 Yangi',
        'in_progress': '🔄 Jarayonda',
        'completed': '✅ Bajarilgan',
        'cancelled': '❌ Bekor qilingan',
    }
    for st in available_statuses:
        rows.append([InlineKeyboardButton(text=labels.get(st, st), callback_data=f"status_{st}_{app_id}")])
    rows.append([InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_status_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_status_confirmation_keyboard(app_id: str, new_status: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    confirm_text = "✅ Tasdiqlash" if lang == 'uz' else "✅ Подтвердить"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=confirm_text, callback_data=f"confirm_status_change_{app_id}_{new_status}")],
        [InlineKeyboardButton(text=back_text, callback_data="back_to_status_main")],
    ])
