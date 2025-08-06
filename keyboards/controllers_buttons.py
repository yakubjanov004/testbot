from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any

def get_controller_main_keyboard(lang="uz"):
    """Controller main keyboard - returns main menu keyboard"""
    return controllers_main_menu(lang)

def controllers_main_menu(lang='uz'):
    """Controllers asosiy menyu"""
    if lang == 'uz':
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📊 Monitoring")],
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="🎯 Sifat nazorati")],
            [KeyboardButton(text="📊 Hisobotlar"), KeyboardButton(text="👨‍🔧 Texniklar")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="🕐 Real vaqtda kuzatish"), KeyboardButton(text="🏆 Sifat boshqaruvi")],
            [KeyboardButton(text="⚙️ Workflow boshqaruvi"), KeyboardButton(text="📋 Buyurtmalar nazorati")],
            [KeyboardButton(text="🌐 Tilni o'zgartirish"), KeyboardButton(text="🏠 Bosh menyu")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📊 Мониторинг")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="🎯 Контроль качества")],
            [KeyboardButton(text="📊 Отчеты"), KeyboardButton(text="👨‍🔧 Техники")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать техническую заявку")],
            [KeyboardButton(text="🕐 Мониторинг в реальном времени"), KeyboardButton(text="🏆 Управление качеством")],
            [KeyboardButton(text="⚙️ Управление процессами"), KeyboardButton(text="📋 Контроль заказов")],
            [KeyboardButton(text="🌐 Изменить язык"), KeyboardButton(text="🏠 Главное меню")]
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

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
