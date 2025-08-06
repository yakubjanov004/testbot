from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_manager_main_keyboard(lang='uz'):
    """Generate main keyboard for manager with locale support, 2 buttons per row where possible"""
    # Ariza yaratish tugmalari (asosiy funksiya)
    create_connection_text = "🔌 Ulanish arizasi yaratish" if lang == "uz" else "🔌 Создать заявку на подключение"
    create_technical_text = "🔧 Texnik xizmat yaratish" if lang == "uz" else "🔧 Создать техническую заявку"
    
    # Arizalarni boshqarish
    view_applications_text = "📋 Arizalarni ko'rish" if lang == "uz" else "📋 Просмотр заявок"
    filter_applications_text = "🔍 Filtrlar" if lang == "uz" else "🔍 Фильтры"
    change_status_text = "🔄 Status o'zgartirish" if lang == "uz" else "🔄 Изменить статус"
    
    # Texnik biriktirish va xabarnomalar
    technician_assignment_text = "👨‍🔧 Texnik biriktirish" if lang == "uz" else "👨‍🔧 Назначить техника"
    notifications_text = "📢 Xabarnomalar" if lang == "uz" else "📢 Уведомления"
    
    # Hisobot va monitoring
    generate_report_text = "📊 Hisobot yaratish" if lang == "uz" else "📊 Создать отчет"
    staff_activity_text = "👥 Xodimlar faoliyati" if lang == "uz" else "👥 Активность сотрудников"
    
    # Real vaqtda kuzatish
    realtime_monitoring_text = "🕐 Real vaqtda kuzatish" if lang == "uz" else "🕐 Мониторинг в реальном времени"
    
    # Hujjatlar yaratish
    word_documents_text = "📄 Hujjatlar yaratish" if lang == "uz" else "📄 Создание документов"
    
    # Inbox va sozlamalar
    inbox_text = "📥 Inbox"
    change_language_text = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"
    
    # 2tadan qilib chiqadigan keyboard
    keyboard = [
        [KeyboardButton(text=create_connection_text), KeyboardButton(text=create_technical_text)],
        [KeyboardButton(text=view_applications_text), KeyboardButton(text=filter_applications_text)],
        [KeyboardButton(text=change_status_text), KeyboardButton(text=technician_assignment_text)],
        [KeyboardButton(text=notifications_text), KeyboardButton(text=generate_report_text)],
        [KeyboardButton(text=staff_activity_text), KeyboardButton(text=realtime_monitoring_text)],
        [KeyboardButton(text=word_documents_text), KeyboardButton(text=inbox_text)],
        [KeyboardButton(text=change_language_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_status_keyboard(statuses: list, application_id: int, lang='uz') -> InlineKeyboardMarkup:
    """Get status selection keyboard with application_id in callback and locale support"""
    status_texts = {
        'new': '🆕 Yangi' if lang == "uz" else '🆕 Новый',
        'in_progress': '⏳ Jarayonda' if lang == "uz" else '⏳ В процессе',
        'completed': '✅ Bajarilgan' if lang == "uz" else '✅ Выполнено',
        'cancelled': '❌ Bekor qilingan' if lang == "uz" else '❌ Отменено',
        'pending': '⏸️ Kutilmoqda' if lang == "uz" else '⏸️ Ожидает',
        'rejected': '🚫 Rad etilgan' if lang == "uz" else '🚫 Отклонено'
    }
    
    buttons = []
    for status in statuses:
        buttons.append(
            InlineKeyboardButton(
                text=status_texts.get(status, status),
                callback_data=f"status_{status}_{application_id}"
            )
        )
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons[:-1], [buttons[-1]]]  # Last button on separate row
    )
    return keyboard

def get_report_type_keyboard(lang='uz'):
    """Generate inline keyboard for report type selection with locale support"""
    report_word_text = "📄 Word formatida" if lang == "uz" else "📄 В формате Word"
    report_pdf_text = "📄 PDF formatida" if lang == "uz" else "📄 В формате PDF"
    
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=report_word_text,
            callback_data="report_word"
        ),
        InlineKeyboardButton(
            text=report_pdf_text,
            callback_data="report_pdf"
        )
    )
    builder.adjust(2)  # 2 buttons in first row
    return builder.as_markup()

