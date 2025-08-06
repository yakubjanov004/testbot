"""
Call Center Inbox Handler
Manages inbox messages for call center operators
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import get_inbox_menu, get_message_actions_menu

# States imports
from states.call_center import CallCenterInboxStates

def get_call_center_inbox_router():
    """Get call center inbox router"""
    router = Router()
    
    @router.callback_query(F.data.startswith("open_inbox_"))
    async def handle_inbox_notification(callback: CallbackQuery, state: FSMContext):
        """Handle inbox notification button click"""
        await callback.answer()
        
        # Extract request ID
        request_id_short = callback.data.replace("open_inbox_", "")
        
        # Show inbox
        await show_call_center_inbox_from_notification(callback.message, state, request_id_short)
    
    async def show_call_center_inbox_from_notification(message: Message, state: FSMContext, target_request_id: str = None):
        """Show call center inbox with focus on specific request"""
        # Show regular inbox
        await call_center_inbox(message, state)

    @router.message(F.text.in_(['📥 Xabarlar', '📥 Сообщения']))
    async def call_center_inbox(message: Message, state: FSMContext):
        """Handle inbox"""
        lang = 'uz'  # Default language
        
        # Mock inbox messages
        messages = [
            {
                'id': 1,
                'subject': 'Yangi zayavka #1234',
                'sender_name': 'Ahmad Karimov',
                'created_at': '2024-01-15 10:30',
                'content': 'Internet muammosi haqida'
            },
            {
                'id': 2,
                'subject': 'Texnik xizmat so\'rovi #5678',
                'sender_name': 'Malika Yusupova',
                'created_at': '2024-01-15 09:15',
                'content': 'TV kanallar ishlamayapti'
            }
        ]
        
        if not messages:
            text = "📭 Inbox bo'sh" if lang == 'uz' else "📭 Входящие пусты"
            await message.answer(text)
            return
        
        if lang == 'uz':
            text = f"📥 <b>Xabarlar ({len(messages)})</b>\n\n"
            for i, msg in enumerate(messages[:10], 1):
                text += f"{i}. {msg.get('subject', 'Mavzu yo\'q')}\n"
                text += f"   👤 {msg.get('sender_name', 'N/A')}\n"
                text += f"   ⏰ {msg.get('created_at', 'N/A')}\n\n"
        else:
            text = f"📥 <b>Сообщения ({len(messages)})</b>\n\n"
            for i, msg in enumerate(messages[:10], 1):
                text += f"{i}. {msg.get('subject', 'Нет темы')}\n"
                text += f"   👤 {msg.get('sender_name', 'N/A')}\n"
                text += f"   ⏰ {msg.get('created_at', 'N/A')}\n\n"
        
        await message.answer(
            text,
            reply_markup=get_inbox_menu(lang)
        )
        await state.set_state(CallCenterInboxStates.viewing_messages)

    @router.message(CallCenterInboxStates.viewing_messages, F.text.in_(['📖 O\'qish', '📖 Читать']))
    async def call_center_read_message(message: Message, state: FSMContext):
        """Handle read message"""
        lang = 'uz'  # Default language
        
        text = (
            "📖 Qaysi xabarni o'qimoqchisiz?\n"
            "Xabar raqamini kiriting:" if lang == 'uz'
            else "📖 Какое сообщение хотите прочитать?\n"
                 "Введите номер сообщения:"
        )
        
        await message.answer(text)
        await state.set_state(CallCenterInboxStates.entering_message_number)

    @router.message(CallCenterInboxStates.entering_message_number)
    async def call_center_process_message_number(message: Message, state: FSMContext):
        """Process message number"""
        lang = 'uz'  # Default language
        
        # Validate message number
        try:
            message_number = int(message.text)
            if message_number < 1 or message_number > 10:
                raise ValueError("Invalid number")
        except ValueError:
            text = (
                "❌ Noto'g'ri raqam. 1-10 oralig'ida kiriting." if lang == 'uz'
                else "❌ Неверный номер. Введите от 1 до 10."
            )
            await message.answer(text)
            await state.clear()
            return
        
        # Mock message details
        message_details = {
            'id': message_number,
            'subject': f'Xabar #{message_number}',
            'sender_name': 'Test User',
            'created_at': '2024-01-15 10:30',
            'content': f'Bu {message_number} raqamli xabar matni'
        }
        
        if lang == 'uz':
            text = (
                f"📖 <b>Xabar #{message_number}</b>\n\n"
                f"📧 <b>Mavzu:</b> {message_details.get('subject', 'Mavzu yo\'q')}\n"
                f"👤 <b>Yuboruvchi:</b> {message_details.get('sender_name', 'N/A')}\n"
                f"⏰ <b>Sana:</b> {message_details.get('created_at', 'N/A')}\n\n"
                f"📝 <b>Matn:</b>\n{message_details.get('content', 'Matn yo\'q')}"
            )
        else:
            text = (
                f"📖 <b>Сообщение #{message_number}</b>\n\n"
                f"📧 <b>Тема:</b> {message_details.get('subject', 'Нет темы')}\n"
                f"👤 <b>Отправитель:</b> {message_details.get('sender_name', 'N/A')}\n"
                f"⏰ <b>Дата:</b> {message_details.get('created_at', 'N/A')}\n\n"
                f"📝 <b>Текст:</b>\n{message_details.get('content', 'Нет текста')}"
            )
        
        await message.answer(
            text,
            reply_markup=get_message_actions_menu(lang)
        )
        await state.update_data(current_message_id=message_details.get('id'))
        await state.set_state(CallCenterInboxStates.viewing_message_details)

    @router.message(CallCenterInboxStates.viewing_message_details, F.text.in_(['✅ O\'qildi', '✅ Прочитано']))
    async def call_center_mark_as_read(message: Message, state: FSMContext):
        """Mark message as read"""
        lang = 'uz'  # Default language
        
        success_text = (
            "✅ Xabar o'qildi deb belgilandi!" if lang == 'uz'
            else "✅ Сообщение отмечено как прочитанное!"
        )
        
        await message.answer(success_text)
        await state.clear()

    @router.message(CallCenterInboxStates.viewing_messages, F.text.in_(['⬅️ Orqaga', '⬅️ Назад']))
    async def call_center_inbox_back(message: Message, state: FSMContext):
        """Handle back to main menu"""
        lang = 'uz'  # Default language
        
        await message.answer(
            "🏠 Bosh sahifaga qaytdingiz" if lang == 'uz' else "🏠 Вернулись на главную страницу"
        )
        await state.clear()

    return router

async def show_call_center_inbox(message: Message):
    """Show call center inbox"""
    lang = 'uz'  # Default language
    
    # Mock inbox messages
    messages = [
        {
            'id': 1,
            'subject': 'Yangi zayavka #1234',
            'sender_name': 'Ahmad Karimov',
            'created_at': '2024-01-15 10:30',
            'content': 'Internet muammosi haqida'
        },
        {
            'id': 2,
            'subject': 'Texnik xizmat so\'rovi #5678',
            'sender_name': 'Malika Yusupova',
            'created_at': '2024-01-15 09:15',
            'content': 'TV kanallar ishlamayapti'
        }
    ]
    
    if not messages:
        text = (
            "📥 Yangi xabarlar yo'q." if lang == 'uz'
            else "📥 Новых сообщений нет."
        )
        await message.answer(text)
    else:
        if lang == 'uz':
            text = f"📥 <b>Xabarlar ({len(messages)})</b>\n\n"
            for i, msg in enumerate(messages[:10], 1):
                text += f"{i}. {msg.get('subject', 'Mavzu yo\'q')}\n"
                text += f"   👤 {msg.get('sender_name', 'N/A')}\n"
                text += f"   ⏰ {msg.get('created_at', 'N/A')}\n\n"
        else:
            text = f"📥 <b>Сообщения ({len(messages)})</b>\n\n"
            for i, msg in enumerate(messages[:10], 1):
                text += f"{i}. {msg.get('subject', 'Нет темы')}\n"
                text += f"   👤 {msg.get('sender_name', 'N/A')}\n"
                text += f"   ⏰ {msg.get('created_at', 'N/A')}\n\n"
        
        await message.answer(
            text,
            reply_markup=get_inbox_menu(lang)
        )
