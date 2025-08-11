from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict, Any


def get_controller_main_menu(lang='uz'):
    """Controller uchun asosiy menyu"""
    texts = {
        'uz': {
            'inbox': '📥 Inbox',
            'view_applications': '📋 Arizalarni ko\'rish',
            'create_connection': '🔌 Ulanish arizasi yaratish',
            'create_technical': '🔧 Texnik xizmat yaratish',
            'realtime_monitoring': '🕐 Real vaqtda kuzatish',
            'monitoring': '📊 Monitoring',
            'staff_activity': '👥 Xodimlar faoliyati',
            'export': '📤 Export',
            'change_language': '🌐 Tilni o\'zgartirish'
        },
        'ru': {
            'inbox': '📥 Входящие',
            'view_applications': '📋 Просмотр заявок',
            'create_connection': '🔌 Создать заявку на подключение',
            'create_technical': '🔧 Создать техническое обслуживание',
            'realtime_monitoring': '🕐 Мониторинг в реальном времени',
            'monitoring': '📊 Мониторинг',
            'staff_activity': '👥 Активность сотрудников',
            'export': '📤 Экспорт',
            'change_language': '🌐 Изменить язык'
        }
    }
    
    t = texts.get(lang, texts['uz'])
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t['inbox']),
                KeyboardButton(text=t['view_applications'])
            ],
            [
                KeyboardButton(text=t['create_connection']),
                KeyboardButton(text=t['create_technical'])
            ],
            [
                KeyboardButton(text=t['realtime_monitoring']),
                KeyboardButton(text=t['monitoring'])
            ],
            [
                KeyboardButton(text=t['staff_activity']),
                KeyboardButton(text=t['export'])
            ],
            [
                KeyboardButton(text=t['change_language'])
            ]
        ],
        resize_keyboard=True
    )
    
    return keyboard


def get_back_button(lang='uz'):
    """Orqaga qaytish tugmasi"""
    texts = {
        'uz': '⬅️ Orqaga',
        'ru': '⬅️ Назад'
    }
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.get(lang, texts['uz']))]
        ],
        resize_keyboard=True
    )
    
    return keyboard


def get_back_to_main_menu(lang='uz'):
    """Asosiy menyuga qaytish tugmasi"""
    texts = {
        'uz': '🏠 Asosiy menyu',
        'ru': '🏠 Главное меню'
    }
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.get(lang, texts['uz']))]
        ],
        resize_keyboard=True
    )
    
    return keyboard


