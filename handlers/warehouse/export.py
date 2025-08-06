"""
Warehouse Export Handler - Simplified Implementation

This module handles export functionality for warehouse.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import get_export_keyboard
from states.warehouse_states import ExportStates

def get_warehouse_export_router():
    router = Router()

    @router.message(F.text.in_(["📤 Export", "📤 Экспорт"]))
    async def export_menu(message: Message, state: FSMContext):
        """Show export menu"""
        try:
            export_text = (
                "📤 **Export va hisobotlar**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_export_keyboard()
            await message.answer(
                text=export_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "export_inventory")
    async def export_inventory(callback: CallbackQuery, state: FSMContext):
        """Export inventory"""
        try:
            await callback.answer()
            
            text = (
                "📤 **Inventar export**\n\n"
                "Inventar ma'lumotlarini export qilish funksiyasi.\n\n"
                "📋 Export turlari:\n"
                "• Excel formatida\n"
                "• CSV formatida\n"
                "• PDF hisobot\n"
                "• JSON formatida\n\n"
                "📊 Mavjud ma'lumotlar:\n"
                "• Jami elementlar: 25\n"
                "• Kategoriyalar: 8\n"
                "• Kam miqdordagi: 3\n"
                "• Tugagan elementlar: 1"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_export_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "export_reports")
    async def export_reports(callback: CallbackQuery, state: FSMContext):
        """Export reports"""
        try:
            await callback.answer()
            
            text = (
                "📤 **Hisobotlar export**\n\n"
                "Turli xil hisobotlarni export qilish funksiyasi.\n\n"
                "📋 Hisobot turlari:\n"
                "• Kunlik hisobot\n"
                "• Haftalik hisobot\n"
                "• Oylik hisobot\n"
                "• Kam miqdordagi elementlar\n"
                "• Tugagan elementlar\n"
                "• Kirim-chiqim hisoboti\n\n"
                "📊 Bugungi ma'lumotlar:\n"
                "• Yangi kirimlar: 5\n"
                "• Chiqimlar: 3\n"
                "• Kam miqdordagi: 2\n"
                "• Tugagan: 1"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_export_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "export_statistics")
    async def export_statistics(callback: CallbackQuery, state: FSMContext):
        """Export statistics"""
        try:
            await callback.answer()
            
            # Mock statistics data
            statistics = {
                'total_items': 150,
                'categories': 8,
                'low_stock_items': 5,
                'out_of_stock_items': 2,
                'total_value': 25000000,
                'monthly_turnover': 5000000,
                'most_popular_items': [
                    {'name': 'Router TP-Link', 'quantity': 25},
                    {'name': 'Kabel UTP', 'quantity': 150},
                    {'name': 'TV antena', 'quantity': 8}
                ]
            }
            
            text = (
                f"📊 **Statistika export**\n\n"
                f"📈 **Umumiy ma'lumotlar:**\n"
                f"• Jami elementlar: {statistics['total_items']}\n"
                f"• Kategoriyalar: {statistics['categories']}\n"
                f"• Kam miqdordagi: {statistics['low_stock_items']}\n"
                f"• Tugagan elementlar: {statistics['out_of_stock_items']}\n\n"
                f"💰 **Moliyaviy:**\n"
                f"• Jami qiymat: {statistics['total_value']:,} so'm\n"
                f"• Oylik aylanma: {statistics['monthly_turnover']:,} so'm\n\n"
                f"🏆 **Eng ko'p talab qilinadigan:**\n"
            )
            
            for item in statistics['most_popular_items']:
                text += f"• {item['name']}: {item['quantity']} dona\n"
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_export_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_export_menu")
    async def back_to_export_menu(callback: CallbackQuery, state: FSMContext):
        """Back to export menu"""
        try:
            await callback.answer()
            
            export_text = (
                "📤 **Export va hisobotlar**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_export_keyboard()
            await callback.message.edit_text(
                text=export_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
