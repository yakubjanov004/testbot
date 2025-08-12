from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def get_junior_manager_main_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Shortened main reply keyboard for junior manager (backward-compatible name)."""
    inbox = "📥 Inbox"
    create_connection = "🔌 Ulanish arizasi yaratish" if lang == 'uz' else "🔌 Создать заявку на подключение"
    orders = "📋 Buyurtmalar" if lang == 'uz' else "📋 Заказы"
    client_search = "🔍 Mijoz qidiruv" if lang == 'uz' else "🔍 Поиск клиентов"
    statistics = "📊 Statistika" if lang == 'uz' else "📊 Статистика"
    change_language = "🌐 Tilni o'zgartirish" if lang == 'uz' else "🌐 Изменить язык"

    keyboard = [
        [KeyboardButton(text=inbox)],
        [KeyboardButton(text=create_connection)],
        [KeyboardButton(text=orders)],
        [KeyboardButton(text=client_search)],
        [KeyboardButton(text=statistics)],
        [KeyboardButton(text=change_language)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_inbox_keyboard(lang='uz'):
    """Inbox uchun asosiy inline keyboard"""
    all_text = "📋 Barcha arizalar" if lang == 'uz' else "📋 Все заявки"
    pending_text = "⏳ Kutilayotgan" if lang == 'uz' else "⏳ Ожидающие"
    progress_text = "🔄 Jarayonda" if lang == 'uz' else "🔄 В процессе"
    refresh_text = "🔄 Yangilash" if lang == 'uz' else "🔄 Обновить"
    
    keyboard = [
        [InlineKeyboardButton(text=all_text, callback_data="jm_inbox_all")],
        [InlineKeyboardButton(text=pending_text, callback_data="jm_inbox_pending")],
        [InlineKeyboardButton(text=progress_text, callback_data="jm_inbox_progress")],
        [InlineKeyboardButton(text=refresh_text, callback_data="jm_inbox_refresh")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_to_inbox_keyboard(lang='uz'):
    """Inbox-ga qaytish uchun inline keyboard"""
    back_text = "🔙 Inbox-ga qaytish" if lang == 'uz' else "🔙 Вернуться в inbox"
    
    keyboard = [
        [InlineKeyboardButton(text=back_text, callback_data="jm_inbox_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_filter_keyboard(lang='uz'):
    """Zayavkalarni filtrlash uchun tugmalar"""
    new_text = "🆕 Yangi zayavkalar" if lang == "uz" else "🆕 Новые заявки"
    assigned_text = "👨‍🔧 Tayinlangan zayavkalar" if lang == "uz" else "👨‍🔧 Назначенные заявки"
    in_progress_text = "⚡ Jarayonda" if lang == "uz" else "⚡ В процессе"
    completed_text = "✅ Bajarilgan" if lang == "uz" else "✅ Завершенные"
    cancelled_text = "❌ Bekor qilingan" if lang == "uz" else "❌ Отмененные"
    today_text = "📅 Bugungi" if lang == "uz" else "📅 Сегодня"
    yesterday_text = "📅 Kechagi" if lang == "uz" else "📅 Вчера"
    
    keyboard = [
        [InlineKeyboardButton(text=new_text, callback_data="filter_orders:new")],
        [InlineKeyboardButton(text=assigned_text, callback_data="filter_orders:assigned")],
        [InlineKeyboardButton(text=in_progress_text, callback_data="filter_orders:in_progress")],
        [InlineKeyboardButton(text=completed_text, callback_data="filter_orders:completed")],
        [InlineKeyboardButton(text=cancelled_text, callback_data="filter_orders:cancelled")],
        [InlineKeyboardButton(text=today_text, callback_data="filter_orders:today")],
        [InlineKeyboardButton(text=yesterday_text, callback_data="filter_orders:yesterday")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_action_keyboard(order_id, status, lang='uz'):
    """Zayavka uchun harakatlar tugmalari"""
    keyboard = []
    
    if status == 'new':
        assign_text = "👨‍🔧 Texnikka tayinlash" if lang == "uz" else "👨‍🔧 Назначить техника"
        keyboard.append([InlineKeyboardButton(text=assign_text, callback_data=f"assign_order:{order_id}")])
    
    if status in ['new', 'assigned', 'in_progress']:
        cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отменить"
        keyboard.append([InlineKeyboardButton(text=cancel_text, callback_data=f"cancel_order:{order_id}")])
    
    if status == 'in_progress':
        complete_text = "✅ Bajarilgan deb belgilash" if lang == "uz" else "✅ Отметить как выполненную"
        keyboard.append([InlineKeyboardButton(text=complete_text, callback_data=f"complete_order:{order_id}")])
    
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard.append([InlineKeyboardButton(text=back_text, callback_data="back_to_orders")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_assign_order_keyboard(order_id, technicians, lang='uz'):
    """Zayavkani texnikka tayinlash uchun tugmalar"""
    keyboard = []
    
    for tech in technicians:
        keyboard.append([InlineKeyboardButton(
            text=f"👨‍🔧 {tech['name']} ({tech['phone']})",
            callback_data=f"assign_to_tech:{order_id}:{tech['id']}"
        )])
    
    cancel_text = "❌ Bekor qilish" if lang == 'uz' else "❌ Отмена"
    keyboard.append([InlineKeyboardButton(text=cancel_text, callback_data="cancel_assign")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_junior_manager_inbox_actions(order_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Texnikka biriktirish", callback_data=f"action_assign_technician_zayavka_{order_id}"))
    keyboard.add(InlineKeyboardButton("Izoh qo'shish", callback_data=f"action_comment_zayavka_{order_id}"))
    keyboard.add(InlineKeyboardButton("Yakunlash", callback_data=f"action_complete_zayavka_{order_id}"))
    return keyboard


def get_application_keyboard(application_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"accept_{application_id}")],
            [InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{application_id}")]
        ]
    )
    return keyboard


def get_workflow_management_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Workflow management menu keyboard for junior manager"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Arizalar kuzatuvi" if lang == 'uz' else "📋 Отслеживание заявок",
                callback_data="jm_workflow_tracking"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Vazifalar monitoringi" if lang == 'uz' else "📊 Мониторинг задач",
                callback_data="jm_workflow_monitoring"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Hisobotlar" if lang == 'uz' else "📈 Отчеты",
                callback_data="jm_workflow_reports"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Analitika" if lang == 'uz' else "📊 Аналитика",
                callback_data="jm_workflow_analytics"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="jm_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_tracking_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Application tracking menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="⏳ Kutilayotgan" if lang == 'uz' else "⏳ Ожидающие",
                callback_data="jm_track_pending"
            ),
            InlineKeyboardButton(
                text="🔄 Jarayonda" if lang == 'uz' else "🔄 В процессе",
                callback_data="jm_track_progress"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные",
                callback_data="jm_track_completed"
            ),
            InlineKeyboardButton(
                text="📋 Barchasi" if lang == 'uz' else "📋 Все",
                callback_data="jm_track_all"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить",
                callback_data="jm_track_refresh"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                callback_data="jm_workflow_tracking"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_task_monitoring_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Task monitoring menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📅 Bugungi monitoring" if lang == 'uz' else "📅 Мониторинг за сегодня",
                callback_data="jm_monitor_daily"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Haftalik monitoring" if lang == 'uz' else "📊 Недельный мониторинг",
                callback_data="jm_monitor_weekly"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Samaradorlik" if lang == 'uz' else "📈 Эффективность",
                callback_data="jm_monitor_performance"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                callback_data="jm_workflow_monitoring"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_junior_manager_main_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Shortened main menu keyboard for junior manager (used by main_menu handler)."""
    inbox = "📥 Inbox"
    create_connection = "🔌 Ulanish arizasi yaratish" if lang == 'uz' else "🔌 Создать заявку на подключение"
    orders = "📋 Buyurtmalar" if lang == 'uz' else "📋 Заказы"
    client_search = "🔍 Mijoz qidiruv" if lang == 'uz' else "🔍 Поиск клиентов"
    statistics = "📊 Statistika" if lang == 'uz' else "📊 Статистика"
    change_language = "🌐 Tilni o'zgartirish" if lang == 'uz' else "🌐 Изменить язык"
    
    keyboard = [
        [KeyboardButton(text=inbox)],
        [KeyboardButton(text=create_connection)],
        [KeyboardButton(text=orders)],
        [KeyboardButton(text=client_search)],
        [KeyboardButton(text=statistics)],
        [KeyboardButton(text=change_language)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_application_list_keyboard(applications: list, page: int = 0, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Generate keyboard for application list with pagination"""
    keyboard = []
    
    # Show applications (5 per page)
    start_idx = page * 5
    end_idx = min(start_idx + 5, len(applications))
    
    for i in range(start_idx, end_idx):
        app = applications[i]
        status_emoji = _get_status_emoji(app['status'])
        client_name = app.get('client_name', 'N/A')[:15]
        text = f"{status_emoji} #{app['id']} - {client_name}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"jm_view_app_{app['id']}"
            )
        ])
    
    # Pagination buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущая",
                callback_data=f"jm_apps_page_{page-1}"
            )
        )
    
    if end_idx < len(applications):
        nav_buttons.append(
            InlineKeyboardButton(
                text="Keyingi ➡️" if lang == 'uz' else "Следующая ➡️",
                callback_data=f"jm_apps_page_{page+1}"
            )
        )
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Close button
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
            callback_data="jm_close_menu"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_action_keyboard(app_id: int, status: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Generate action keyboard for specific application"""
    keyboard = []
    
    # Junior managers have limited actions
    if status == 'new':
        keyboard.append([
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отменить",
                callback_data=f"jm_cancel_app_{app_id}"
            )
        ])
    
    # View details button
    keyboard.append([
        InlineKeyboardButton(
            text="📋 Batafsil" if lang == 'uz' else "📋 Подробности",
            callback_data=f"jm_details_app_{app_id}"
        )
    ])
    
    # Back button
    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
            callback_data="jm_track_all"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_client_search_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Client search method selection keyboard for junior manager"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📱 Telefon" if lang == 'uz' else "📱 Телефон",
                callback_data="jm_client_search_phone"
            ),
            InlineKeyboardButton(
                text="👤 Ism" if lang == 'uz' else "👤 Имя",
                callback_data="jm_client_search_name"
            )
        ],
        [
            InlineKeyboardButton(
                text="🆔 ID" if lang == 'uz' else "🆔 ID",
                callback_data="jm_client_search_id"
            ),
            InlineKeyboardButton(
                text="➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент",
                callback_data="jm_client_search_new"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="jm_cancel_application_creation"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_client_selection_keyboard(clients: list, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Generate keyboard for client selection"""
    keyboard = []
    
    for client in clients[:8]:  # Limit to 8 clients
        text = f"👤 {client['full_name']} - {client.get('phone', 'N/A')}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"jm_select_client_{client['id']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="🔍 Boshqa qidirish" if lang == 'uz' else "🔍 Другой поиск",
            callback_data="jm_search_again"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
            callback_data="jm_cancel_application_creation"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_priority_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Application priority selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔴 Yuqori" if lang == 'uz' else "🔴 Высокий",
                callback_data="jm_priority_high"
            ),
            InlineKeyboardButton(
                text="🟡 O'rta" if lang == 'uz' else "🟡 Средний",
                callback_data="jm_priority_medium"
            )
        ],
        [
            InlineKeyboardButton(
                text="🟢 Past" if lang == 'uz' else "🟢 Низкий",
                callback_data="jm_priority_low"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="jm_cancel_application_creation"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_confirmation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Application confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash" if lang == 'uz' else "✅ Подтвердить",
                callback_data="jm_confirm_application"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Tahrirlash" if lang == 'uz' else "📝 Редактировать",
                callback_data="jm_edit_application"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="jm_cancel_application_creation"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def _get_status_emoji(status: str) -> str:
    """Get emoji for application status"""
    status_emojis = {
        'new': '🆕',
        'assigned': '👤',
        'in_progress': '⏳',
        'completed': '✅',
        'cancelled': '❌',
        'on_hold': '⏸️',
        'issue': '🔴'
    }
    return status_emojis.get(status, '❓')


def get_language_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Junior manager uchun til tanlash inline keyboard"""
    uz_text = "🇺🇿 O'zbekcha" if lang == "uz" else "🇺🇿 Узбекский"
    ru_text = "🇷🇺 Ruscha" if lang == "uz" else "🇷🇺 Русский"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=uz_text, callback_data="jm_lang_uz")],
            [InlineKeyboardButton(text=ru_text, callback_data="jm_lang_ru")]
        ]
    )
    return keyboard