def get_controller_workflow_keyboard(request_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Controller uchun workflow tugmalari"""
    if lang == 'uz':
        keyboard = [
            [
                InlineKeyboardButton(text="📋 Batafsil", callback_data=f"ctrl_view_{request_id}"),
                InlineKeyboardButton(text="👨‍🔧 Texnikka tayinlash", callback_data=f"ctrl_assign_{request_id}")
            ],
            [
                InlineKeyboardButton(text="📊 Monitoring", callback_data=f"ctrl_monitor_{request_id}"),
                InlineKeyboardButton(text="🔄 O'tkazish", callback_data=f"ctrl_transfer_{request_id}")
            ],
            [
                InlineKeyboardButton(text="⚡ Muhimlikni o'zgartirish", callback_data=f"ctrl_priority_{request_id}")
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text="📋 Подробно", callback_data=f"ctrl_view_{request_id}"),
                InlineKeyboardButton(text="👨‍🔧 Назначить технику", callback_data=f"ctrl_assign_{request_id}")
            ],
            [
                InlineKeyboardButton(text="📊 Мониторинг", callback_data=f"ctrl_monitor_{request_id}"),
                InlineKeyboardButton(text="🔄 Передать", callback_data=f"ctrl_transfer_{request_id}")
            ],
            [
                InlineKeyboardButton(text="⚡ Изменить приоритет", callback_data=f"ctrl_priority_{request_id}")
            ]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_technician_assignment_keyboard(technicians: List[Dict], request_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Texnik tayinlash uchun keyboard"""
    keyboard = []
    
    for tech in technicians[:8]:  # Maksimal 8 ta
        workload_emoji = "🟢" if tech.get('active_requests', 0) == 0 else "🟡" if tech.get('active_requests', 0) < 3 else "🔴"
        button_text = f"{workload_emoji} {tech['full_name']} ({tech.get('active_requests', 0)})"
        
        keyboard.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"ctrl_select_tech_{request_id}_{tech['id']}"
            )
        ])
    
    # Cancel button
    cancel_text = "❌ Bekor qilish" if lang == 'uz' else "❌ Отмена"
    keyboard.append([
        InlineKeyboardButton(text=cancel_text, callback_data=f"ctrl_cancel_assign_{request_id}")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_priority_selection_keyboard(request_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Muhimlik darajasini tanlash uchun keyboard"""
    if lang == 'uz':
        keyboard = [
            [
                InlineKeyboardButton(text="🟢 Past", callback_data=f"ctrl_set_priority_{request_id}_low"),
                InlineKeyboardButton(text="🟡 O'rta", callback_data=f"ctrl_set_priority_{request_id}_medium")
            ],
            [
                InlineKeyboardButton(text="🟠 Yuqori", callback_data=f"ctrl_set_priority_{request_id}_high"),
                InlineKeyboardButton(text="🔴 Shoshilinch", callback_data=f"ctrl_set_priority_{request_id}_urgent")
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"ctrl_cancel_priority_{request_id}")
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text="🟢 Низкий", callback_data=f"ctrl_set_priority_{request_id}_low"),
                InlineKeyboardButton(text="🟡 Средний", callback_data=f"ctrl_set_priority_{request_id}_medium")
            ],
            [
                InlineKeyboardButton(text="🟠 Высокий", callback_data=f"ctrl_set_priority_{request_id}_high"),
                InlineKeyboardButton(text="🔴 Срочный", callback_data=f"ctrl_set_priority_{request_id}_urgent")
            ],
            [
                InlineKeyboardButton(text="❌ Отмена", callback_data=f"ctrl_cancel_priority_{request_id}")
            ]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_transfer_options_keyboard(request_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Zayavkani o'tkazish uchun keyboard"""
    if lang == 'uz':
        keyboard = [
            [
                InlineKeyboardButton(text="👨‍💼 Menejerga", callback_data=f"ctrl_transfer_{request_id}_manager"),
                InlineKeyboardButton(text="👨‍💼 Jr. Menejerga", callback_data=f"ctrl_transfer_{request_id}_junior_manager")
            ],
            [
                InlineKeyboardButton(text="📞 Call-markazga", callback_data=f"ctrl_transfer_{request_id}_call_center"),
                InlineKeyboardButton(text="📦 Omborga", callback_data=f"ctrl_transfer_{request_id}_warehouse")
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"ctrl_cancel_transfer_{request_id}")
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text="👨‍💼 Менеджеру", callback_data=f"ctrl_transfer_{request_id}_manager"),
                InlineKeyboardButton(text="👨‍💼 Мл. менеджеру", callback_data=f"ctrl_transfer_{request_id}_junior_manager")
            ],
            [
                InlineKeyboardButton(text="📞 Call-центру", callback_data=f"ctrl_transfer_{request_id}_call_center"),
                InlineKeyboardButton(text="📦 Складу", callback_data=f"ctrl_transfer_{request_id}_warehouse")
            ],
            [
                InlineKeyboardButton(text="❌ Отмена", callback_data=f"ctrl_cancel_transfer_{request_id}")
            ]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def orders_control_menu(lang='uz'):
    """Buyurtmalar nazorati menyusi"""
    if lang == 'uz':
        keyboard = [
            [KeyboardButton(text="🆕 Yangi buyurtmalar"), KeyboardButton(text="⏳ Kutilayotgan")],
            [KeyboardButton(text="🔴 Muammoli buyurtmalar"), KeyboardButton(text="📊 Buyurtmalar hisoboti")],
            [KeyboardButton(text="🏠 Bosh menyu")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="🆕 Новые заказы"), KeyboardButton(text="⏳ Ожидающие")],
            [KeyboardButton(text="🔴 Проблемные заказы"), KeyboardButton(text="📊 Отчет по заказам")],
            [KeyboardButton(text="🏠 Главное меню")]
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def technicians_menu(lang='uz'):
    """Texniklar menyusi"""
    if lang == 'uz':
        keyboard = [
            [KeyboardButton(text="📋 Texniklar ro'yxati"), KeyboardButton(text="📊 Texniklar samaradorligi")],
            [KeyboardButton(text="🎯 Vazifa tayinlash"), KeyboardButton(text="📈 Texniklar hisoboti")],
            [KeyboardButton(text="🏠 Bosh menyu")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📋 Список техников"), KeyboardButton(text="📊 Эффективность техников")],
            [KeyboardButton(text="🎯 Назначение задач"), KeyboardButton(text="📈 Отчет по техникам")],
            [KeyboardButton(text="🏠 Главное меню")]
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def quality_control_menu(lang='uz'):
    """Sifat nazorati menyusi"""
    if lang == 'uz':
        keyboard = [
            [KeyboardButton(text="💬 Mijoz fikrlari"), KeyboardButton(text="⚠️ Muammoli holatlar")],
            [KeyboardButton(text="📊 Sifat baholash"), KeyboardButton(text="📈 Sifat tendensiyalari")],
            [KeyboardButton(text="📋 Sifat hisoboti"), KeyboardButton(text="🏠 Bosh menyu")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="💬 Отзывы клиентов"), KeyboardButton(text="⚠️ Проблемные ситуации")],
            [KeyboardButton(text="📊 Оценка качества"), KeyboardButton(text="📈 Тенденции качества")],
            [KeyboardButton(text="📋 Отчет по качеству"), KeyboardButton(text="🏠 Главное меню")]
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def reports_menu(lang='uz'):
    """Hisobotlar menyusi"""
    if lang == 'uz':
        keyboard = [
            [KeyboardButton(text="📈 Tizim hisoboti"), KeyboardButton(text="👨‍🔧 Texniklar hisoboti")],
            [KeyboardButton(text="⭐ Sifat hisoboti"), KeyboardButton(text="📅 Kunlik hisobot")],
            [KeyboardButton(text="📊 Haftalik hisobot"), KeyboardButton(text="🏠 Bosh menyu")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📈 Системный отчет"), KeyboardButton(text="👨‍🔧 Отчет по техникам")],
            [KeyboardButton(text="⭐ Отчет по качеству"), KeyboardButton(text="📅 Ежедневный отчет")],
            [KeyboardButton(text="📊 Еженедельный отчет"), KeyboardButton(text="🏠 Главное меню")]
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def language_keyboard():
    """Til tanlash klaviaturasi"""
    keyboard = [
        [KeyboardButton(text="🇺🇿 O'zbek tili"), KeyboardButton(text="🇷🇺 Русский язык")],
    ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def order_priority_keyboard(lang='uz'):
    """Buyurtma ustuvorligi klaviaturasi"""
    if lang == 'uz':
        keyboard = [
            [InlineKeyboardButton(text="🔴 Yuqori", callback_data="set_priority_high")],
            [InlineKeyboardButton(text="🟡 O'rta", callback_data="set_priority_medium")],
            [InlineKeyboardButton(text="🟢 Past", callback_data="set_priority_low")],
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="controllers_back")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(text="🔴 Высокий", callback_data="set_priority_high")],
            [InlineKeyboardButton(text="🟡 Средний", callback_data="set_priority_medium")],
            [InlineKeyboardButton(text="🟢 Низкий", callback_data="set_priority_low")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="controllers_back")]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def technician_assignment_keyboard(lang='uz', technicians=None):
    """Texnik tayinlash klaviaturasi"""
    keyboard = []
    
    if technicians:
        for tech in technicians[:10]:  # Maksimal 10 ta texnik
            button_text = f"👨‍🔧 {tech['full_name']} ({tech.get('active_tasks', 0)})"
            keyboard.append([InlineKeyboardButton(
                text=button_text, 
                callback_data=f"assign_tech_{tech['id']}"
            )])
    
    back_text = "◀️ Orqaga" if lang == 'uz' else "◀️ Назад"
    keyboard.append([InlineKeyboardButton(text=back_text, callback_data="controllers_back")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def back_to_controllers_menu(lang='uz'):
    """Controllers menyusiga qaytish"""
    if lang == 'uz':
        keyboard = [
            [KeyboardButton(text="🏠 Bosh menyu")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="🏠 Главное меню")]
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def quality_control_detailed_menu(lang='uz'):
    """Batafsil sifat nazorati menyusi"""
    if lang == 'uz':
        keyboard = [
            [InlineKeyboardButton(text="💬 Mijoz fikrlari", callback_data="quality_customer_feedback")],
            [InlineKeyboardButton(text="⚠️ Hal etilmagan muammolar", callback_data="quality_unresolved_issues")],
            [InlineKeyboardButton(text="📊 Xizmat sifatini baholash", callback_data="quality_service_assessment")],
            [InlineKeyboardButton(text="📈 Sifat tendensiyalari", callback_data="quality_trends")],
            [InlineKeyboardButton(text="📋 Sifat hisoboti", callback_data="quality_reports")],
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="controllers_back")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(text="💬 Отзывы клиентов", callback_data="quality_customer_feedback")],
            [InlineKeyboardButton(text="⚠️ Нерешенные проблемы", callback_data="quality_unresolved_issues")],
            [InlineKeyboardButton(text="📊 Оценка качества услуг", callback_data="quality_service_assessment")],
            [InlineKeyboardButton(text="📈 Тенденции качества", callback_data="quality_trends")],
            [InlineKeyboardButton(text="📋 Отчет по качеству", callback_data="quality_reports")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="controllers_back")]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def feedback_detailed_filter_menu(lang='uz'):
    """Fikrlarni filtrlash menyusi"""
    if lang == 'uz':
        keyboard = [
            [InlineKeyboardButton(text="⭐⭐⭐⭐⭐ (5)", callback_data="feedback_filter_5")],
            [InlineKeyboardButton(text="⭐⭐⭐⭐ (4)", callback_data="feedback_filter_4")],
            [InlineKeyboardButton(text="⭐⭐⭐ (3)", callback_data="feedback_filter_3")],
            [InlineKeyboardButton(text="⭐⭐ (2)", callback_data="feedback_filter_2")],
            [InlineKeyboardButton(text="⭐ (1)", callback_data="feedback_filter_1")],
            [InlineKeyboardButton(text="📋 Barcha fikrlar", callback_data="feedback_filter_all")],
            [InlineKeyboardButton(text="🕒 So'nggi fikrlar", callback_data="feedback_filter_recent")],
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="quality_control")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(text="⭐⭐⭐⭐⭐ (5)", callback_data="feedback_filter_5")],
            [InlineKeyboardButton(text="⭐⭐⭐⭐ (4)", callback_data="feedback_filter_4")],
            [InlineKeyboardButton(text="⭐⭐⭐ (3)", callback_data="feedback_filter_3")],
            [InlineKeyboardButton(text="⭐⭐ (2)", callback_data="feedback_filter_2")],
            [InlineKeyboardButton(text="⭐ (1)", callback_data="feedback_filter_1")],
            [InlineKeyboardButton(text="📋 Все отзывы", callback_data="feedback_filter_all")],
            [InlineKeyboardButton(text="🕒 Последние отзывы", callback_data="feedback_filter_recent")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="quality_control")]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def technical_service_assignment_keyboard(request_id, technicians=None, lang='uz'):
    """Technical service assignment keyboard"""
    keyboard = []
    
    if technicians:
        for tech in technicians[:10]:  # Maximum 10 technicians
            button_text = f"👨‍🔧 {tech['full_name']}"
            if tech.get('active_tasks'):
                button_text += f" ({tech['active_tasks']})"
            
            keyboard.append([InlineKeyboardButton(
                text=button_text, 
                callback_data=f"assign_technical_to_technician_{tech['id']}_{request_id}"
            )])
    
    back_text = "◀️ Orqaga" if lang == 'uz' else "◀️ Назад"
    keyboard.append([InlineKeyboardButton(text=back_text, callback_data="controllers_back")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_quality_keyboard(lang='uz'):
    """Generate quality keyboard for controller with locale support"""
    quality_issues_text = "🔴 Sifat muammolari" if lang == "uz" else "🔴 Проблемы качества"
    quality_metrics_text = "📊 Sifat ko'rsatkichlari" if lang == "uz" else "📊 Показатели качества"
    quality_reports_text = "📋 Sifat hisobotlari" if lang == "uz" else "📋 Отчеты качества"
    quality_settings_text = "⚙️ Sifat sozlamalari" if lang == "uz" else "⚙️ Настройки качества"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=quality_issues_text, callback_data="ctrl_quality_issues"),
            InlineKeyboardButton(text=quality_metrics_text, callback_data="ctrl_quality_metrics")
        ],
        [
            InlineKeyboardButton(text=quality_reports_text, callback_data="ctrl_quality_reports"),
            InlineKeyboardButton(text=quality_settings_text, callback_data="ctrl_quality_settings")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

def get_controller_back_keyboard(lang='uz'):
    """Controller uchun bosh menyuga qaytish klaviaturasi"""
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_text)]],
        resize_keyboard=True
    )

