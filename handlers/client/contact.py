"""
Client Contact Handler - Simplified Implementation

This module handles client contact functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_contact_keyboard, get_main_menu_keyboard
from states.client_states import ContactStates
from utils.role_system import get_role_router

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567'
    }

async def get_user_lang(user_id: int) -> str:
    """Mock get user language"""
    return 'uz'

def get_client_contact_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["📞 Aloqa", "📞 Контакты"]))
    async def client_contact_handler(message: Message, state: FSMContext):
        """Client contact handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            lang = user.get('language', 'uz')
            
            contact_text = (
                "📞 <b>Aloqa ma'lumotlari - To'liq ma'lumot</b>\n\n"
                "🏢 <b>Kompaniya:</b> Alfa Connect\n"
                "📞 <b>Asosiy telefon:</b> +998901234567\n"
                "📱 <b>Mobil raqam:</b> +998901234568\n"
                "📧 <b>Email:</b> info@alfaconnect.uz\n"
                "🌐 <b>Veb-sayt:</b> www.alfaconnect.uz\n\n"
                "🏛️ <b>Ofis manzili:</b>\n"
                "Toshkent shahri, Chorsu tumani,\n"
                "Alfa Connect binosi, 1-qavat\n\n"
                "⏰ <b>Ish vaqti:</b>\n"
                "Dushanba - Shanba: 09:00 - 18:00\n"
                "Yakshanba: 10:00 - 16:00\n\n"
                "💬 <b>Telegram kanal:</b> @alfaconnect_uz\n"
                "📱 <b>Telegram guruh:</b> @alfaconnect_support"
                if lang == 'uz' else
                "📞 <b>Контактная информация - Полная информация</b>\n\n"
                "🏢 <b>Компания:</b> Alfa Connect\n"
                "📞 <b>Основной телефон:</b> +998901234567\n"
                "📱 <b>Мобильный номер:</b> +998901234568\n"
                "📧 <b>Email:</b> info@alfaconnect.uz\n"
                "🌐 <b>Веб-сайт:</b> www.alfaconnect.uz\n\n"
                "🏛️ <b>Адрес офиса:</b>\n"
                "Город Ташкент, Чорсу район,\n"
                "Здание Alfa Connect, 1-й этаж\n\n"
                "⏰ <b>Время работы:</b>\n"
                "Понедельник - Суббота: 09:00 - 18:00\n"
                "Воскресенье: 10:00 - 16:00\n\n"
                "💬 <b>Telegram канал:</b> @alfaconnect_uz\n"
                "📱 <b>Telegram группа:</b> @alfaconnect_support"
            )
            
            sent_message = await message.answer(
                text=contact_text,
                reply_markup=get_contact_keyboard(lang),
                parse_mode='HTML'
            )
            
            await state.set_state(ContactStates.contact_info)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Back to main menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            main_menu_text = (
                "🏠 Bosh sahifa. Quyidagi menyudan kerakli bo'limni tanlang:"
                if lang == 'uz' else
                "🏠 Главная страница. Выберите нужный раздел из меню ниже:"
            )
            
            await callback.message.edit_text(
                text=main_menu_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.clear()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router
