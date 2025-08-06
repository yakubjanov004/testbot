"""
Manager Word Documents Handler - Simplified Implementation

This module handles word document generation for managers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_word_documents_keyboard
from states.manager_states import WordDocumentsStates

def get_manager_word_documents_router():
    router = Router()

    @router.message(F.text.in_(["📄 Word hujjatlar", "📄 Word документы"]))
    async def word_documents_menu(message: Message, state: FSMContext):
        """Show word documents menu"""
        try:
            docs_text = (
                "📄 **Word hujjatlar**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_word_documents_keyboard()
            await message.answer(
                text=docs_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "generate_report")
    async def generate_report(callback: CallbackQuery, state: FSMContext):
        """Generate report"""
        try:
            await callback.answer()
            
            text = (
                "📄 **Hisobot yaratish**\n\n"
                "Word formatida hisobot yaratish funksiyasi.\n\n"
                "📋 Mavjud hisobot turlari:\n"
                "• Kunlik hisobot\n"
                "• Haftalik hisobot\n"
                "• Oylik hisobot\n"
                "• Xodimlar samaradorligi\n"
                "• Texniklar hisoboti\n"
                "• Mijozlar hisoboti\n\n"
                "📊 Bugungi ma'lumotlar:\n"
                "• Jami ariyalar: 45\n"
                "• Bajarilgan: 25\n"
                "• Jarayonda: 8\n"
                "• Yangi: 12"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_docs_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "create_contract")
    async def create_contract(callback: CallbackQuery, state: FSMContext):
        """Create contract"""
        try:
            await callback.answer()
            
            text = (
                "📄 **Shartnoma yaratish**\n\n"
                "Mijozlar bilan shartnoma yaratish funksiyasi.\n\n"
                "📋 Shartnoma turlari:\n"
                "• Internet xizmati shartnomasi\n"
                "• TV xizmati shartnomasi\n"
                "• Texnik xizmat shartnomasi\n"
                "• Umumiy shartnoma\n\n"
                "👥 Mavjud mijozlar:\n"
                "• Ahmad Karimov - Internet xizmati\n"
                "• Malika Yusupova - TV xizmati\n"
                "• Bekzod Toirov - Texnik xizmat"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_docs_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "create_invoice")
    async def create_invoice(callback: CallbackQuery, state: FSMContext):
        """Create invoice"""
        try:
            await callback.answer()
            
            text = (
                "📄 **Hisob-faktura yaratish**\n\n"
                "Mijozlar uchun hisob-faktura yaratish funksiyasi.\n\n"
                "📋 Hisob-faktura turlari:\n"
                "• Internet xizmati to'lovi\n"
                "• TV xizmati to'lovi\n"
                "• Texnik xizmat to'lovi\n"
                "• Qo'shimcha xizmatlar\n\n"
                "💰 To'lov ma'lumotlari:\n"
                "• Internet: 50,000-200,000 so'm/oy\n"
                "• TV: 30,000-80,000 so'm/oy\n"
                "• Texnik xizmat: 20,000-100,000 so'm"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_docs_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_docs_menu")
    async def back_to_word_documents_menu(callback: CallbackQuery, state: FSMContext):
        """Back to word documents menu"""
        try:
            await callback.answer()
            
            docs_text = (
                "📄 **Word hujjatlar**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_word_documents_keyboard()
            await callback.message.edit_text(
                text=docs_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router 