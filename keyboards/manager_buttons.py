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
    """Arizalarni ko'rish klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Barcha arizalar" if lang == 'uz' else "📋 Все заявки", callback_data="view_all_apps")],
        [InlineKeyboardButton(text="🔍 Qidirish" if lang == 'uz' else "🔍 Поиск", callback_data="search_apps")],
        [InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_main")]
    ])


def get_manager_back_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Orqaga qaytish klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_main")]
    ])


def get_manager_realtime_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Real vaqt monitoring klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить", callback_data="refresh_realtime")],
        [InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_main")]
    ])


def get_realtime_navigation_keyboard(lang: str = 'uz', current_page: int = 1, total_pages: int = 1) -> InlineKeyboardMarkup:
    """Real vaqt monitoring navigatsiya klaviaturasi"""
    buttons = []
    nav_row = []
    
    if current_page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"realtime_page_{current_page - 1}"))
    
    nav_row.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="realtime_current"))
    
    if current_page < total_pages:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"realtime_page_{current_page + 1}"))
    
    if nav_row:
        buttons.append(nav_row)
    
    buttons.append([InlineKeyboardButton(text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить", callback_data="refresh_realtime")])
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_realtime_refresh_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Real vaqt yangilash klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить", callback_data="refresh_realtime")]
    ])


def get_status_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Status tanlash klaviaturasi"""
    statuses = [
        ("📝 Yangi", "new"),
        ("⏳ Jarayonda", "in_progress"),
        ("✅ Bajarildi", "completed"),
        ("❌ Bekor qilindi", "cancelled")
    ]
    
    buttons = []
    for text, status in statuses:
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"set_status_{status}")])
    
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_status_management_keyboard(lang: str = 'uz', app_id: str = None) -> InlineKeyboardMarkup:
    """Status boshqaruv klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Yangi", callback_data=f"status_{app_id}_new")],
        [InlineKeyboardButton(text="⏳ Jarayonda", callback_data=f"status_{app_id}_in_progress")],
        [InlineKeyboardButton(text="✅ Bajarildi", callback_data=f"status_{app_id}_completed")],
        [InlineKeyboardButton(text="❌ Bekor qilindi", callback_data=f"status_{app_id}_cancelled")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_apps")]
    ])


def get_status_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Status navigatsiya klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Barchasi" if lang == 'uz' else "📋 Все", callback_data="status_view_all"),
            InlineKeyboardButton(text="🆕 Yangi" if lang == 'uz' else "🆕 Новые", callback_data="status_view_new")
        ],
        [
            InlineKeyboardButton(text="🔄 Jarayonda" if lang == 'uz' else "🔄 В процессе", callback_data="status_view_progress"),
            InlineKeyboardButton(text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные", callback_data="status_view_completed")
        ],
        [InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_status_main")]
    ])


def get_manager_search_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Qidirish klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Telefon bo'yicha", callback_data="search_by_phone")],
        [InlineKeyboardButton(text="👤 Ism bo'yicha", callback_data="search_by_name")],
        [InlineKeyboardButton(text="🆔 ID bo'yicha", callback_data="search_by_id")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")]
    ])


def get_manager_filters_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Filter klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Sana bo'yicha", callback_data="filter_by_date")],
        [InlineKeyboardButton(text="📋 Status bo'yicha", callback_data="filter_by_status")],
        [InlineKeyboardButton(text="👤 Xodim bo'yicha", callback_data="filter_by_staff")],
        [InlineKeyboardButton(text="🔄 Tozalash", callback_data="clear_filters")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_apps")]
    ])


def get_status_confirmation_keyboard(app_id: str, new_status: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    confirm_text = "✅ Tasdiqlash" if lang == 'uz' else "✅ Подтвердить"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=confirm_text, callback_data=f"confirm_status_change_{app_id}_{new_status}")],
        [InlineKeyboardButton(text=back_text, callback_data="back_to_status_main")],
    ])


def get_inbox_navigation_keyboard(lang: str = 'uz', current_page: int = 1, total_pages: int = 1) -> InlineKeyboardMarkup:
    """
    Inbox sahifalash uchun navigatsiya klaviaturasi
    """
    buttons = []
    nav_row = []
    
    # Previous button
    if current_page > 1:
        nav_row.append(InlineKeyboardButton(
            text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Назад",
            callback_data=f"inbox_page_{current_page - 1}"
        ))
    
    # Page info
    nav_row.append(InlineKeyboardButton(
        text=f"{current_page}/{total_pages}",
        callback_data="inbox_current_page"
    ))
    
    # Next button
    if current_page < total_pages:
        nav_row.append(InlineKeyboardButton(
            text="Keyingi ➡️" if lang == 'uz' else "Вперед ➡️",
            callback_data=f"inbox_page_{current_page + 1}"
        ))
    
    if nav_row:
        buttons.append(nav_row)
    
    # Back to main menu button
    buttons.append([InlineKeyboardButton(
        text="🏠 Asosiy menyu" if lang == 'uz' else "🏠 Главное меню",
        callback_data="manager_main_menu"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_junior_assignment_keyboard(lang: str = 'uz', junior_managers: list = None) -> InlineKeyboardMarkup:
    """
    Junior manager tayinlash uchun klaviatura
    """
    buttons = []
    
    if junior_managers:
        for junior in junior_managers:
            buttons.append([InlineKeyboardButton(
                text=f"👤 {junior.get('full_name', 'Noma\'lum')}",
                callback_data=f"assign_junior_{junior.get('id', 0)}"
            )])
    
    # Cancel button
    buttons.append([InlineKeyboardButton(
        text="❌ Bekor qilish" if lang == 'uz' else "❌ Отменить",
        callback_data="cancel_junior_assignment"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_junior_confirmation_keyboard(lang: str = 'uz', request_id: str = None) -> InlineKeyboardMarkup:
    """
    Junior manager tasdiqlash klaviaturasi
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="✅ Qabul qilish" if lang == 'uz' else "✅ Принять",
                callback_data=f"junior_accept_{request_id}"
            ),
            InlineKeyboardButton(
                text="❌ Rad etish" if lang == 'uz' else "❌ Отклонить",
                callback_data=f"junior_reject_{request_id}"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_application_actions_keyboard(lang: str = 'uz', app_id: str = None) -> InlineKeyboardMarkup:
    """
    Ariza uchun amallar klaviaturasi
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="👁 Ko'rish" if lang == 'uz' else "👁 Просмотр",
                callback_data=f"view_app_{app_id}"
            ),
            InlineKeyboardButton(
                text="✏️ Tahrirlash" if lang == 'uz' else "✏️ Редактировать",
                callback_data=f"edit_app_{app_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Status o'zgartirish" if lang == 'uz' else "📋 Изменить статус",
                callback_data=f"change_status_{app_id}"
            ),
            InlineKeyboardButton(
                text="👤 Tayinlash" if lang == 'uz' else "👤 Назначить",
                callback_data=f"assign_app_{app_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📄 Word hujjat" if lang == 'uz' else "📄 Word документ",
                callback_data=f"generate_word_{app_id}"
            ),
            InlineKeyboardButton(
                text="🗑 O'chirish" if lang == 'uz' else "🗑 Удалить",
                callback_data=f"delete_app_{app_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                callback_data="back_to_apps_list"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_application_navigation_keyboard(lang: str = 'uz', current_page: int = 1, total_pages: int = 1) -> InlineKeyboardMarkup:
    """
    Arizalar ro'yxati uchun navigatsiya klaviaturasi
    """
    buttons = []
    nav_row = []
    
    # Previous button
    if current_page > 1:
        nav_row.append(InlineKeyboardButton(
            text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Назад",
            callback_data=f"apps_page_{current_page - 1}"
        ))
    
    # Page info
    nav_row.append(InlineKeyboardButton(
        text=f"{current_page}/{total_pages}",
        callback_data="apps_current_page"
    ))
    
    # Next button
    if current_page < total_pages:
        nav_row.append(InlineKeyboardButton(
            text="Keyingi ➡️" if lang == 'uz' else "Вперед ➡️",
            callback_data=f"apps_page_{current_page + 1}"
        ))
    
    if nav_row:
        buttons.append(nav_row)
    
    # Filter button
    buttons.append([
        InlineKeyboardButton(
            text="🔍 Filter" if lang == 'uz' else "🔍 Фильтр",
            callback_data="apps_filter"
        ),
        InlineKeyboardButton(
            text="🏠 Asosiy menyu" if lang == 'uz' else "🏠 Главное меню",
            callback_data="manager_main_menu"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
