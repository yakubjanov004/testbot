from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