def get_technician_keyboard(lang='uz'):
    """Generate technician keyboard for controller with locale support"""
    view_all_text = "📋 Barcha texniklar" if lang == "uz" else "📋 Все техники"
    active_text = "🟢 Faol texniklar" if lang == "uz" else "🟢 Активные техники"
    busy_text = "🟡 Band texniklar" if lang == "uz" else "🟡 Занятые техники"
    performance_text = "📊 Samaradorlik" if lang == "uz" else "📊 Производительность"
    assignments_text = "📋 Tayinlashlar" if lang == "uz" else "📋 Назначения"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=view_all_text, callback_data="ctrl_tech_all"),
            InlineKeyboardButton(text=active_text, callback_data="ctrl_tech_active")
        ],
        [
            InlineKeyboardButton(text=busy_text, callback_data="ctrl_tech_busy"),
            InlineKeyboardButton(text=performance_text, callback_data="ctrl_tech_performance")
        ],
        [
            InlineKeyboardButton(text=assignments_text, callback_data="ctrl_tech_assignments")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

def get_technical_service_keyboard(lang='uz'):
    """Generate technical service keyboard for controller with locale support"""
    create_service_text = "🔧 Texnik xizmat yaratish" if lang == "uz" else "🔧 Создать техническую услугу"
    view_services_text = "📋 Texnik xizmatlarni ko'rish" if lang == "uz" else "📋 Просмотр технических услуг"
    assign_technician_text = "👨‍🔧 Texnik tayinlash" if lang == "uz" else "👨‍🔧 Назначить техника"
    service_reports_text = "📊 Xizmat hisobotlari" if lang == "uz" else "📊 Отчеты услуг"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=create_service_text, callback_data="ctrl_service_create"),
            InlineKeyboardButton(text=view_services_text, callback_data="ctrl_service_view")
        ],
        [
            InlineKeyboardButton(text=assign_technician_text, callback_data="ctrl_service_assign"),
            InlineKeyboardButton(text=service_reports_text, callback_data="ctrl_service_reports")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

def get_staff_creation_keyboard(lang='uz'):
    """Generate staff creation keyboard for controller with locale support"""
    create_connection_text = "🔌 Ulanish arizasi yaratish" if lang == "uz" else "🔌 Создать заявку на подключение"
    create_technical_text = "🔧 Texnik xizmat yaratish" if lang == "uz" else "🔧 Создать техническую заявку"
    view_applications_text = "📋 Arizalarni ko'rish" if lang == "uz" else "📋 Просмотр заявок"
    assign_technician_text = "👨‍🔧 Texnik tayinlash" if lang == "uz" else "👨‍🔧 Назначить техника"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=create_connection_text, callback_data="ctrl_staff_connection"),
            InlineKeyboardButton(text=create_technical_text, callback_data="ctrl_staff_technical")
        ],
        [
            InlineKeyboardButton(text=view_applications_text, callback_data="ctrl_staff_view"),
            InlineKeyboardButton(text=assign_technician_text, callback_data="ctrl_staff_assign")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

def get_monitoring_keyboard(lang='uz'):
    """Generate monitoring keyboard for controller with locale support"""
    system_status_text = "📊 Tizim holati" if lang == "uz" else "📊 Состояние системы"
    performance_text = "📈 Samaradorlik" if lang == "uz" else "📈 Производительность"
    alerts_text = "🚨 Ogohlantirishlar" if lang == "uz" else "🚨 Уведомления"
    reports_text = "📋 Hisobotlar" if lang == "uz" else "📋 Отчеты"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=system_status_text, callback_data="ctrl_monitor_system"),
            InlineKeyboardButton(text=performance_text, callback_data="ctrl_monitor_performance")
        ],
        [
            InlineKeyboardButton(text=alerts_text, callback_data="ctrl_monitor_alerts"),
            InlineKeyboardButton(text=reports_text, callback_data="ctrl_monitor_reports")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

def get_realtime_monitoring_keyboard(lang='uz'):
    """Generate realtime monitoring keyboard for controller with locale support"""
    live_status_text = "🟢 Jonli holat" if lang == "uz" else "🟢 Живое состояние"
    recent_activities_text = "📋 So'nggi faoliyatlar" if lang == "uz" else "📋 Последние действия"
    alerts_text = "🚨 Ogohlantirishlar" if lang == "uz" else "🚨 Уведомления"
    performance_text = "📈 Samaradorlik" if lang == "uz" else "📈 Производительность"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=live_status_text, callback_data="ctrl_realtime_status"),
            InlineKeyboardButton(text=recent_activities_text, callback_data="ctrl_realtime_activities")
        ],
        [
            InlineKeyboardButton(text=alerts_text, callback_data="ctrl_realtime_alerts"),
            InlineKeyboardButton(text=performance_text, callback_data="ctrl_realtime_performance")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

# Application Creator callbacks
def get_application_creator_keyboard(lang='uz'):
    """Generate application creator keyboard for controller"""
    search_phone_text = "📞 Telefon orqali qidirish" if lang == "uz" else "📞 Поиск по телефону"
    search_name_text = "👤 Ism orqali qidirish" if lang == "uz" else "👤 Поиск по имени"
    search_id_text = "🆔 ID orqali qidirish" if lang == "uz" else "🆔 Поиск по ID"
    new_client_text = "🆕 Yangi mijoz" if lang == "uz" else "🆕 Новый клиент"
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=search_phone_text, callback_data="ctrl_search_phone"),
            InlineKeyboardButton(text=search_name_text, callback_data="ctrl_search_name")
        ],
        [
            InlineKeyboardButton(text=search_id_text, callback_data="ctrl_search_id"),
            InlineKeyboardButton(text=new_client_text, callback_data="ctrl_search_new")
        ],
        [
            InlineKeyboardButton(text=cancel_text, callback_data="ctrl_cancel_creation"),
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

def get_client_selection_keyboard(clients, lang='uz'):
    """Generate client selection keyboard"""
    keyboard = []
    
    for client in clients[:10]:  # Maximum 10 clients
        button_text = f"👤 {client.get('full_name', 'N/A')} - {client.get('phone', 'N/A')}"
        keyboard.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"ctrl_select_client_{client['id']}"
            )
        ])
    
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard.append([InlineKeyboardButton(text=back_text, callback_data="ctrl_cancel_creation")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_priority_selection_keyboard(request_id, lang='uz'):
    """Generate priority selection keyboard"""
    low_text = "🟢 Past" if lang == "uz" else "🟢 Низкий"
    medium_text = "🟡 O'rta" if lang == "uz" else "🟡 Средний"
    high_text = "🟠 Yuqori" if lang == "uz" else "🟠 Высокий"
    urgent_text = "🔴 Shoshilinch" if lang == "uz" else "🔴 Срочный"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=low_text, callback_data=f"ctrl_priority_{request_id}_low"),
            InlineKeyboardButton(text=medium_text, callback_data=f"ctrl_priority_{request_id}_medium")
        ],
        [
            InlineKeyboardButton(text=high_text, callback_data=f"ctrl_priority_{request_id}_high"),
            InlineKeyboardButton(text=urgent_text, callback_data=f"ctrl_priority_{request_id}_urgent")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="ctrl_cancel_creation")
        ]
    ])
    return keyboard