def get_equipment_keyboard(equipment_list, lang='uz'):
    """Generate inline keyboard for equipment selection with locale support"""
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    builder = InlineKeyboardBuilder()
    for equipment in equipment_list:
        builder.add(InlineKeyboardButton(
            text=f"📦 {equipment['name']}",
            callback_data=f"equipment_{equipment['id']}"
        ))
    
    # Add back button
    builder.add(InlineKeyboardButton(
        text=back_text,
        callback_data="back_to_equipment_menu"
    ))
    
    builder.adjust(1)  # One button per row
    return builder.as_markup()

def get_assign_technician_keyboard(application_id, technicians, lang='uz'):
    """Generate inline keyboard for assigning a technician to an application with locale support"""
    builder = InlineKeyboardBuilder()
    for tech in technicians:
        text = f"👨‍🔧 {tech['full_name']}"
        builder.add(InlineKeyboardButton(
            text=text,
            callback_data=f"manager_assign_zayavka_{application_id}_{tech['id']}"
        ))
    builder.adjust(1)  # One button per row
    return builder.as_markup()

def get_back_inline_keyboard(lang='uz'):
    """Generate inline keyboard with a single 'Back' button with locale support"""
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=back_text,
        callback_data="back_to_assign_technician"
    ))
    return builder.as_markup()

def get_manager_filter_reply_keyboard(lang='uz'):
    status_text = "🟢 Status bo'yicha" if lang == 'uz' else "🟢 По статусу"
    date_text = "📅 Sana bo'yicha" if lang == 'uz' else "📅 По дате"
    tech_text = "👨‍🔧 Texnik biriktirilganligi bo'yicha" if lang == 'uz' else "👨‍🔧 По назначению техника"
    back_text = "◀️ Orqaga" if lang == 'uz' else "◀️ Назад"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=status_text)],
            [KeyboardButton(text=date_text)],
            [KeyboardButton(text=tech_text)],
            [KeyboardButton(text=back_text)]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_status_filter_inline_keyboard(lang='uz'):
    new_text = "🆕 Yangi" if lang == 'uz' else "🆕 Новый"
    in_progress_text = "⏳ Jarayonda" if lang == 'uz' else "⏳ В процессе"
    completed_text = "✅ Yakunlangan" if lang == 'uz' else "✅ Завершено"
    cancelled_text = "❌ Bekor qilingan" if lang == 'uz' else "❌ Отменено"
    all_text = "📋 Barchasi" if lang == 'uz' else "📋 Все"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=new_text, callback_data='filter_status_new'),
                InlineKeyboardButton(text=in_progress_text, callback_data='filter_status_in_progress')
            ],
            [
                InlineKeyboardButton(text=completed_text, callback_data='filter_status_completed'),
                InlineKeyboardButton(text=cancelled_text, callback_data='filter_status_cancelled')
            ],
            [
                InlineKeyboardButton(text=all_text, callback_data='filter_status_all'),
            ]
        ]
    )

def get_date_filter_inline_keyboard(lang='uz'):
    today_text = "📅 Bugun" if lang == 'uz' else "📅 Сегодня"
    yesterday_text = "🗓️ Kecha" if lang == 'uz' else "🗓️ Вчера"
    week_text = "📆 Bu hafta" if lang == 'uz' else "📆 На этой неделе"
    month_text = "🗓️ Bu oy" if lang == 'uz' else "🗓️ В этом месяце"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=today_text, callback_data='filter_date_today'),
                InlineKeyboardButton(text=yesterday_text, callback_data='filter_date_yesterday')
            ],
            [
                InlineKeyboardButton(text=week_text, callback_data='filter_date_week'),
                InlineKeyboardButton(text=month_text, callback_data='filter_date_month')
            ]
        ]
    )