def get_statistics_keyboard(lang='uz'):
    """Generate statistics keyboard for junior manager with locale support"""
    daily_text = "📅 Kunlik statistika" if lang == "uz" else "📅 Дневная статистика"
    weekly_text = "📅 Haftalik statistika" if lang == "uz" else "📅 Недельная статистика"
    monthly_text = "📅 Oylik statistika" if lang == "uz" else "📅 Месячная статистика"
    performance_text = "📊 Samaradorlik" if lang == "uz" else "📊 Производительность"
    applications_text = "📋 Ariza statistikasi" if lang == "uz" else "📋 Статистика заявок"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=daily_text, callback_data="jm_stats_daily"),
            InlineKeyboardButton(text=weekly_text, callback_data="jm_stats_weekly")
        ],
        [
            InlineKeyboardButton(text=monthly_text, callback_data="jm_stats_monthly"),
            InlineKeyboardButton(text=performance_text, callback_data="jm_stats_performance")
        ],
        [
            InlineKeyboardButton(text=applications_text, callback_data="jm_stats_applications")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_junior_manager_main")
        ]
    ])
    return keyboard


def get_orders_keyboard(lang='uz'):
    """Generate orders keyboard for junior manager with locale support"""
    view_all_text = "📋 Barcha buyurtmalar" if lang == "uz" else "📋 Все заказы"
    new_orders_text = "🆕 Yangi buyurtmalar" if lang == "uz" else "🆕 Новые заказы"
    pending_orders_text = "⏳ Kutilayotgan buyurtmalar" if lang == "uz" else "⏳ Ожидающие заказы"
    completed_orders_text = "✅ Bajarilgan buyurtmalar" if lang == "uz" else "✅ Выполненные заказы"
    search_orders_text = "🔍 Buyurtma qidirish" if lang == "uz" else "🔍 Поиск заказа"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=view_all_text, callback_data="jm_orders_all"),
            InlineKeyboardButton(text=new_orders_text, callback_data="jm_orders_new")
        ],
        [
            InlineKeyboardButton(text=pending_orders_text, callback_data="jm_orders_pending"),
            InlineKeyboardButton(text=completed_orders_text, callback_data="jm_orders_completed")
        ],
        [
            InlineKeyboardButton(text=search_orders_text, callback_data="jm_orders_search")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_junior_manager_main")
        ]
    ])
    return keyboard


