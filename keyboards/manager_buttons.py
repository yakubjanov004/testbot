from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_manager_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """
    Manager uchun asosiy reply menyu (O'zbek va Rus tillarida).
    """
    if lang == "uz":
        connection_order_text = "🔌 Ulanish arizasi yaratish"
        service_order_text = "🔧 Texnik xizmat yaratish"
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📋 Hammasini ko'rish")],
            [KeyboardButton(text=connection_order_text), KeyboardButton(text=service_order_text)],
            [KeyboardButton(text="🕐 Real vaqtda kuzatish"), KeyboardButton(text="📊 Monitoring")],
            [KeyboardButton(text="👥 Xodimlar faoliyati"), KeyboardButton(text="🔄 Status o'zgartirish")],
            [KeyboardButton(text="📤 Export"), KeyboardButton(text="🌐 Tilni o'zgartirish")],
        ]
    else:  # ruscha
        connection_order_text = "🔌 Создать заявку на подключение"
        service_order_text = "🔧 Создать техническую заявку"
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📋 Все заявки")],
            [KeyboardButton(text=connection_order_text), KeyboardButton(text=service_order_text)],
            [KeyboardButton(text="🕐 Мониторинг в реальном времени"), KeyboardButton(text="📊 Мониторинг")],
            [KeyboardButton(text="👥 Активность сотрудников"), KeyboardButton(text="🔄 Изменить статус")],
            [KeyboardButton(text="📤 Экспорт"), KeyboardButton(text="🌐 Изменить язык")],
        ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