def get_tech_filter_inline_keyboard(lang='uz'):
    assigned_text = "👨‍🔧 Biriktirilgan" if lang == 'uz' else "👨‍🔧 Назначенные"
    unassigned_text = "🚫 Biriktirilmagan" if lang == 'uz' else "🚫 Не назначенные"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=assigned_text, callback_data='filter_tech_assigned'),
                InlineKeyboardButton(text=unassigned_text, callback_data='filter_tech_unassigned')
            ]
        ]
    )

def get_pagination_inline_keyboard(page, total_pages, lang='uz', has_prev=True, has_next=True):
    prev_text = "Avvalgisi" if lang == 'uz' else "Предыдущая"
    next_text = "Keyingisi" if lang == 'uz' else "Следующая"
    back_text = "Orqaga" if lang == 'uz' else "Назад"
    buttons = []
    row = []
    if has_prev:
        row.append(InlineKeyboardButton(text=prev_text, callback_data=f'filter_page_prev_{page-1}'))
    if has_next:
        row.append(InlineKeyboardButton(text=next_text, callback_data=f'filter_page_next_{page+1}'))
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text=back_text, callback_data='filter_back')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_filtered_applications_keyboard(applications: list, lang='uz') -> InlineKeyboardMarkup:
    """Show filtered applications with clear button"""
    clear_text = "🔄 Tozalash" if lang == "uz" else "🔄 Очистить"
    
    buttons = []
    for app in applications:
        status_emoji = {
            'new': '🆕',
            'in_progress': '⏳',
            'completed': '✅',
            'cancelled': '❌'
        }.get(app.get('status', 'new'), '📋')
        
        text = f"{status_emoji} ID: {app['id']} - {app.get('user_name', '-')}"
        buttons.append([InlineKeyboardButton(
            text=text,
            callback_data=f"view_application_{app['id']}"
        )])
    
    # Add clear filter button
    buttons.append([InlineKeyboardButton(
        text=clear_text, 
        callback_data="filter_clear"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_filter_results_keyboard(page: int, total_pages: int, has_next: bool, has_prev: bool, lang='uz') -> InlineKeyboardMarkup:
    """Filtered results pagination keyboard with locale support"""
    prev_text = "◀️ Oldingi" if lang == "uz" else "◀️ Предыдущая"
    next_text = "Keyingi ▶️" if lang == "uz" else "Следующая ▶️"
    clear_text = "🔄 Tozalash" if lang == "uz" else "🔄 Очистить"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    buttons = []
    
    # Navigation buttons
    nav_row = []
    if has_prev:
        nav_row.append(InlineKeyboardButton(text=prev_text, callback_data=f"filter_page_{page-1}"))
    if has_next:
        nav_row.append(InlineKeyboardButton(text=next_text, callback_data=f"filter_page_{page+1}"))
    
    if nav_row:
        buttons.append(nav_row)
    
    # Page info
    if total_pages > 1:
        buttons.append([
            InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="filter_page_info")
        ])
    
    # Control buttons
    control_row = [
        InlineKeyboardButton(text=clear_text, callback_data="filter_clear"),
        InlineKeyboardButton(text=back_text, callback_data="back_to_main_menu")
    ]
    buttons.append(control_row)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_confirmation_keyboard(action_type="confirm", lang='uz') -> InlineKeyboardMarkup:
    """Generate confirmation keyboard with locale support"""
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отменить"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data=f"confirm_{action_type}"),
            InlineKeyboardButton(text=cancel_text, callback_data=f"cancel_{action_type}")
        ]
    ])
    return keyboard