# Workflow Manager callbacks
def get_workflow_manager_keyboard(lang='uz'):
    """Generate workflow manager keyboard"""
    statistics_text = "📊 Workflow statistikasi" if lang == "uz" else "📊 Статистика workflow"
    active_workflows_text = "🔄 Faol workflow'lar" if lang == "uz" else "🔄 Активные workflow"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=statistics_text, callback_data="view_workflow_statistics"),
            InlineKeyboardButton(text=active_workflows_text, callback_data="view_active_workflows")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

def get_workflow_navigation_keyboard(lang='uz'):
    """Generate workflow navigation keyboard"""
    prev_text = "⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий"
    next_text = "Keyingi ➡️" if lang == "uz" else "Следующий ➡️"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=prev_text, callback_data="workflow_prev"),
            InlineKeyboardButton(text=next_text, callback_data="workflow_next")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

# Technicians callbacks
def get_technicians_management_keyboard(lang='uz'):
    """Generate technicians management keyboard"""
    view_all_text = "📋 Barcha texniklar" if lang == "uz" else "📋 Все техники"
    performance_text = "📊 Samaradorlik" if lang == "uz" else "📊 Производительность"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=view_all_text, callback_data="view_technicians"),
            InlineKeyboardButton(text=performance_text, callback_data="view_technician_performance")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

