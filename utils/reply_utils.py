"""
Reply Utilities Module

Bu modul controller uchun barcha reply va inline response'larni boshqarish uchun utility funksiyalarini o'z ichiga oladi.
"""

from typing import Union, Optional, Dict, Any
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
import asyncio


class ReplyManager:
    """Universal reply manager for controller handlers"""
    
    def __init__(self, state: FSMContext):
        self.state = state
        self.current_message_id: Optional[int] = None
    
    async def get_current_message_id(self) -> Optional[int]:
        """Get current message ID from state"""
        data = await self.state.get_data()
        return data.get("current_message_id")
    
    async def set_current_message_id(self, message_id: int):
        """Set current message ID in state"""
        await self.state.update_data(current_message_id=message_id)
    
    async def clear_current_message_id(self):
        """Clear current message ID from state"""
        await self.state.update_data(current_message_id=None)


async def send_or_edit_message(
    event: Union[Message, CallbackQuery],
    text: str,
    state: FSMContext,
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
    parse_mode: str = "HTML",
    **kwargs
) -> int:
    """
    Universal function to send or edit messages
    
    Args:
        event: Message or CallbackQuery event
        text: Message text
        state: FSM context
        reply_markup: Optional keyboard markup
        parse_mode: Parse mode (default: HTML)
        **kwargs: Additional message parameters
    
    Returns:
        int: Message ID
    """
    data = await state.get_data()
    current_message_id = data.get("current_message_id")
    chat_id = event.from_user.id
    
    try:
        if current_message_id:
            # Try to edit existing message
            await event.bot.edit_message_text(
                chat_id=chat_id,
                message_id=current_message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                **kwargs
            )
            return current_message_id
        else:
            # Send new message
            message = await event.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                **kwargs
            )
            await state.update_data(current_message_id=message.message_id)
            return message.message_id
            
    except Exception as e:
        print(f"Error in send_or_edit_message: {e}")
        try:
            # If editing failed, delete old message and send new one
            if current_message_id:
                await event.bot.delete_message(chat_id=chat_id, message_id=current_message_id)
        except Exception as del_e:
            print(f"Error deleting old message: {del_e}")
        
        # Send new message
        message = await event.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            **kwargs
        )
        await state.update_data(current_message_id=message.message_id)
        return message.message_id


async def answer_callback_query(
    callback: CallbackQuery,
    text: str = "",
    show_alert: bool = False,
    **kwargs
):
    """
    Safely answer callback query
    
    Args:
        callback: CallbackQuery object
        text: Answer text
        show_alert: Whether to show alert
        **kwargs: Additional parameters
    """
    try:
        await callback.answer(text=text, show_alert=show_alert, **kwargs)
    except Exception as e:
        print(f"Error answering callback query: {e}")


async def send_error_message(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    error_text: str = "❌ Xatolik yuz berdi",
    **kwargs
) -> int:
    """
    Send error message with proper handling
    
    Args:
        event: Message or CallbackQuery event
        state: FSM context
        error_text: Error message text
        **kwargs: Additional parameters
    
    Returns:
        int: Message ID
    """
    if isinstance(event, CallbackQuery):
        await answer_callback_query(event, error_text, show_alert=True)
        return 0
    
    return await send_or_edit_message(event, error_text, state, **kwargs)


async def send_success_message(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    success_text: str = "✅ Muvaffaqiyatli bajarildi",
    **kwargs
) -> int:
    """
    Send success message with proper handling
    
    Args:
        event: Message or CallbackQuery event
        state: FSM context
        success_text: Success message text
        **kwargs: Additional parameters
    
    Returns:
        int: Message ID
    """
    if isinstance(event, CallbackQuery):
        await answer_callback_query(event, success_text, show_alert=True)
        return 0
    
    return await send_or_edit_message(event, success_text, state, **kwargs)


async def handle_inline_response(
    callback: CallbackQuery,
    state: FSMContext,
    response_text: str,
    show_alert: bool = True,
    **kwargs
):
    """
    Handle inline response for callback queries
    
    Args:
        callback: CallbackQuery object
        state: FSM context
        response_text: Response text
        show_alert: Whether to show alert
        **kwargs: Additional parameters
    """
    await answer_callback_query(callback, response_text, show_alert=show_alert, **kwargs)


async def clear_message_state(state: FSMContext):
    """
    Clear message state
    
    Args:
        state: FSM context
    """
    await state.update_data(current_message_id=None)


async def update_message_with_progress(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    progress_text: str,
    **kwargs
) -> int:
    """
    Update message with progress information
    
    Args:
        event: Message or CallbackQuery event
        state: FSM context
        progress_text: Progress text
        **kwargs: Additional parameters
    
    Returns:
        int: Message ID
    """
    return await send_or_edit_message(event, progress_text, state, **kwargs)