def get_application_actions_keyboard(application_id: int, lang='uz') -> InlineKeyboardMarkup:
    """Generate application action buttons with locale support"""
    change_status_text = "📊 Holatni o'zgartirish" if lang == "uz" else "📊 Изменить статус"
    assign_responsible_text = "👨‍🔧 Texnik biriktirish" if lang == "uz" else "👨‍🔧 Назначить техника"
    view_text = "👁️ Ko'rish" if lang == "uz" else "👁️ Просмотр"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=change_status_text, 
                callback_data=f"app_change_status_{application_id}"
            ),
            InlineKeyboardButton(
                text=assign_responsible_text, 
                callback_data=f"app_assign_tech_{application_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text=view_text, 
                callback_data=f"app_view_details_{application_id}"
            ),
            InlineKeyboardButton(
                text=back_text, 
                callback_data="back_to_applications"
            )
        ]
    ])
    return keyboard

def get_manager_language_keyboard(lang='uz') -> InlineKeyboardMarkup:
    """Language selection keyboard for manager"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="manager_lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="manager_lang_ru")
        ]
    ])
    return keyboard

def get_manager_back_keyboard(lang='uz'):
    """Manager uchun bosh menyuga qaytish klaviaturasi"""
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_text)]],
        resize_keyboard=True
    )

def get_manager_view_applications_keyboard(lang='uz'):
    view_all_text = "📋 Hammasini ko'rish" if lang == 'uz' else "📋 Посмотреть все"
    by_id_text = "🔎 ID bo'yicha ko'rish" if lang == 'uz' else "🔎 По ID"
    back_text = "◀️ Orqaga" if lang == 'uz' else "◀️ Назад"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=view_all_text)],
            [KeyboardButton(text=by_id_text)],
            [KeyboardButton(text=back_text)]
        ],
        resize_keyboard=True
    )

def get_staff_activity_keyboard(lang='uz'):
    """Xodimlar faoliyati uchun reply keyboard"""
    online_text = "🟢 Onlayn xodimlar" if lang == "uz" else "🟢 Сотрудники онлайн"
    performance_text = "📊 Samaradorlik" if lang == "uz" else "📊 Производительность"
    workload_text = "📋 Ish yuki" if lang == "uz" else "📋 Рабочая нагрузка"
    attendance_text = "📅 Davomat" if lang == "uz" else "📅 Посещаемость"
    junior_work_text = "👨‍💼 Kichik menejerlar ishi" if lang == "uz" else "👨‍💼 Работа младших менеджеров"
    back_text = "🔙 Orqaga" if lang == "uz" else "🔙 Назад"

    keyboard = [
        [KeyboardButton(text=online_text)],
        [KeyboardButton(text=performance_text)],
        [KeyboardButton(text=workload_text)],
        [KeyboardButton(text=attendance_text)],
        [KeyboardButton(text=junior_work_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_inbox_keyboard(lang='uz'):
    """Inbox uchun keyboard"""
    new_messages_text = "🆕 Yangi xabarlar" if lang == "uz" else "🆕 Новые сообщения"
    read_messages_text = "✅ O'qilgan xabarlar" if lang == "uz" else "✅ Прочитанные сообщения"
    urgent_messages_text = "🚨 Shoshilinch xabarlar" if lang == "uz" else "🚨 Срочные сообщения"
    client_messages_text = "👤 Mijoz xabarlari" if lang == "uz" else "👤 Сообщения клиентов"
    system_messages_text = "⚙️ Tizim xabarlari" if lang == "uz" else "⚙️ Системные сообщения"
    back_text = "🔙 Orqaga" if lang == "uz" else "🔙 Назад"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=new_messages_text,
                callback_data="inbox_new"
            )
        ],
        [
            InlineKeyboardButton(
                text=read_messages_text,
                callback_data="inbox_read"
            )
        ],
        [
            InlineKeyboardButton(
                text=urgent_messages_text,
                callback_data="inbox_urgent"
            )
        ],
        [
            InlineKeyboardButton(
                text=client_messages_text,
                callback_data="inbox_client"
            )
        ],
        [
            InlineKeyboardButton(
                text=system_messages_text,
                callback_data="inbox_system"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Yangi zayavkalar" if lang == 'uz' else "📝 Новые заявки",
                callback_data="inbox_zayavka"
            )
        ],
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="inbox_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_reports_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Reports menu keyboard for manager"""
    daily_text = "📅 Kunlik" if lang == "uz" else "📅 Ежедневный"
    weekly_text = "📅 Haftalik" if lang == "uz" else "📅 Еженедельный"
    monthly_text = "📅 Oylik" if lang == "uz" else "📅 Ежемесячный"
    technician_text = "👨‍🔧 Texniklar" if lang == "uz" else "👨‍🔧 Техники"
    status_text = "📊 Status" if lang == "uz" else "📊 Статус"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=daily_text,
                callback_data="report_daily"
            )
        ],
        [
            InlineKeyboardButton(
                text=weekly_text,
                callback_data="report_weekly"
            )
        ],
        [
            InlineKeyboardButton(
                text=monthly_text,
                callback_data="report_monthly"
            )
        ],
        [
            InlineKeyboardButton(
                text=technician_text,
                callback_data="report_technician"
            )
        ],
        [
            InlineKeyboardButton(
                text=status_text,
                callback_data="report_status"
            )
        ],
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="manager_back_to_main"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
def get_application_keyboard(application_id):
    """Application actions keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_{application_id}")],
            [InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{application_id}")],
            [InlineKeyboardButton(text="👁️ Batafsil", callback_data=f"view_{application_id}")]
        ]
    )
    return keyboard

def get_notifications_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Generate notifications keyboard for manager"""
    send_staff_text = "👤 Xodimga xabar yuborish" if lang == "uz" else "👤 Отправить сообщение сотруднику"
    send_broadcast_text = "📢 Barcha xodimlarga xabar" if lang == "uz" else "📢 Сообщение всем сотрудникам"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=send_staff_text, callback_data="send_staff_notification")],
        [InlineKeyboardButton(text=send_broadcast_text, callback_data="send_broadcast_notification")],
        [InlineKeyboardButton(text=back_text, callback_data="back_to_main_menu")]
    ])
    return keyboard