def get_technician_navigation_keyboard(lang='uz'):
    """Generate technician navigation keyboard"""
    prev_text = "⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий"
    next_text = "Keyingi ➡️" if lang == "uz" else "Следующий ➡️"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=prev_text, callback_data="technician_prev"),
            InlineKeyboardButton(text=next_text, callback_data="technician_next")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_technician")
        ]
    ])
    return keyboard

def get_technician_actions_keyboard(technician_id, lang='uz'):
    """Generate technician actions keyboard"""
    view_details_text = "👁️ Batafsil" if lang == "uz" else "👁️ Подробно"
    assign_task_text = "📋 Vazifa tayinlash" if lang == "uz" else "📋 Назначить задачу"
    performance_text = "📊 Samaradorlik" if lang == "uz" else "📊 Производительность"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=view_details_text, callback_data=f"technician:view:{technician_id}"),
            InlineKeyboardButton(text=assign_task_text, callback_data=f"technician:assign:{technician_id}")
        ],
        [
            InlineKeyboardButton(text=performance_text, callback_data=f"technician:performance:{technician_id}")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_technicians")
        ]
    ])
    return keyboard

# Technical Service callbacks
def get_technical_service_navigation_keyboard(lang='uz'):
    """Generate technical service navigation keyboard"""
    prev_text = "⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий"
    next_text = "Keyingi ➡️" if lang == "uz" else "Следующий ➡️"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=prev_text, callback_data="ts_prev_service"),
            InlineKeyboardButton(text=next_text, callback_data="ts_next_service")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_controller_main")
        ]
    ])
    return keyboard

