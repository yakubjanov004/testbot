from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_help_menu_keyboard, get_back_to_help_menu_keyboard
from states.client_states import HelpStates
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

async def answer_and_cleanup(callback, cleanup_after=True):
    """Mock answer and cleanup"""
    await callback.answer()

def get_client_help_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["❓ Yordam"]))
    async def client_help_handler(message: Message, state: FSMContext):
        """Client help handler (inline version)"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return

            help_text = "Yordam menyusi. Kerakli bo'limni tanlang."

            sent_message = await message.answer(
                help_text,
                reply_markup=get_help_menu_keyboard('uz')
            )
            # Save last message id for inline cleanup
            await state.update_data(last_message_id=sent_message.message_id)
            await state.set_state(HelpStates.help_menu)

        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    # Foydalanuvchi matn yuborganida inline tugmalarni o'chirish
    @router.message(HelpStates.help_menu, F.text)
    async def clear_inline_on_text(message: Message, state: FSMContext):
        """Inline tugmalarni o'chirish va holatni tiklash (inline version)"""
        try:
            data = await state.get_data()
            last_message_id = data.get('last_message_id')

            if last_message_id:
                try:
                    await message.bot.edit_message_reply_markup(
                        chat_id=message.from_user.id,
                        message_id=last_message_id,
                        reply_markup=None
                    )
                except Exception:
                    pass

            await state.set_state(HelpStates.main_menu)

        except Exception as e:
            await state.set_state(HelpStates.main_menu)

    @router.callback_query(F.data == "client_faq")
    async def client_faq_handler(callback: CallbackQuery, state: FSMContext):
        """Tez-tez so'raladigan savollar (inline)"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
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
            )

            await callback.message.edit_text(
                faq_text,
                reply_markup=get_back_to_help_menu_keyboard('uz')
            )
            await state.update_data(last_message_id=callback.message.message_id)

        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "client_how_to_order")
    async def client_how_to_order_handler(callback: CallbackQuery, state: FSMContext):
        """Qanday buyurtma berish (inline)"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
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
            )

            await callback.message.edit_text(
                guide_text,
                reply_markup=get_back_to_help_menu_keyboard('uz')
            )
            await state.update_data(last_message_id=callback.message.message_id)

        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "client_track_order")
    async def client_track_order_handler(callback: CallbackQuery, state: FSMContext):
        """Buyurtmani kuzatish (inline)"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
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
            )

            await callback.message.edit_text(
                track_text,
                reply_markup=get_back_to_help_menu_keyboard('uz')
            )
            await state.update_data(last_message_id=callback.message.message_id)

        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "client_contact_support")
    async def client_contact_support_handler(callback: CallbackQuery, state: FSMContext):
        """Qo'llab-quvvatlash xizmati (inline)"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
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
            )

            await callback.message.edit_text(
                support_text,
                reply_markup=get_back_to_help_menu_keyboard('uz')
            )
            await state.update_data(last_message_id=callback.message.message_id)

        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "client_back_help")
    async def client_back_help_handler(callback: CallbackQuery, state: FSMContext):
        """Yordam bo'limiga qaytish (inline)"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            help_text = "Yordam bo'limi"

            await callback.message.edit_text(
                help_text,
                reply_markup=get_help_menu_keyboard('uz')
            )
            await state.update_data(last_message_id=callback.message.message_id)

        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "client_contact_operator")
    async def client_contact_operator_handler(callback: CallbackQuery, state: FSMContext):
        """Operator bilan bog'lanish (inline)"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
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
            )

            await callback.message.edit_text(
                support_text,
                reply_markup=get_back_to_help_menu_keyboard('uz')
            )
            await state.update_data(last_message_id=callback.message.message_id)

        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router