def get_word_document_type_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Generate word document type keyboard for manager"""
    work_order_text = "📋 Ish buyrug'i" if lang == "uz" else "📋 Рабочий приказ"
    manager_report_text = "📊 Menejer hisoboti" if lang == "uz" else "📊 Отчет менеджера"
    quality_control_text = "✅ Kvalitet nazorati" if lang == "uz" else "✅ Контроль качества"
    work_time_report_text = "⏰ Ishlash vaqti hisoboti" if lang == "uz" else "⏰ Отчет рабочего времени"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=work_order_text, callback_data="word_doc_work_order")],
        [InlineKeyboardButton(text=manager_report_text, callback_data="word_doc_manager_report")],
        [InlineKeyboardButton(text=quality_control_text, callback_data="word_doc_quality_control")],
        [InlineKeyboardButton(text=work_time_report_text, callback_data="word_doc_work_time_report")],
        [InlineKeyboardButton(text=back_text, callback_data="back_to_manager_main")]
    ])
    return keyboard
    if lang == 'uz':
        buttons = [
            [InlineKeyboardButton(text="📢 Barchaga yuborish", callback_data="notification_send_all")],
            [InlineKeyboardButton(text="👥 Rolga yuborish", callback_data="notification_send_role")],
            [InlineKeyboardButton(text="👤 Shaxsiy yuborish", callback_data="notification_send_individual")],
            [InlineKeyboardButton(text="🕓 Tarix", callback_data="notification_history")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="manager_main_menu")]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="📢 Отправить всем", callback_data="notification_send_all")],
            [InlineKeyboardButton(text="👥 Отправить по роли", callback_data="notification_send_role")],
            [InlineKeyboardButton(text="👤 Личное сообщение", callback_data="notification_send_individual")],
            [InlineKeyboardButton(text="🕓 История", callback_data="notification_history")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="manager_main_menu")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_language_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Manager uchun til tanlash inline keyboard"""
    uz_text = "🇺🇿 O‘zbekcha" if lang == "uz" else "🇺🇿 Узбекский"
    ru_text = "🇷🇺 Ruscha" if lang == "uz" else "🇷🇺 Русский"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=uz_text, callback_data="lang_uz")],
            [InlineKeyboardButton(text=ru_text, callback_data="lang_ru")]
        ]
    )
    return keyboard