# Staff Application Creation callbacks
def get_staff_creation_keyboard(lang='uz'):
    """Generate staff creation keyboard"""
    view_members_text = "📋 Xodimlarni ko'rish" if lang == "uz" else "📋 Просмотр сотрудников"
    create_app_text = "📝 Ariza yaratish" if lang == "uz" else "📝 Создать заявку"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=view_members_text, callback_data="view_staff_members"),
            InlineKeyboardButton(text=create_app_text, callback_data="create_staff_application")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_staff_creation")
        ]
    ])
    return keyboard

def get_staff_navigation_keyboard(lang='uz'):
    """Generate staff navigation keyboard"""
    prev_text = "⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий"
    next_text = "Keyingi ➡️" if lang == "uz" else "Следующий ➡️"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=prev_text, callback_data="staff_prev"),
            InlineKeyboardButton(text=next_text, callback_data="staff_next")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_staff_creation")
        ]
    ])
    return keyboard

# Quality callbacks
def get_quality_management_keyboard(lang='uz'):
    """Generate quality management keyboard"""
    issues_text = "🔴 Sifat muammolari" if lang == "uz" else "🔴 Проблемы качества"
    metrics_text = "📊 Sifat ko'rsatkichlari" if lang == "uz" else "📊 Показатели качества"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=issues_text, callback_data="view_quality_issues"),
            InlineKeyboardButton(text=metrics_text, callback_data="view_quality_metrics")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_quality")
        ]
    ])
    return keyboard

