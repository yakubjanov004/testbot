"""
Warehouse Inbox Handler - Simplified Implementation

This module handles inbox functionality for warehouse.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import get_inbox_keyboard
from states.warehouse_states import InboxStates

def get_warehouse_inbox_router():
    router = Router()

    @router.message(F.text.in_(["📥 Kirish qutisi", "📥 Входящие"]))
    async def inbox_menu(message: Message, state: FSMContext):
        """Show inbox menu"""
        try:
            inbox_text = (
                "📥 **Kirish qutisi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_inbox_keyboard()
            await message.answer(
                text=inbox_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_inbox_messages")
    async def view_inbox_messages(callback: CallbackQuery, state: FSMContext):
        """View inbox messages"""
        try:
            await callback.answer()
            
            # Mock inbox messages data
            messages = [
                {
                    'id': 'MSG001',
                    'sender': 'Aziz Karimov',
                    'subject': 'Yangi materiallar kerak',
                    'content': 'Router va kabel materiallari kerak',
                    'priority': 'Yuqori',
                    'received': '2024-01-15 10:30',
                    'status': 'O\'qilmagan'
                },
                {
                    'id': 'MSG002',
                    'sender': 'Malika Yusupova',
                    'subject': 'Inventar hisoboti',
                    'content': 'Haftalik inventar hisobotini yuboring',
                    'priority': 'O\'rta',
                    'received': '2024-01-15 11:45',
                    'status': 'O\'qilgan'
                },
                {
                    'id': 'MSG003',
                    'sender': 'Bekzod Toirov',
                    'subject': 'Materiallar yetarli emas',
                    'content': 'TV antena materiallari tugab qolyapti',
                    'priority': 'Yuqori',
                    'received': '2024-01-15 09:15',
                    'status': 'O\'qilgan'
                }
            ]
            
            text = "📥 **Kirish qutisi xabarlari**\n\n"
            for msg in messages:
                priority_emoji = {
                    'Yuqori': '🔴',
                    'O\'rta': '🟡',
                    'Past': '🟢'
                }.get(msg['priority'], '⚪')
                
                status_emoji = '🔵' if msg['status'] == 'O\'qilmagan' else '⚪'
                
                text += (
                    f"{status_emoji} **{msg['id']}** - {msg['subject']}\n"
                    f"👤 Yuboruvchi: {msg['sender']}\n"
                    f"{priority_emoji} Daraja: {msg['priority']}\n"
                    f"📝 Matn: {msg['content']}\n"
                    f"📅 Vaqt: {msg['received']}\n\n"
                )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_inbox_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mark_as_read")
    async def mark_as_read(callback: CallbackQuery, state: FSMContext):
        """Mark messages as read"""
        try:
            await callback.answer()
            
            text = (
                "📥 **Xabarlarni o'qilgan deb belgilash**\n\n"
                "Xabarlarni o'qilgan deb belgilash funksiyasi.\n\n"
                "📋 O'qilmagan xabarlar:\n"
                "• MSG001 - Aziz Karimov (Yangi materiallar kerak)\n"
                "• MSG003 - Bekzod Toirov (Materiallar yetarli emas)\n\n"
                "✅ O'qilgan xabarlar:\n"
                "• MSG002 - Malika Yusupova (Inventar hisoboti)\n\n"
                "📊 Umumiy ma'lumotlar:\n"
                "• Jami xabarlar: 3\n"
                "• O'qilmagan: 2\n"
                "• O'qilgan: 1"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_inbox_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "delete_messages")
    async def delete_messages(callback: CallbackQuery, state: FSMContext):
        """Delete messages"""
        try:
            await callback.answer()
            
            text = (
                "🗑️ **Xabarlarni o'chirish**\n\n"
                "Xabarlarni o'chirish funksiyasi.\n\n"
                "📋 O'chiriladigan xabarlar:\n"
                "• MSG001 - Aziz Karimov (Yangi materiallar kerak)\n"
                "• MSG002 - Malika Yusupova (Inventar hisoboti)\n"
                "• MSG003 - Bekzod Toirov (Materiallar yetarli emas)\n\n"
                "⚠️ Eslatma:\n"
                "• O'chirilgan xabarlar tiklanmaydi\n"
                "• Faqat o'qilgan xabarlarni o'chirish mumkin\n"
                "• Muhim xabarlarni saqlab qolishni unutmang"
            )
            
            keyboard = [
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_inbox_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_inbox_menu")
    async def back_to_inbox_menu(callback: CallbackQuery, state: FSMContext):
        """Back to inbox menu"""
        try:
            await callback.answer()
            
            inbox_text = (
                "📥 **Kirish qutisi**\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = get_inbox_keyboard()
            await callback.message.edit_text(
                text=inbox_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router