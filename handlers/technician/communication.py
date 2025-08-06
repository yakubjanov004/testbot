"""
Technician Communication Handler - Simplified Implementation

This module handles communication for technicians.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.technician_buttons import get_communication_keyboard
from states.technician_states import CommunicationStates

def get_technician_communication_router():
    router = Router()

    @router.message(F.text.in_(["💬 Aloqa", "💬 Связь"]))
    async def communication_menu(message: Message, state: FSMContext):
        """Show communication menu"""
        try:
            comm_text = (
                "💬 **Aloqa va xabarlar**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_communication_keyboard()
            await message.answer(
                text=comm_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "contact_client")
    async def contact_client(callback: CallbackQuery, state: FSMContext):
        """Contact client"""
        try:
            await callback.answer()
            
            text = (
                "📞 **Mijoz bilan bog'lanish**\n\n"
                "Mijoz bilan bog'lanish funksiyasi.\n\n"
                "📋 Joriy buyurtmalar:\n"
                "• ORD001 - Ahmad Karimov (+998901234567)\n"
                "• ORD002 - Malika Yusupova (+998901234568)\n\n"
                "💬 Xabar turi:\n"
                "• Buyurtma holati haqida\n"
                "• Kelishilgan vaqt haqida\n"
                "• Texnik muammo haqida\n"
                "• Boshqa savollar"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_comm_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "contact_manager")
    async def contact_manager(callback: CallbackQuery, state: FSMContext):
        """Contact manager"""
        try:
            await callback.answer()
            
            text = (
                "👨‍💼 **Menejer bilan bog'lanish**\n\n"
                "Menejer bilan bog'lanish funksiyasi.\n\n"
                "👨‍💼 Mavjud menejerlar:\n"
                "• Aziz Karimov (Katta menejer) - +998901234569\n"
                "• Malika Yusupova (Menejer) - +998901234570\n"
                "• Bekzod Toirov (Kichik menejer) - +998901234571\n\n"
                "💬 Xabar turi:\n"
                "• Buyurtma holati haqida\n"
                "• Texnik muammo haqida\n"
                "• Qo'shimcha yordam haqida\n"
                "• Boshqa savollar"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_comm_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "send_report")
    async def send_report(callback: CallbackQuery, state: FSMContext):
        """Send report"""
        try:
            await callback.answer()
            
            text = (
                "📋 **Hisobot yuborish**\n\n"
                "Hisobot yuborish funksiyasi.\n\n"
                "📋 Hisobot turlari:\n"
                "• Kunlik hisobot\n"
                "• Buyurtma hisoboti\n"
                "• Texnik hisobot\n"
                "• Muammo hisoboti\n\n"
                "📊 Bugungi ma'lumotlar:\n"
                "• Bajarilgan buyurtmalar: 5\n"
                "• Kutilayotgan buyurtmalar: 2\n"
                "• Muammolar: 1\n"
                "• Ish vaqti: 8 soat"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_comm_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_comm_menu")
    async def back_to_communication_menu(callback: CallbackQuery, state: FSMContext):
        """Back to communication menu"""
        try:
            await callback.answer()
            
            comm_text = (
                "💬 **Aloqa va xabarlar**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_communication_keyboard()
            await callback.message.edit_text(
                text=comm_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
