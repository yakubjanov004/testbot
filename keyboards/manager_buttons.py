from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_manager_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """
    Manager uchun asosiy reply menyu (O'zbek va Rus tillarida).
    """
    if lang == "uz":
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📋 Hammasini ko'rish")],
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