def get_junior_manager_back_keyboard(lang='uz'):
    """Junior manager uchun bosh menyuga qaytish klaviaturasi"""
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_text)]],
        resize_keyboard=True
    )


def get_client_search_keyboard(lang='uz'):
    """Alias for get_client_search_menu for compatibility"""
    return get_client_search_menu(lang)


def get_details_input_keyboard(app_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for details input"""
    keyboard = [
        [InlineKeyboardButton(
            text="❌ Bekor qilish",
            callback_data=f"jm_details_cancel_{app_id}"
        )]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_details_confirmation_keyboard(app_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for details confirmation"""
    keyboard = [
        [InlineKeyboardButton(
            text="📤 Controller-ga yuborish",
            callback_data=f"jm_details_forward_{app_id}"
        )],
        [InlineKeyboardButton(
            text="🔙 Inbox-ga qaytish",
            callback_data="jm_inbox_back"
        )]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_contact_note_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for contact note input"""
    cancel_button = InlineKeyboardButton(
        text="❌ Bekor qilish",
        callback_data="jm_back_to_application"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])


def get_controller_note_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for controller note input"""
    cancel_button = InlineKeyboardButton(
        text="❌ Bekor qilish",
        callback_data="jm_back_to_application"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])


def get_send_to_controller_confirmation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for send to controller confirmation"""
    confirm_button = InlineKeyboardButton(
        text="✅ Yuborish",
        callback_data="jm_confirm_send_to_controller"
    )
    edit_button = InlineKeyboardButton(
        text="📝 Tahrirlash",
        callback_data="jm_edit_controller_note"
    )
    cancel_button = InlineKeyboardButton(
        text="❌ Bekor qilish",
        callback_data="jm_back_to_application"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[confirm_button], [edit_button], [cancel_button]])


def get_edit_controller_note_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for editing controller note"""
    cancel_button = InlineKeyboardButton(
        text="❌ Bekor qilish",
        callback_data="jm_back_to_application"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])


