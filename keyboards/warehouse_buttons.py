from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_warehouse_main_keyboard(language: str) -> ReplyKeyboardMarkup:
    """Warehouse uchun asosiy menyu - tex.txt talablariga mos"""
    inbox = "📥 Inbox"
    inventory = "📦 Inventarizatsiya" if language == 'uz' else "📦 Инвентаризация"
    orders = "📋 Buyurtmalar" if language == 'uz' else "📋 Заказы"
    statistics = "📊 Statistikalar" if language == 'uz' else "📊 Статистика"
    export = "📤 Export" if language == 'uz' else "📤 Экспорт"
    
    # Tex.txt bo'yicha warehouse ariza yaratmaydi, faqat boshqaradi
    change_lang = "🌐 Tilni o'zgartirish" if language == 'uz' else "🌐 Изменить язык"
    
    keyboard = [
        [KeyboardButton(text=inbox)],
        [KeyboardButton(text=inventory), KeyboardButton(text=orders)],
        [KeyboardButton(text=statistics), KeyboardButton(text=export)],
        [KeyboardButton(text=change_lang)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def warehouse_inventory_menu(language: str) -> ReplyKeyboardMarkup:
    add_item = "➕ Mahsulot qo'shish" if language == 'uz' else "➕ Добавить товар"
    update_item = "✏️ Mahsulotni yangilash" if language == 'uz' else "✏️ Обновить товар"
    low_stock = "⚠️ Kam zaxira" if language == 'uz' else "⚠️ Низкий запас"
    out_of_stock = "❌ Tugagan mahsulotlar" if language == 'uz' else "❌ Нет в наличии"
    search = "🔍 Qidirish" if language == 'uz' else "🔍 Поиск"
    view_all = "📋 Barcha mahsulotlar" if language == 'uz' else "📋 Все товары"
    back = "◀️ Orqaga" if language == 'uz' else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=add_item), KeyboardButton(text=update_item)],
        [KeyboardButton(text=low_stock), KeyboardButton(text=out_of_stock)],
        [KeyboardButton(text=search), KeyboardButton(text=view_all)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def warehouse_orders_menu(language: str) -> ReplyKeyboardMarkup:
    """Buyurtmalar uchun menyu (ReplyKeyboard)"""
    pending = "⏳ Kutilayotgan buyurtmalar" if language == 'uz' else "⏳ Ожидающие заказы"
    in_progress = "🔄 Jarayondagi buyurtmalar" if language == 'uz' else "🔄 Заказы в процессе"
    completed = "✅ Bajarilgan buyurtmalar" if language == 'uz' else "✅ Выполненные заказы"
    back = "◀️ Orqaga" if language == 'uz' else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=pending), KeyboardButton(text=in_progress)],
        [KeyboardButton(text=completed)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def warehouse_statistics_menu(language: str) -> ReplyKeyboardMarkup:
    """Statistikalar uchun asosiy menyu (ReplyKeyboard)"""
    inventory_stats = "📦 Inventarizatsiya statistikasi" if language == 'uz' else "📦 Статистика инвентаризации"
    orders_stats = "📋 Buyurtmalar statistikasi" if language == 'uz' else "📋 Статистика заказов"
    low_stock_stats = "⚠️ Kam zaxira statistikasi" if language == 'uz' else "⚠️ Статистика низкого запаса"
    financial_stats = "💰 Moliyaviy hisobot" if language == 'uz' else "💰 Финансовый отчет"
    period_stats = "📆 Vaqt oralig'idagi statistika" if language == 'uz' else "📆 Статистика за период"
    back = "◀️ Orqaga" if language == 'uz' else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=inventory_stats)],
        [KeyboardButton(text=orders_stats)],
        [KeyboardButton(text=low_stock_stats)],
        [KeyboardButton(text=financial_stats)],
        [KeyboardButton(text=period_stats)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def statistics_period_menu(language: str) -> ReplyKeyboardMarkup:
    """Vaqt oralig'idagi statistika uchun ichki reply menyu"""
    monthly = "📈 Oylik statistika" if language == 'uz' else "📈 Месячная статистика"
    daily = "📅 Kunlik statistika" if language == 'uz' else "📅 Ежедневная статистика"
    weekly = "📊 Haftalik statistika" if language == 'uz' else "📊 Недельная статистика"
    yearly = "🗓 Yillik statistika" if language == 'uz' else "🗓 Годовая статистика"
    back = "◀️ Orqaga" if language == 'uz' else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=monthly), KeyboardButton(text=daily)],
        [KeyboardButton(text=weekly), KeyboardButton(text=yearly)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def inventory_menu(language: str) -> InlineKeyboardMarkup:
    """Inventory management menu"""
    add_item_text = "➕ Mahsulot qo'shish" if language == "uz" else "➕ Добавить товар"
    update_item_text = "✏️ Mahsulotni yangilash" if language == "uz" else "✏️ Обновить товар"
    low_stock_report_text = "⚠️ Kam zaxira hisoboti" if language == "uz" else "⚠️ Отчет о низком запасе"
    back_text = "◀️ Orqaga" if language == "uz" else "◀️ Назад"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=add_item_text,
                callback_data="add_inventory_item"
            )
        ],
        [
            InlineKeyboardButton(
                text=update_item_text,
                callback_data="update_inventory_item"
            )
        ],
        [
            InlineKeyboardButton(
                text=low_stock_report_text,
                callback_data="low_stock_report"
            )
        ],
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="warehouse_back"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def orders_menu(language: str) -> InlineKeyboardMarkup:
    """Orders management menu"""
    pending_orders_text = "⏳ Kutilayotgan buyurtmalar" if language == "uz" else "⏳ Ожидающие заказы"
    in_progress_orders_text = "🔄 Jarayondagi buyurtmalar" if language == "uz" else "🔄 Заказы в процессе"
    completed_orders_text = "✅ Bajarilgan buyurtmalar" if language == "uz" else "✅ Выполненные заказы"
    back_text = "◀️ Orqaga" if language == "uz" else "◀️ Назад"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=pending_orders_text,
                callback_data="pending_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text=in_progress_orders_text,
                callback_data="in_progress_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text=completed_orders_text,
                callback_data="completed_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="warehouse_back"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def order_status_keyboard(language: str, current_status: str) -> InlineKeyboardMarkup:
    """Order status update keyboard"""
    start_processing_text = "▶️ Qayta ishlashni boshlash" if language == "uz" else "▶️ Начать обработку"
    parts_ready_text = "🔧 Ehtiyot qismlar tayyor" if language == "uz" else "🔧 Запчасти готовы"
    ready_for_technician_text = "👨‍🔧 Texnik uchun tayyor" if language == "uz" else "👨‍🔧 Готово для техника"
    back_text = "◀️ Orqaga" if language == "uz" else "◀️ Назад"
    
    keyboard = []
    
    if current_status == 'confirmed':
        keyboard.append([
            InlineKeyboardButton(
                text=start_processing_text,
                callback_data="update_order_status_in_progress"
            )
        ])
    
    if current_status == 'in_progress':
        keyboard.extend([
            [
                InlineKeyboardButton(
                    text=parts_ready_text,
                    callback_data="update_order_status_parts_ready"
                )
            ],
            [
                InlineKeyboardButton(
                    text=ready_for_technician_text,
                    callback_data="update_order_status_ready_for_tech"
                )
            ]
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            text=back_text,
            callback_data="warehouse_orders"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def inventory_actions_keyboard(language: str) -> InlineKeyboardMarkup:
    """Inventory item actions keyboard"""
    update_quantity_text = "📊 Miqdorni yangilash" if language == "uz" else "📊 Обновить количество"
    set_min_quantity_text = "⚠️ Minimal miqdorni belgilash" if language == "uz" else "⚠️ Установить минимальное количество"
    delete_item_text = "🗑️ Mahsulotni o'chirish" if language == "uz" else "🗑️ Удалить товар"
    back_text = "◀️ Orqaga" if language == "uz" else "◀️ Назад"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=update_quantity_text,
                callback_data="update_quantity"
            )
        ],
        [
            InlineKeyboardButton(
                text=set_min_quantity_text,
                callback_data="set_min_quantity"
            )
        ],
        [
            InlineKeyboardButton(
                text=delete_item_text,
                callback_data="delete_item"
            )
        ],
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="warehouse_inventory"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def inventory_actions_inline(item_id: int, language: str) -> InlineKeyboardMarkup:
    increase = "➕ Kirim" if language == 'uz' else "➕ Приход"
    decrease = "➖ Chiqim" if language == 'uz' else "➖ Расход"
    delete = "🗑️ O‘chirish" if language == 'uz' else "🗑️ Удалить"
    back = "◀️ Orqaga" if language == 'uz' else "◀️ Назад"
    keyboard = [
        [InlineKeyboardButton(text=increase, callback_data=f"increase_{item_id}"),
         InlineKeyboardButton(text=decrease, callback_data=f"decrease_{item_id}")],
        [InlineKeyboardButton(text=delete, callback_data=f"delete_{item_id}")],
        [InlineKeyboardButton(text=back, callback_data="warehouse_inventory")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def warehouse_detailed_statistics_menu(language: str) -> InlineKeyboardMarkup:
    """Detailed statistics menu for warehouse"""
    daily_stats = "📅 Kunlik statistika" if language == 'uz' else "📅 Ежедневная статистика"
    weekly_stats = "📊 Haftalik hisobot" if language == 'uz' else "📊 Недельный отчет"
    monthly_stats = "📈 Oylik hisobot" if language == 'uz' else "📈 Месячный отчет"
    back = "◀️ Orqaga" if language == 'uz' else "◀️ Назад"
    keyboard = [
        [InlineKeyboardButton(text=daily_stats, callback_data="warehouse_stats_daily")],
        [InlineKeyboardButton(text=weekly_stats, callback_data="warehouse_stats_weekly")],
        [InlineKeyboardButton(text=monthly_stats, callback_data="warehouse_stats_monthly")],
        [InlineKeyboardButton(text=back, callback_data="warehouse_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def inventory_detailed_list_menu(language: str) -> InlineKeyboardMarkup:
    """Detailed inventory list menu"""
    all_items = "📦 Barcha mahsulotlar" if language == 'uz' else "📦 Все товары"
    low_stock = "⚠️ Kam zaxira" if language == 'uz' else "⚠️ Низкий запас"
    out_of_stock = "❌ Zaxira tugagan" if language == 'uz' else "❌ Нет в наличии"
    back = "◀️ Orqaga" if language == 'uz' else "◀️ Назад"
    keyboard = [
        [InlineKeyboardButton(text=all_items, callback_data="inventory_all_items")],
        [InlineKeyboardButton(text=low_stock, callback_data="inventory_low_stock")],
        [InlineKeyboardButton(text=out_of_stock, callback_data="inventory_out_of_stock")],
        [InlineKeyboardButton(text=back, callback_data="warehouse_inventory")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def statistics_menu(language: str) -> InlineKeyboardMarkup:
    """Warehouse statistics menu"""
    inventory_stats = "📦 Inventarizatsiya statistikasi" if language == 'uz' else "📦 Статистика инвентаризации"
    orders_stats = "📋 Buyurtmalar statistikasi" if language == 'uz' else "📋 Статистика заказов"
    export_stats = "📤 Hisobotni export qilish" if language == 'uz' else "📤 Экспорт отчета"
    back = "◀️ Orqaga" if language == 'uz' else "◀️ Назад"
    keyboard = [
        [InlineKeyboardButton(text=inventory_stats, callback_data="warehouse_inventory_stats")],
        [InlineKeyboardButton(text=orders_stats, callback_data="warehouse_orders_stats")],
        [InlineKeyboardButton(text=export_stats, callback_data="warehouse_export_stats")],
        [InlineKeyboardButton(text=back, callback_data="warehouse_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def export_menu(language: str, export_types: list = None) -> InlineKeyboardMarkup:
    """Export menu for warehouse operations"""
    if export_types is None:
        export_types = ["inventory", "orders", "statistics"]
    
    keyboard = []
    
    # Map export types to display names
    type_names = {
        "inventory": "📦 Inventarizatsiya export" if language == 'uz' else "📦 Экспорт инвентаризации",
        "orders": "📋 Buyurtmalar export" if language == 'uz' else "📋 Экспорт заказов",
        "statistics": "📊 Statistikalar export" if language == 'uz' else "📊 Экспорт статистики",
        "issued_items": "📤 Berilgan materiallar export" if language == 'uz' else "📤 Экспорт выданных материалов",
        "users": "👥 Foydalanuvchilar export" if language == 'uz' else "👥 Экспорт пользователей"
    }
    
    for export_type in export_types:
        if export_type in type_names:
            keyboard.append([
                InlineKeyboardButton(
                    text=type_names[export_type], 
                    callback_data=f"export_{export_type}"
                )
            ])

    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def export_reply_menu(language: str) -> ReplyKeyboardMarkup:
    """Export uchun ichki reply menyu"""
    excel = "Excelga export" if language == 'uz' else "Экспорт в Excel"
    pdf = "PDFga export" if language == 'uz' else "Экспорт в PDF"
    word = "Wordga export" if language == 'uz' else "Экспорт в Word"
    keyboard = [
        [KeyboardButton(text=excel), KeyboardButton(text=pdf)],
        [KeyboardButton(text=word)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def language_selection_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    uz_text = "🇺🇿 O'zbek tili"
    ru_text = "🇷🇺 Русский язык"
    keyboard = [
        [InlineKeyboardButton(text=uz_text, callback_data="set_language_uz")],
        [InlineKeyboardButton(text=ru_text, callback_data="set_language_ru")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def export_format_keyboard(language: str) -> InlineKeyboardMarkup:
    """Export format selection keyboard"""
    excel = "📊 Excel" if language == 'uz' else "📊 Excel"
    pdf = "📄 PDF" if language == 'uz' else "📄 PDF"
    word = "📝 Word" if language == 'uz' else "📝 Word"
    keyboard = [
        [InlineKeyboardButton(text=excel, callback_data="export_format_xlsx")],
        [InlineKeyboardButton(text=pdf, callback_data="export_format_pdf")],
        [InlineKeyboardButton(text=word, callback_data="export_format_docx")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def update_item_fields_inline(item_id: int, language: str) -> InlineKeyboardMarkup:
    name = "✏️ Nomi" if language == 'uz' else "✏️ Название"
    quantity = "🔢 Miqdori" if language == 'uz' else "🔢 Количество"
    price = "💰 Narxi" if language == 'uz' else "💰 Цена"
    description = "📝 Tavsifi" if language == 'uz' else "📝 Описание"
    keyboard = [
        [InlineKeyboardButton(text=name, callback_data=f"update_name_{item_id}"),
         InlineKeyboardButton(text=quantity, callback_data=f"update_quantity_{item_id}")],
        [InlineKeyboardButton(text=price, callback_data=f"update_price_{item_id}"),
         InlineKeyboardButton(text=description, callback_data=f"update_description_{item_id}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_application_keyboard(app_id: int) -> InlineKeyboardMarkup:
    """Create keyboard for an application"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁️ Ko'rish", callback_data=f"view_app_{app_id}"),
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_app_{app_id}")
            ]
        ]
    )
    return keyboard
def equipment_preparation_keyboard(request_id: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Equipment preparation keyboard for warehouse"""
    prepare_text = "📦 Uskunani tayyorlash" if lang == "uz" else "📦 Подготовить оборудование"
    
    keyboard = [
        [InlineKeyboardButton(
            text=prepare_text,
            callback_data=f"prepare_equipment_{request_id}"
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_language_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_language_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language_ru")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# New centralized keyboard functions for warehouse handlers

def get_warehouse_inbox_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Navigation keyboard for warehouse inbox"""
    keyboard = [
        [
            InlineKeyboardButton(text="⬅️ Oldingi", callback_data="wh_prev"),
            InlineKeyboardButton(text="Keyingisi ➡️", callback_data="wh_next")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_warehouse_request_actions_keyboard(request_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Action buttons for warehouse requests"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"wh_approve_{request_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"wh_reject_{request_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_warehouse_back_to_inbox_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Back to inbox keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="📥 Inbox'ga qaytish", callback_data="wh_back_to_inbox")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_warehouse_cancel_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Cancel action keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="wh_back_to_inbox")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_warehouse_application_actions_keyboard(app_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Action buttons for warehouse applications"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Yakunlash", callback_data=f"wh_complete_{app_id}"),
            InlineKeyboardButton(text="🔧 Texnikka qaytarish", callback_data=f"wh_return_tech_{app_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_warehouse_export_types_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Export types selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="📦 Inventarizatsiya", callback_data="warehouse_export_inventory")],
        [InlineKeyboardButton(text="📋 Berilgan materiallar", callback_data="warehouse_export_issued_items")],
        [InlineKeyboardButton(text="📑 Buyurtmalar", callback_data="warehouse_export_orders")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="warehouse_export_statistics")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_warehouse_export_formats_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Export formats selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="CSV", callback_data="warehouse_format_csv")],
        [InlineKeyboardButton(text="Excel", callback_data="warehouse_format_xlsx")],
        [InlineKeyboardButton(text="Word", callback_data="warehouse_format_docx")],
        [InlineKeyboardButton(text="PDF", callback_data="warehouse_format_pdf")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="warehouse_export_back_types")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_warehouse_export_back_types_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Back to export types keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="📦 Inventarizatsiya", callback_data="warehouse_export_inventory")],
        [InlineKeyboardButton(text="📋 Berilgan materiallar", callback_data="warehouse_export_issued_items")],
        [InlineKeyboardButton(text="📑 Buyurtmalar", callback_data="warehouse_export_orders")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="warehouse_export_statistics")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="warehouse_export_back_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_warehouse_back_to_main_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Back to main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="warehouse_back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