def get_manager_word_documents_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Manager uchun Word hujjatlari yaratish inline keyboard"""
    contract_text = "📄 Shartnoma yaratish" if lang == "uz" else "📄 Создать договор"
    invoice_text = "🧾 Hisob-faktura yaratish" if lang == "uz" else "🧾 Создать счет-фактуру"
    report_text = "📊 Hisobot yaratish" if lang == "uz" else "📊 Создать отчет"
    certificate_text = "📜 Sertifikat yaratish" if lang == "uz" else "📜 Создать сертификат"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=contract_text, callback_data="manager_create_contract")],
            [InlineKeyboardButton(text=invoice_text, callback_data="manager_create_invoice")],
            [InlineKeyboardButton(text=report_text, callback_data="manager_create_report")],
            [InlineKeyboardButton(text=certificate_text, callback_data="manager_create_certificate")],
            [InlineKeyboardButton(text=back_text, callback_data="manager_back_to_main")]
        ]
    )
    return keyboard

def get_manager_filters_keyboard(lang='uz'):
    """Generate filters keyboard for manager with locale support"""
    region_text = "🌍 Hudud bo'yicha" if lang == "uz" else "🌍 По региону"
    status_text = "📊 Holat bo'yicha" if lang == "uz" else "📊 По статусу"
    date_text = "📅 Sana bo'yicha" if lang == "uz" else "📅 По дате"
    priority_text = "⚡ Ustuvorlik bo'yicha" if lang == "uz" else "⚡ По приоритету"
    type_text = "📋 Ariza turi bo'yicha" if lang == "uz" else "📋 По типу заявки"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=region_text, callback_data="filter_by_region"),
            InlineKeyboardButton(text=status_text, callback_data="filter_by_status")
        ],
        [
            InlineKeyboardButton(text=date_text, callback_data="filter_by_date"),
            InlineKeyboardButton(text=priority_text, callback_data="filter_by_priority")
        ],
        [
            InlineKeyboardButton(text=type_text, callback_data="filter_by_type")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_manager_main")
        ]
    ])
    return keyboard

def get_manager_notifications_keyboard(lang='uz'):
    """Generate notifications keyboard for manager with locale support"""
    new_text = "🆕 Yangi bildirishnomalar" if lang == "uz" else "🆕 Новые уведомления"
    read_text = "✅ O'qilgan bildirishnomalar" if lang == "uz" else "✅ Прочитанные уведомления"
    urgent_text = "🚨 Shoshilinch bildirishnomalar" if lang == "uz" else "🚨 Срочные уведомления"
    all_text = "📋 Barcha bildirishnomalar" if lang == "uz" else "📋 Все уведомления"
    settings_text = "⚙️ Bildirishnoma sozlamalari" if lang == "uz" else "⚙️ Настройки уведомлений"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=new_text, callback_data="notifications_new"),
            InlineKeyboardButton(text=read_text, callback_data="notifications_read")
        ],
        [
            InlineKeyboardButton(text=urgent_text, callback_data="notifications_urgent"),
            InlineKeyboardButton(text=all_text, callback_data="notifications_all")
        ],
        [
            InlineKeyboardButton(text=settings_text, callback_data="notifications_settings")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_manager_main")
        ]
    ])
    return keyboard

def get_manager_search_keyboard(lang='uz'):
    """Generate search keyboard for manager with locale support"""
    search_text = "🔍 Qidiruv" if lang == "uz" else "🔍 Поиск"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = [
        [KeyboardButton(text=search_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
