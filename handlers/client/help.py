"""
Client Help Handler - Simplified Implementation

This module handles client help functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.client_states import HelpStates
from filters.role_filter import RoleFilter
from utils.role_system import get_role_router
from keyboards.client_buttons import get_client_help_menu, get_back_to_help_menu_inline

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
    """Get client help router with role filtering and inline callbacks"""
    router = get_role_router("client")
    
    # Extra safety: apply role filter if needed
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["❓ Yordam", "❓ Помощь"]))
    async def help_handler(message: Message, state: FSMContext):
        """Show help menu with inline buttons"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            help_text = (
                "Yordam menyusi. Kerakli bo'limni tanlang."
                if lang == 'uz' else
                "Меню помощи. Выберите нужный раздел."
            )
            await message.answer(help_text, reply_markup=get_client_help_menu(lang))
            await state.set_state(HelpStates.help_menu)
        except Exception:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "client_faq")
    async def client_faq_handler(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            faq_text = (
                "❓ Tez-tez so'raladigan savollar:\n\n"
                "1. Qanday buyurtma beraman?\n"
                "   - 'Yangi buyurtma' tugmasini bosing\n\n"
                "2. Buyurtmam qachon bajariladi?\n"
                "   - Odatda 1-3 ish kuni ichida\n\n"
                "3. Narxlar qanday?\n"
                "   - Operator siz bilan bog'lanib narxni aytadi\n\n"
                "4. Bekor qilsam bo'ladimi?\n"
                "   - Ha, operator orqali bekor qilishingiz mumkin"
                if lang == 'uz' else
                "❓ Часто задаваемые вопросы:\n\n"
                "1. Как сделать заказ?\n"
                "   - Нажмите кнопку 'Новый заказ'\n\n"
                "2. Когда выполнят мой заказ?\n"
                "   - Обычно в течение 1-3 рабочих дней\n\n"
                "3. Какие цены?\n"
                "   - Оператор свяжется с вами и сообщит цену\n\n"
                "4. Можно ли отменить?\n"
                "   - Да, можете отменить через оператора"
            )
            await callback.message.edit_text(faq_text, reply_markup=get_back_to_help_menu_inline(lang))
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "client_how_to_order")
    async def client_how_to_order_handler(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            guide_text = (
                "📝 Qanday buyurtma berish:\n\n"
                "1️⃣ 'Yangi buyurtma' tugmasini bosing\n"
                "2️⃣ Buyurtma turini tanlang\n"
                "3️⃣ Tavsifni kiriting\n"
                "4️⃣ Manzilni kiriting\n"
                "5️⃣ Rasm biriktiring (ixtiyoriy)\n"
                "6️⃣ Geolokatsiya yuboring (ixtiyoriy)\n"
                "7️⃣ Buyurtmani tasdiqlang\n\n"
                "✅ Tayyor! Operator siz bilan bog'lanadi."
                if lang == 'uz' else
                "📝 Как сделать заказ:\n\n"
                "1️⃣ Нажмите 'Новый заказ'\n"
                "2️⃣ Выберите тип заказа\n"
                "3️⃣ Введите описание\n"
                "4️⃣ Введите адрес\n"
                "5️⃣ Прикрепите фото (по желанию)\n"
                "6️⃣ Отправьте геолокацию (по желанию)\n"
                "7️⃣ Подтвердите заказ\n\n"
                "✅ Готово! Оператор свяжется с вами."
            )
            await callback.message.edit_text(guide_text, reply_markup=get_back_to_help_menu_inline(lang))
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "client_track_order")
    async def client_track_order_handler(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            track_text = (
                "📍 Buyurtmani kuzatish:\n\n"
                "Buyurtmangiz holatini bilish uchun:\n"
                "• 'Mening buyurtmalarim' bo'limiga o'ting\n"
                "• Yoki operator bilan bog'laning\n\n"
                "Buyurtma holatlari:\n"
                "🆕 Yangi - qabul qilindi\n"
                "✅ Tasdiqlangan - ishga olingan\n"
                "⏳ Jarayonda - bajarilmoqda\n"
                "✅ Bajarilgan - tugallangan"
                if lang == 'uz' else
                "📍 Отслеживание заказа:\n\n"
                "Чтобы узнать статус заказа:\n"
                "• Перейдите в 'Мои заказы'\n"
                "• Или свяжитесь с оператором\n\n"
                "Статусы заказа:\n"
                "🆕 Новый - принят\n"
                "✅ Подтвержден - взят в работу\n"
                "⏳ В процессе - выполняется\n"
                "✅ Выполнен - завершен"
            )
            await callback.message.edit_text(track_text, reply_markup=get_back_to_help_menu_inline(lang))
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "client_contact_support")
    async def client_contact_support_handler(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            support_text = (
                "📞 Qo'llab-quvvatlash xizmati:\n\n"
                "📱 Telefon: +998 90 123 45 67\n"
                "📧 Email: support@company.uz\n"
                "💬 Telegram: @support_bot\n\n"
                "🕐 Ish vaqti:\n"
                "Dushanba - Juma: 9:00 - 18:00\n"
                "Shanba: 9:00 - 14:00\n"
                "Yakshanba: Dam olish kuni\n\n"
                "Yoki botda xabar qoldiring!"
                if lang == 'uz' else
                "📞 Служба поддержки:\n\n"
                "📱 Телефон: +998 90 123 45 67\n"
                "📧 Email: support@company.uz\n"
                "💬 Telegram: @support_bot\n\n"
                "🕐 Рабочее время:\n"
                "Понедельник - Пятница: 9:00 - 18:00\n"
                "Суббота: 9:00 - 14:00\n"
                "Воскресенье: Выходной\n\n"
                "Или оставьте сообщение в боте!"
            )
            await callback.message.edit_text(support_text, reply_markup=get_back_to_help_menu_inline(lang))
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "client_back_help")
    async def client_back_help_handler(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            help_text = (
                "Yordam menyusi. Kerakli bo'limni tanlang."
                if lang == 'uz' else
                "Меню помощи. Выберите нужный раздел."
            )
            await callback.message.edit_text(help_text, reply_markup=get_client_help_menu(lang))
            await state.set_state(HelpStates.help_menu)
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
