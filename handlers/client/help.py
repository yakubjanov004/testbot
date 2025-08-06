"""
Client Help Handler - Simplified Implementation

This module handles client help functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.client_states import HelpStates
from filters.role_filter import RoleFilter

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

async def get_user_role(user_id: int) -> str:
    """Mock get user role"""
    return 'client'

def get_client_help_router():
    """Get client help router with role filtering"""
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["❓ Yordam", "❓ Помощь"]))
    async def help_handler(message: Message, state: FSMContext):
        """Handle help request"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            help_text = (
                "❓ <b>Yordam va ko'rsatmalar</b>\n\n"
                "🔧 <b>Texnik xizmatlar:</b>\n"
                "• Internet tezligi sekin\n"
                "• TV signal yo'q\n"
                "• Router muammosi\n"
                "• Kabellar uzilgan\n\n"
                "🔌 <b>Ulanish xizmatlari:</b>\n"
                "• Uy internet ulanishi\n"
                "• Ofis internet ulanishi\n"
                "• TV ulanishi\n\n"
                "📞 <b>Bog'lanish:</b>\n"
                "• Telefon: +998 71 123 45 67\n"
                "• Telegram: @alfaconnect_support\n\n"
                "⏰ <b>Ish vaqti:</b> Dushanba - Shanba, 9:00 - 18:00"
                if lang == 'uz' else
                "❓ <b>Помощь и инструкции</b>\n\n"
                "🔧 <b>Технические услуги:</b>\n"
                "• Медленный интернет\n"
                "• Нет ТВ сигнала\n"
                "• Проблемы с роутером\n"
                "• Обрыв кабелей\n\n"
                "🔌 <b>Услуги подключения:</b>\n"
                "• Подключение домашнего интернета\n"
                "• Подключение офисного интернета\n"
                "• Подключение ТВ\n\n"
                "📞 <b>Контакты:</b>\n"
                "• Телефон: +998 71 123 45 67\n"
                "• Telegram: @alfaconnect_support\n\n"
                "⏰ <b>Время работы:</b> Понедельник - Суббота, 9:00 - 18:00"
            )
            
            from keyboards.client_buttons import get_back_keyboard
            keyboard = get_back_keyboard(lang)
            
            await message.answer(help_text, reply_markup=keyboard, parse_mode='HTML')
            await state.set_state(HelpStates.help_info)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "help_info")
    async def help_info_callback(callback: CallbackQuery, state: FSMContext):
        """Handle help info callback"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            help_text = (
                "❓ <b>Yordam va ko'rsatmalar</b>\n\n"
                "🔧 <b>Texnik xizmatlar:</b>\n"
                "• Internet tezligi sekin\n"
                "• TV signal yo'q\n"
                "• Router muammosi\n"
                "• Kabellar uzilgan\n\n"
                "🔌 <b>Ulanish xizmatlari:</b>\n"
                "• Uy internet ulanishi\n"
                "• Ofis internet ulanishi\n"
                "• TV ulanishi\n\n"
                "📞 <b>Bog'lanish:</b>\n"
                "• Telefon: +998 71 123 45 67\n"
                "• Telegram: @alfaconnect_support\n\n"
                "⏰ <b>Ish vaqti:</b> Dushanba - Shanba, 9:00 - 18:00"
                if lang == 'uz' else
                "❓ <b>Помощь и инструкции</b>\n\n"
                "🔧 <b>Технические услуги:</b>\n"
                "• Медленный интернет\n"
                "• Нет ТВ сигнала\n"
                "• Проблемы с роутером\n"
                "• Обрыв кабелей\n\n"
                "🔌 <b>Услуги подключения:</b>\n"
                "• Подключение домашнего интернета\n"
                "• Подключение офисного интернета\n"
                "• Подключение ТВ\n\n"
                "📞 <b>Контакты:</b>\n"
                "• Телефон: +998 71 123 45 67\n"
                "• Telegram: @alfaconnect_support\n\n"
                "⏰ <b>Время работы:</b> Понедельник - Суббота, 9:00 - 18:00"
            )
            
            from keyboards.client_buttons import get_back_keyboard
            keyboard = get_back_keyboard(lang)
            
            await callback.message.edit_text(help_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
