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


# Controller-specific inline keyboards mirroring client keyboards

def get_controller_regions_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Toshkent shahri", callback_data="ctrl_region_tashkent_city"),
            InlineKeyboardButton(text="Toshkent viloyati", callback_data="ctrl_region_tashkent_region")
        ],
        [
            InlineKeyboardButton(text="Andijon", callback_data="ctrl_region_andijon"),
            InlineKeyboardButton(text="Farg'ona", callback_data="ctrl_region_fergana")
        ],
        [
            InlineKeyboardButton(text="Namangan", callback_data="ctrl_region_namangan"),
            InlineKeyboardButton(text="Sirdaryo", callback_data="ctrl_region_sirdaryo")
        ],
        [
            InlineKeyboardButton(text="Jizzax", callback_data="ctrl_region_jizzax"),
            InlineKeyboardButton(text="Samarqand", callback_data="ctrl_region_samarkand")
        ],
        [
            InlineKeyboardButton(text="Buxoro", callback_data="ctrl_region_bukhara"),
            InlineKeyboardButton(text="Navoiy", callback_data="ctrl_region_navoi")
        ],
        [
            InlineKeyboardButton(text="Qashqadaryo", callback_data="ctrl_region_kashkadarya"),
            InlineKeyboardButton(text="Surxondaryo", callback_data="ctrl_region_surkhandarya")
        ],
        [
            InlineKeyboardButton(text="Xorazm", callback_data="ctrl_region_khorezm"),
            InlineKeyboardButton(text="Qoraqalpog'iston", callback_data="ctrl_region_karakalpakstan")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def controller_zayavka_type_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    person_physical_text = "👤 Jismoniy shaxs" if lang == "uz" else "👤 Физическое лицо"
    person_legal_text = "🏢 Yuridik shaxs" if lang == "uz" else "🏢 Юридическое лицо"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=person_physical_text, callback_data="ctrl_zayavka_type_b2b")],
            [InlineKeyboardButton(text=person_legal_text, callback_data="ctrl_zayavka_type_b2c")]
        ]
    )
    return keyboard


def controller_media_attachment_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes_text, callback_data="ctrl_attach_media_yes")],
        [InlineKeyboardButton(text=no_text, callback_data="ctrl_attach_media_no")]
    ])
    return keyboard


def controller_geolocation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes_text, callback_data="ctrl_send_location_yes")],
        [InlineKeyboardButton(text=no_text, callback_data="ctrl_send_location_no")]
    ])
    return keyboard


def controller_confirmation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    resend_text = "🔄 Qayta yuborish" if lang == "uz" else "🔄 Отправить заново"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data="ctrl_confirm_zayavka"),
            InlineKeyboardButton(text=resend_text, callback_data="ctrl_resend_zayavka")
        ]
    ])
    return keyboard


def get_controller_tariff_selection_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Standard", callback_data="ctrl_tariff_standard"),
            InlineKeyboardButton(text="Yangi", callback_data="ctrl_tariff_new")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_creator_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📱 Telefon" if lang == 'uz' else "📱 Телефон"), callback_data="ctrl_search_phone"),
            InlineKeyboardButton(text=("👤 Ism" if lang == 'uz' else "👤 Имя"), callback_data="ctrl_search_name")
        ],
        [
            InlineKeyboardButton(text=("🆔 ID" if lang == 'uz' else "🆔 ID"), callback_data="ctrl_search_id"),
            InlineKeyboardButton(text=("➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент"), callback_data="ctrl_search_new")
        ],
        [
            InlineKeyboardButton(text=("❌ Bekor qilish" if lang == 'uz' else "❌ Отменить"), callback_data="ctrl_cancel_creation")
        ]
    ])


# Realtime monitoring keyboards for controller

def get_realtime_monitoring_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    status_text = "🟢 Jonli holat" if lang == 'uz' else "🟢 Живой статус"
    activities_text = "📝 Faoliyatlar" if lang == 'uz' else "📝 Активности"
    alerts_text = "⚠️ Ogohlantirishlar" if lang == 'uz' else "⚠️ Оповещения"
    performance_text = "📈 Ko'rsatkichlar" if lang == 'uz' else "📈 Показатели"
    remaining_text = "⌛ Qolgan vaqtlar" if lang == 'uz' else "⌛ Оставшееся время"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=status_text, callback_data='ctrl_realtime_status')],
        [InlineKeyboardButton(text=remaining_text, callback_data='ctrl_realtime_remaining')],
        [InlineKeyboardButton(text=activities_text, callback_data='ctrl_realtime_activities')],
        [InlineKeyboardButton(text=alerts_text, callback_data='ctrl_realtime_alerts')],
        [InlineKeyboardButton(text=performance_text, callback_data='ctrl_realtime_performance')],
    ])


def get_realtime_refresh_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    refresh_text = "🔄 Yangilash" if lang == 'uz' else "🔄 Обновить"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=refresh_text, callback_data='ctrl_realtime_refresh')],
        [InlineKeyboardButton(text=back_text, callback_data='controllers_back')],
    ])