def get_quality_navigation_keyboard(lang='uz'):
    """Generate quality navigation keyboard"""
    prev_text = "⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий"
    next_text = "Keyingi ➡️" if lang == "uz" else "Следующий ➡️"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=prev_text, callback_data="quality_prev_issue"),
            InlineKeyboardButton(text=next_text, callback_data="quality_next_issue")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_quality")
        ]
    ])
    return keyboard

# Monitoring callbacks
def get_monitoring_detailed_keyboard(lang='uz'):
    """Generate monitoring detailed keyboard"""
    statistics_text = "📊 Batafsil statistika" if lang == "uz" else "📊 Подробная статистика"
    system_status_text = "🖥️ Tizim holati" if lang == "uz" else "🖥️ Состояние системы"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=statistics_text, callback_data="view_detailed_statistics"),
            InlineKeyboardButton(text=system_status_text, callback_data="view_system_status")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_monitoring")
        ]
    ])
    return keyboard

# Realtime monitoring additional callbacks
def get_realtime_refresh_keyboard(lang='uz'):
    """Generate realtime refresh keyboard"""
    refresh_text = "🔄 Yangilash" if lang == "uz" else "🔄 Обновить"
    detailed_text = "📋 Batafsil" if lang == "uz" else "📋 Подробно"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=refresh_text, callback_data="ctrl_refresh_realtime"),
            InlineKeyboardButton(text=detailed_text, callback_data="ctrl_detailed_view")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="ctrl_back_to_realtime")
        ]
    ])
    return keyboard
