"""
Warehouse Inventory Handler - Simplified Implementation

This module handles inventory management for warehouse.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import get_inventory_keyboard
from states.warehouse_states import InventoryStates

def get_warehouse_inventory_router():
    router = Router()

    @router.message(F.text.in_(["📦 Inventar", "📦 Инвентарь"]))
    async def inventory_menu(message: Message, state: FSMContext):
        """Show inventory menu"""
        try:
            inv_text = (
                "📦 **Inventar boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_inventory_keyboard()
            await message.answer(
                text=inv_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_inventory")
    async def view_inventory(callback: CallbackQuery, state: FSMContext):
        """View inventory"""
        try:
            await callback.answer()
            
            # Mock inventory data
            inventory = [
                {
                    'id': 'INV001',
                    'name': 'Router TP-Link',
                    'category': 'Internet jihozlari',
                    'quantity': 25,
                    'min_quantity': 5,
                    'location': 'A1-B2'
                },
                {
                    'id': 'INV002',
                    'name': 'Kabel UTP',
                    'category': 'Kabellar',
                    'quantity': 150,
                    'min_quantity': 20,
                    'location': 'C3-D4'
                },
                {
                    'id': 'INV003',
                    'name': 'TV antena',
                    'category': 'TV jihozlari',
                    'quantity': 8,
                    'min_quantity': 10,
                    'location': 'E5-F6'
                }
            ]
            
            text = "📦 **Inventar ro'yxati**\n\n"
            for item in inventory:
                status_emoji = '🟢' if item['quantity'] >= item['min_quantity'] else '🔴'
                text += (
                    f"{status_emoji} **{item['id']}** - {item['name']}\n"
                    f"📋 Kategoriya: {item['category']}\n"
                    f"📊 Miqdori: {item['quantity']} dona\n"
                    f"⚠️ Minimal: {item['min_quantity']} dona\n"
                    f"📍 Joylashuv: {item['location']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_inv_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "add_inventory")
    async def add_inventory(callback: CallbackQuery, state: FSMContext):
        """Add inventory item"""
        try:
            await callback.answer()
            
            text = (
                "➕ **Inventar qo'shish**\n\n"
                "Yangi inventar elementini qo'shish funksiyasi.\n\n"
                "📋 Qo'shiladigan elementlar:\n"
                "• Router TP-Link - 10 dona\n"
                "• Kabel UTP - 50 metr\n"
                "• TV antena - 5 dona\n"
                "• Modem - 3 dona\n\n"
                "📍 Joylashuvlar:\n"
                "• A1-B2 - Internet jihozlari\n"
                "• C3-D4 - Kabellar\n"
                "• E5-F6 - TV jihozlari"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_inv_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "low_stock")
    async def low_stock(callback: CallbackQuery, state: FSMContext):
        """Show low stock items"""
        try:
            await callback.answer()
            
            # Mock low stock data
            low_stock_items = [
                {
                    'id': 'INV003',
                    'name': 'TV antena',
                    'quantity': 8,
                    'min_quantity': 10,
                    'location': 'E5-F6'
                },
                {
                    'id': 'INV004',
                    'name': 'Modem',
                    'quantity': 2,
                    'min_quantity': 5,
                    'location': 'A1-B2'
                }
            ]
            
            text = "⚠️ **Kam miqdordagi elementlar**\n\n"
            for item in low_stock_items:
                text += (
                    f"🔴 **{item['id']}** - {item['name']}\n"
                    f"📊 Mavjud: {item['quantity']} dona\n"
                    f"⚠️ Minimal: {item['min_quantity']} dona\n"
                    f"📍 Joylashuv: {item['location']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_inv_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_inv_menu")
    async def back_to_inventory_menu(callback: CallbackQuery, state: FSMContext):
        """Back to inventory menu"""
        try:
            await callback.answer()
            
            inv_text = (
                "📦 **Inventar boshqaruvi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_inventory_keyboard()
            await callback.message.edit_text(
                text=inv_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
