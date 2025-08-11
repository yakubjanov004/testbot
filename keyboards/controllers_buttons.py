from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any

def controllers_main_menu(lang='uz'):
    if lang == 'uz':
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📋 Arizalarni ko'rish")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="🕐 Real vaqtda kuzatish"), KeyboardButton(text="📊 Monitoring")],
            [KeyboardButton(text="👥 Xodimlar faoliyati"), KeyboardButton(text="📤 Export")],
            [KeyboardButton(text="🌐 Tilni o'zgartirish")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📋 Просмотр заявок")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать техническую заявку")],
            [KeyboardButton(text="🕐 Мониторинг в реальном времени"), KeyboardButton(text="📊 Мониторинг")],
            [KeyboardButton(text="👥 Активность сотрудников"), KeyboardButton(text="📤 Экспорт")],
            [KeyboardButton(text="🌐 Изменить язык")]
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