async def send_confirmation_message(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    confirmation_text: str,
    confirm_callback_data: str,
    cancel_callback_data: str,
    **kwargs
) -> int:
    """
    Send confirmation message with yes/no buttons
    
    Args:
        event: Message or CallbackQuery event
        state: FSM context
        confirmation_text: Confirmation text
        confirm_callback_data: Confirm button callback data
        cancel_callback_data: Cancel button callback data
        **kwargs: Additional parameters
    
    Returns:
        int: Message ID
    """
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data=confirm_callback_data),
            InlineKeyboardButton(text="❌ Yo'q", callback_data=cancel_callback_data)
        ]
    ])
    
    return await send_or_edit_message(
        event, 
        confirmation_text, 
        state, 
        reply_markup=keyboard,
        **kwargs
    )


async def send_list_message(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    title: str,
    items: list,
    item_formatter: callable = None,
    empty_text: str = "Hech qanday ma'lumot topilmadi",
    **kwargs
) -> int:
    """
    Send formatted list message
    
    Args:
        event: Message or CallbackQuery event
        state: FSM context
        title: List title
        items: List of items
        item_formatter: Function to format each item
        empty_text: Text to show when list is empty
        **kwargs: Additional parameters
    
    Returns:
        int: Message ID
    """
    if not items:
        text = f"{title}\n\n{empty_text}"
    else:
        text = f"{title}\n\n"
        for i, item in enumerate(items, 1):
            if item_formatter:
                text += item_formatter(item, i)
            else:
                text += f"{i}. {str(item)}\n"
    
    return await send_or_edit_message(event, text, state, **kwargs)


async def send_paginated_message(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    title: str,
    items: list,
    page: int = 1,
    items_per_page: int = 10,
    item_formatter: callable = None,
    navigation_callback_prefix: str = "page",
    **kwargs
) -> int:
    """
    Send paginated message with navigation
    
    Args:
        event: Message or CallbackQuery event
        state: FSM context
        title: Message title
        items: List of items
        page: Current page (1-based)
        items_per_page: Items per page
        item_formatter: Function to format each item
        navigation_callback_prefix: Prefix for navigation callback data
        **kwargs: Additional parameters
    
    Returns:
        int: Message ID
    """
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    
    total_pages = (len(items) + items_per_page - 1) // items_per_page
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_items = items[start_idx:end_idx]
    
    # Format text
    text = f"{title}\n\n"
    if not page_items:
        text += "Hech qanday ma'lumot topilmadi"
    else:
        for i, item in enumerate(page_items, start_idx + 1):
            if item_formatter:
                text += item_formatter(item, i)
            else:
                text += f"{i}. {str(item)}\n"
    
    text += f"\n📄 Sahifa {page}/{total_pages}"
    
    # Create navigation keyboard
    keyboard_buttons = []
    if total_pages > 1:
        nav_row = []
        if page > 1:
            nav_row.append(InlineKeyboardButton(
                text="◀️ Oldingi", 
                callback_data=f"{navigation_callback_prefix}_prev_{page}"
            ))
        if page < total_pages:
            nav_row.append(InlineKeyboardButton(
                text="Keyingi ▶️", 
                callback_data=f"{navigation_callback_prefix}_next_{page}"
            ))
        if nav_row:
            keyboard_buttons.append(nav_row)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons) if keyboard_buttons else None
    
    return await send_or_edit_message(event, text, state, reply_markup=keyboard, **kwargs)


# Convenience functions for common reply patterns
async def reply_with_loading(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    loading_text: str = "⏳ Yuklanmoqda...",
    **kwargs
) -> int:
    """Send loading message"""
    return await send_or_edit_message(event, loading_text, state, **kwargs)


async def reply_with_error(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    error_text: str = "❌ Xatolik yuz berdi",
    **kwargs
) -> int:
    """Send error message"""
    return await send_error_message(event, state, error_text, **kwargs)


async def reply_with_success(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    success_text: str = "✅ Muvaffaqiyatli bajarildi",
    **kwargs
) -> int:
    """Send success message"""
    return await send_success_message(event, state, success_text, **kwargs)


async def reply_with_info(
    event: Union[Message, CallbackQuery],
    state: FSMContext,
    info_text: str,
    **kwargs
) -> int:
    """Send info message"""
    return await send_or_edit_message(event, info_text, state, **kwargs)


# Export all functions
__all__ = [
    'ReplyManager',
    'send_or_edit_message',
    'answer_callback_query',
    'send_error_message',
    'send_success_message',
    'handle_inline_response',
    'clear_message_state',
    'update_message_with_progress',
    'send_confirmation_message',
    'send_list_message',
    'send_paginated_message',
    'reply_with_loading',
    'reply_with_error',
    'reply_with_success',
    'reply_with_info'
]