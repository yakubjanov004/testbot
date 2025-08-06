"""
Client Help Handler - Simplified Implementation

This module handles help and support for clients.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_help_keyboard
from states.client_states import HelpStates

def get_client_help_router():
    router = Router()

    @router.message(F.text.in_(["❓ Yordam", "❓ Помощь"]))
    async def help_menu(message: Message, state: FSMContext):
        """Show help menu"""
        try:
            help_text = (
                "❓ **Yordam va qo'llab-quvvatlash**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_help_keyboard()
            await message.answer(
                text=help_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "faq")
    async def show_faq(callback: CallbackQuery, state: FSMContext):
        """Show frequently asked questions"""
        try:
            await callback.answer()
            
            faq_text = (
                "❓ **Ko'p so'raladigan savollar**\n\n"
                "**Q: Internet ulanish uchun qanday ariza berish kerak?**\n"
                "A: Asosiy menyuda '🔌 Ulanish uchun ariza' tugmasini bosing va ko'rsatmalarga amal qiling.\n\n"
                "**Q: Texnik muammo bo'lsa nima qilish kerak?**\n"
                "A: '🔧 Texnik xizmat' bo'limidan ariza yarating va muammoni batafsil tasvirlab bering.\n\n"
                "**Q: Buyurtma holatini qanday tekshirish mumkin?**\n"
                "A: '📋 Mening buyurtmalarim' bo'limida barcha buyurtmalaringizni ko'rishingiz mumkin.\n\n"
                "**Q: Qo'ng'iroq orqali bog'lanish mumkinmi?**\n"
                "A: Ha, +998901234567 raqamiga qo'ng'iroq qilishingiz mumkin.\n\n"
                "**Q: Ariza qabul qilindimi qanday bilish mumkin?**\n"
                "A: Ariza yaratganingizda sizga tasdiqlash xabari yuboriladi."
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_help_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=faq_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "contact_support")
    async def contact_support(callback: CallbackQuery, state: FSMContext):
        """Show contact support information"""
        try:
            await callback.answer()
            
            support_text = (
                "📞 **Qo'llab-quvvatlash bilan bog'lanish**\n\n"
                "**📱 Telefon raqamlar:**\n"
                "• Asosiy: +998901234567\n"
                "• Texnik yordam: +998901234568\n"
                "• Qo'ng'iroq markazi: +998901234569\n\n"
                "**📧 Email manzillar:**\n"
                "• Umumiy: info@alfaconnect.uz\n"
                "• Texnik yordam: support@alfaconnect.uz\n"
                "• Shikoyatlar: complaints@alfaconnect.uz\n\n"
                "**⏰ Ish vaqti:**\n"
                "• Dushanba - Juma: 09:00 - 18:00\n"
                "• Shanba: 09:00 - 15:00\n"
                "• Yakshanba: Dam olish kuni\n\n"
                "**📍 Manzil:**\n"
                "Toshkent shahri, Chilonzor tumani, 15-uy"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_help_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=support_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "service_info")
    async def show_service_info(callback: CallbackQuery, state: FSMContext):
        """Show service information"""
        try:
            await callback.answer()
            
            service_text = (
                "📋 **Xizmatlar haqida ma'lumot**\n\n"
                "**🔌 Internet ulanish:**\n"
                "• Tezlik: 10-100 Mbps\n"
                "• Narx: 50,000-200,000 so'm/oy\n"
                "• O'rnatish: 1-3 kun\n\n"
                "**📺 TV xizmati:**\n"
                "• Kanallar: 100+ ta\n"
                "• HD sifat: Mavjud\n"
                "• Narx: 30,000-80,000 so'm/oy\n\n"
                "**🔧 Texnik xizmat:**\n"
                "• Bepul diagnostika\n"
                "• 24 soat ichida javob\n"
                "• Malakali texniklar\n\n"
                "**📱 Mobil xizmatlar:**\n"
                "• 4G/5G internet\n"
                "• Cheksiz qo'ng'iroqlar\n"
                "• SMS paketlari"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_help_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=service_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_help_menu")
    async def back_to_help_menu(callback: CallbackQuery, state: FSMContext):
        """Back to help menu"""
        try:
            await callback.answer()
            
            help_text = (
                "❓ **Yordam va qo'llab-quvvatlash**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_help_keyboard()
            await callback.message.edit_text(
                text=help_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