def get_back_to_application_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for back to application"""
    back_button = InlineKeyboardButton(
        text="⬅️ Orqaga qaytish",
        callback_data="jm_back_to_application"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[back_button]])


def get_orders_navigation_keyboard(current_index: int, total_orders: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create navigation keyboard for orders"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="jm_prev_order"
        ))
    
    # Next button
    if current_index < total_orders - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="jm_next_order"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_clients_navigation_keyboard(current_index: int, total_clients: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create navigation keyboard for clients"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="client_prev"
        ))
    
    # Next button
    if current_index < total_clients - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="client_next"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_detailed_statistics_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for detailed statistics"""
    keyboard = [
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_statistics")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_workflow_management_menu_updated(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Updated workflow management menu keyboard for junior manager"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Arizalar kuzatuvi" if lang == 'uz' else "📋 Отслеживание заявок",
                callback_data="jm_workflow_tracking"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Vazifalar monitoringi" if lang == 'uz' else "📊 Мониторинг задач",
                callback_data="jm_workflow_monitoring"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Hisobotlar" if lang == 'uz' else "📈 Отчеты",
                callback_data="jm_workflow_reports"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Analitika" if lang == 'uz' else "📊 Аналитика",
                callback_data="jm_workflow_analytics"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                callback_data="back_to_main"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_tracking_menu_updated(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Updated application tracking menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="⏳ Kutilmoqda" if lang == 'uz' else "⏳ Ожидающие",
                callback_data="jm_track_pending"
            ),
            InlineKeyboardButton(
                text="🔄 Jarayonda" if lang == 'uz' else "🔄 В процессе",
                callback_data="jm_track_progress"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные",
                callback_data="jm_track_completed"
            ),
            InlineKeyboardButton(
                text="📋 Barchasi" if lang == 'uz' else "📋 Все",
                callback_data="jm_track_all"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                callback_data="jm_workflow_back"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_task_monitoring_menu_updated(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Updated task monitoring menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📅 Kunlik" if lang == 'uz' else "📅 Дневной",
                callback_data="jm_monitor_daily"
            ),
            InlineKeyboardButton(
                text="📊 Haftalik" if lang == 'uz' else "📊 Недельный",
                callback_data="jm_monitor_weekly"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Samaradorlik" if lang == 'uz' else "📈 Эффективность",
                callback_data="jm_monitor_performance"
            ),
            InlineKeyboardButton(
                text="📋 Barchasi" if lang == 'uz' else "📋 Все",
                callback_data="jm_monitor_all"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                callback_data="jm_workflow_back"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_junior_manager_main_keyboard_updated(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Updated junior manager main inline keyboard (used in some flows)."""
    keyboard = [
        [
            InlineKeyboardButton(text="🔌 Ulanish arizasi yaratish", callback_data="create_connection"),
            InlineKeyboardButton(text="🔧 Texnik xizmat yaratish", callback_data="create_technical")
        ],
        [
            InlineKeyboardButton(text="📥 Inbox", callback_data="view_inbox"),
            InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="view_orders")
        ],
        [
            InlineKeyboardButton(text="🔍 Mijoz qidiruv", callback_data="search_clients"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="view_statistics")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_client_search_menu_updated(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Updated client search menu"""
    keyboard = [
        [
            InlineKeyboardButton(text="📱 Telefon raqami", callback_data="search_by_phone"),
            InlineKeyboardButton(text="👤 Ism", callback_data="search_by_name")
        ],
        [
            InlineKeyboardButton(text="🆔 ID", callback_data="search_by_id"),
            InlineKeyboardButton(text="➕ Yangi mijoz", callback_data="create_new_client")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_priority_keyboard_updated(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Updated application priority keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(text="🟢 Past", callback_data="priority_low"),
            InlineKeyboardButton(text="🟡 O'rta", callback_data="priority_medium")
        ],
        [
            InlineKeyboardButton(text="🟠 Yuqori", callback_data="priority_high"),
            InlineKeyboardButton(text="🔴 Shoshilinch", callback_data="priority_urgent")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_details")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_confirmation_keyboard_updated(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Updated application confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_application"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_application")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)