"""
Warehouse Statistics Handler - Simplified Implementation

This module handles statistics functionality for warehouse.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import get_statistics_keyboard
from states.warehouse_states import StatisticsStates

def get_warehouse_statistics_router():
    router = Router()

    @router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
    async def statistics_menu(message: Message, state: FSMContext):
        """Show statistics menu"""
        try:
            stats_text = (
                "📊 **Statistika va hisobotlar**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_statistics_keyboard()
            await message.answer(
                text=stats_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "daily_statistics")
    async def daily_statistics(callback: CallbackQuery, state: FSMContext):
        """Show daily statistics"""
        try:
            await callback.answer()
            
            # Mock daily statistics
            daily_stats = {
                'total_items': 150,
                'new_items': 5,
                'issued_items': 8,
                'low_stock_items': 3,
                'out_of_stock_items': 1,
                'total_value': 25000000,
                'issued_value': 2000000
            }
            
            text = (
                f"📊 **Kunlik statistika**\n\n"
                f"📦 **Inventar:**\n"
                f"• Jami elementlar: {daily_stats['total_items']}\n"
                f"• Yangi elementlar: {daily_stats['new_items']}\n"
                f"• Chiqarilgan: {daily_stats['issued_items']}\n"
                f"• Kam miqdordagi: {daily_stats['low_stock_items']}\n"
                f"• Tugagan: {daily_stats['out_of_stock_items']}\n\n"
                f"💰 **Moliyaviy:**\n"
                f"• Jami qiymat: {daily_stats['total_value']:,} so'm\n"
                f"• Chiqarilgan qiymat: {daily_stats['issued_value']:,} so'm"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_stats_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "weekly_statistics")
    async def weekly_statistics(callback: CallbackQuery, state: FSMContext):
        """Show weekly statistics"""
        try:
            await callback.answer()
            
            # Mock weekly statistics
            weekly_stats = {
                'total_items': 150,
                'issued_items': 45,
                'returned_items': 3,
                'total_value': 25000000,
                'issued_value': 5000000,
                'popular_items': [
                    {'name': 'Router TP-Link', 'issued': 15},
                    {'name': 'Kabel UTP', 'issued': 25},
                    {'name': 'TV antena', 'issued': 8}
                ]
            }
            
            text = (
                f"📊 **Haftalik statistika**\n\n"
                f"📦 **Inventar:**\n"
                f"• Jami elementlar: {weekly_stats['total_items']}\n"
                f"• Chiqarilgan: {weekly_stats['issued_items']}\n"
                f"• Qaytarilgan: {weekly_stats['returned_items']}\n\n"
                f"💰 **Moliyaviy:**\n"
                f"• Jami qiymat: {weekly_stats['total_value']:,} so'm\n"
                f"• Chiqarilgan qiymat: {weekly_stats['issued_value']:,} so'm\n\n"
                f"🏆 **Eng ko'p chiqariladigan elementlar:**\n"
            )
            
            for item in weekly_stats['popular_items']:
                text += f"• {item['name']}: {item['issued']} dona\n"
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_stats_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "inventory_report")
    async def inventory_report(callback: CallbackQuery, state: FSMContext):
        """Show inventory report"""
        try:
            await callback.answer()
            
            # Mock inventory report data
            inventory_report = {
                'categories': [
                    {'name': 'Internet jihozlari', 'count': 25, 'value': 10000000},
                    {'name': 'TV jihozlari', 'count': 15, 'value': 5000000},
                    {'name': 'Kabellar', 'count': 50, 'value': 2000000},
                    {'name': 'Qo\'shimcha jihozlari', 'count': 30, 'value': 3000000}
                ],
                'low_stock_items': [
                    {'name': 'TV antena', 'quantity': 8, 'min_quantity': 10},
                    {'name': 'Modem', 'quantity': 2, 'min_quantity': 5}
                ],
                'out_of_stock_items': [
                    {'name': 'Eski router', 'quantity': 0, 'min_quantity': 2}
                ]
            }
            
            text = (
                "📊 **Inventar hisoboti**\n\n"
                "📋 **Kategoriyalar bo'yicha:**\n"
            )
            
            for category in inventory_report['categories']:
                text += (
                    f"• {category['name']}: {category['count']} dona, "
                    f"{category['value']:,} so'm\n"
                )
            
            text += f"\n⚠️ **Kam miqdordagi elementlar:**\n"
            for item in inventory_report['low_stock_items']:
                text += (
                    f"• {item['name']}: {item['quantity']}/{item['min_quantity']} dona\n"
                )
            
            text += f"\n❌ **Tugagan elementlar:**\n"
            for item in inventory_report['out_of_stock_items']:
                text += (
                    f"• {item['name']}: {item['quantity']}/{item['min_quantity']} dona\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_stats_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_stats_menu")
    async def back_to_statistics_menu(callback: CallbackQuery, state: FSMContext):
        """Back to statistics menu"""
        try:
            await callback.answer()
            
            stats_text = (
                "📊 **Statistika va hisobotlar**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_statistics_keyboard()
            await callback.message.edit_text(
                text=stats_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
