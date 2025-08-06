"""
Client Contact Handler - Simplified Implementation

This module handles client contact functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.client_states import ContactStates
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

def get_client_contact_router():
    """Get client contact router with role filtering"""
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📞 Bog'lanish", "📞 Связаться"]))
    async def contact_handler(message: Message, state: FSMContext):
        """Handle contact request"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            contact_text = (
                "📞 <b>Biz bilan bog'lanish</b>\n\n"
                "📱 <b>Telefon:</b> +998 71 123 45 67\n"
                "📧 <b>Email:</b> info@alfaconnect.uz\n"
                "🌐 <b>Veb-sayt:</b> www.alfaconnect.uz\n"
                "📍 <b>Manzil:</b> Toshkent shahri, Chilonzor tumani\n"
                "⏰ <b>Ish vaqti:</b> Dushanba - Shanba, 9:00 - 18:00\n\n"
                "💬 <b>Telegram kanal:</b> @alfaconnect_uz"
                if lang == 'uz' else
                "📞 <b>Связаться с нами</b>\n\n"
                "📱 <b>Телефон:</b> +998 71 123 45 67\n"
                "📧 <b>Email:</b> info@alfaconnect.uz\n"
                "🌐 <b>Веб-сайт:</b> www.alfaconnect.uz\n"
                "📍 <b>Адрес:</b> г. Ташкент, Чиланзарский район\n"
                "⏰ <b>Время работы:</b> Понедельник - Суббота, 9:00 - 18:00\n\n"
                "💬 <b>Telegram канал:</b> @alfaconnect_uz"
            )
            
            from keyboards.client_buttons import get_back_keyboard
            keyboard = get_back_keyboard(lang)
            
            await message.answer(contact_text, reply_markup=keyboard, parse_mode='HTML')
            await state.set_state(ContactStates.contact_info)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "contact_info")
    async def contact_info_callback(callback: CallbackQuery, state: FSMContext):
        """Handle contact info callback"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            contact_text = (
                "📞 <b>Biz bilan bog'lanish</b>\n\n"
                "📱 <b>Telefon:</b> +998 71 123 45 67\n"
                "📧 <b>Email:</b> info@alfaconnect.uz\n"
                "🌐 <b>Veb-sayt:</b> www.alfaconnect.uz\n"
                "📍 <b>Manzil:</b> Toshkent shahri, Chilonzor tumani\n"
                "⏰ <b>Ish vaqti:</b> Dushanba - Shanba, 9:00 - 18:00\n\n"
                "💬 <b>Telegram kanal:</b> @alfaconnect_uz"
                if lang == 'uz' else
                "📞 <b>Связаться с нами</b>\n\n"
                "📱 <b>Телефон:</b> +998 71 123 45 67\n"
                "📧 <b>Email:</b> info@alfaconnect.uz\n"
                "🌐 <b>Веб-сайт:</b> www.alfaconnect.uz\n"
                "📍 <b>Адрес:</b> г. Ташкент, Чиланзарский район\n"
                "⏰ <b>Время работы:</b> Понедельник - Суббота, 9:00 - 18:00\n\n"
                "💬 <b>Telegram канал:</b> @alfaconnect_uz"
            )
            
            from keyboards.client_buttons import get_back_keyboard
            keyboard = get_back_keyboard(lang)
            
            await callback.message.edit_text(contact_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
