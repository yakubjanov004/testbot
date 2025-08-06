"""
Controller Reply Examples

Bu fayl controller uchun yangi reply utility'larini qanday ishlatishni ko'rsatadi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.reply_utils import (
    send_or_edit_message,
    answer_callback_query,
    reply_with_error,
    reply_with_success,
    reply_with_info,
    handle_inline_response,
    clear_message_state,
    send_confirmation_message,
    send_list_message,
    send_paginated_message,
    reply_with_loading
)

def get_example_controller_router():
    """Example controller router with all reply patterns"""
    router = Router()
    
    # 1. Basic message reply
    @router.message(F.text == "Test Reply")
    async def test_basic_reply(message: Message, state: FSMContext):
        """Basic message reply example"""
        try:
            await send_or_edit_message(
                message,
                "✅ Bu oddiy reply misoli",
                state,
                parse_mode='HTML'
            )
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik: {e}")
    
    # 2. Callback query with inline response
    @router.callback_query(F.data == "test_callback")
    async def test_callback_reply(callback: CallbackQuery, state: FSMContext):
        """Callback query reply example"""
        try:
            # Answer the callback query
            await answer_callback_query(callback, "Tugma bosildi!")
            
            # Send or edit message
            await send_or_edit_message(
                callback,
                "✅ Callback query reply misoli",
                state,
                parse_mode='HTML'
            )
        except Exception as e:
            await reply_with_error(callback, state, f"Xatolik: {e}")
    
    # 3. Error handling
    @router.message(F.text == "Test Error")
    async def test_error_handling(message: Message, state: FSMContext):
        """Error handling example"""
        try:
            # Simulate an error
            raise Exception("Test xatolik")
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik yuz berdi: {e}")
    
    # 4. Success message
    @router.message(F.text == "Test Success")
    async def test_success_message(message: Message, state: FSMContext):
        """Success message example"""
        try:
            await reply_with_success(message, state, "Muvaffaqiyatli bajarildi!")
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik: {e}")
    
    # 5. Info message
    @router.message(F.text == "Test Info")
    async def test_info_message(message: Message, state: FSMContext):
        """Info message example"""
        try:
            await reply_with_info(
                message, 
                state, 
                "ℹ️ Bu ma'lumot xabari"
            )
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik: {e}")
    
    # 6. Loading message
    @router.message(F.text == "Test Loading")
    async def test_loading_message(message: Message, state: FSMContext):
        """Loading message example"""
        try:
            # Show loading
            await reply_with_loading(message, state, "⏳ Yuklanmoqda...")
            
            # Simulate some work
            import asyncio
            await asyncio.sleep(2)
            
            # Update with result
            await send_or_edit_message(
                message,
                "✅ Yuklash tugadi!",
                state,
                parse_mode='HTML'
            )
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik: {e}")
    
    # 7. Confirmation message
    @router.message(F.text == "Test Confirmation")
    async def test_confirmation_message(message: Message, state: FSMContext):
        """Confirmation message example"""
        try:
            await send_confirmation_message(
                message,
                state,
                "❓ Bu amalni bajarishni xohlaysizmi?",
                "confirm_action",
                "cancel_action"
            )
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik: {e}")
    
    # 8. List message
    @router.message(F.text == "Test List")
    async def test_list_message(message: Message, state: FSMContext):
        """List message example"""
        try:
            items = [
                "Birinchilik",
                "Ikkinchilik", 
                "Uchinchilik"
            ]
            
            def format_item(item, index):
                return f"{index}. {item}\n"
            
            await send_list_message(
                message,
                state,
                "📋 Ro'yxat misoli",
                items,
                item_formatter=format_item
            )
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik: {e}")
    
    # 9. Paginated message
    @router.message(F.text == "Test Pagination")
    async def test_paginated_message(message: Message, state: FSMContext):
        """Paginated message example"""
        try:
            items = [f"Element {i}" for i in range(1, 26)]
            
            def format_item(item, index):
                return f"{index}. {item}\n"
            
            await send_paginated_message(
                message,
                state,
                "📄 Sahifali ro'yxat",
                items,
                page=1,
                items_per_page=5,
                item_formatter=format_item,
                navigation_callback_prefix="test_page"
            )
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik: {e}")
    
    # 10. Inline response for callback
    @router.callback_query(F.data == "test_inline")
    async def test_inline_response(callback: CallbackQuery, state: FSMContext):
        """Inline response example"""
        try:
            await handle_inline_response(
                callback,
                state,
                "Bu inline response!",
                show_alert=True
            )
        except Exception as e:
            await reply_with_error(callback, state, f"Xatolik: {e}")
    
    # 11. Clear message state
    @router.message(F.text == "Test Clear")
    async def test_clear_state(message: Message, state: FSMContext):
        """Clear state example"""
        try:
            await clear_message_state(state)
            await reply_with_success(message, state, "State tozalandi!")
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik: {e}")
    
    # 12. Complex workflow example
    @router.message(F.text == "Test Workflow")
    async def test_complex_workflow(message: Message, state: FSMContext):
        """Complex workflow example"""
        try:
            # Step 1: Show loading
            await reply_with_loading(message, state, "⏳ Jarayon boshlanmoqda...")
            
            # Step 2: Simulate work
            import asyncio
            await asyncio.sleep(1)
            
            # Step 3: Update with progress
            await send_or_edit_message(
                message,
                "📊 Jarayon 50% tugadi...",
                state,
                parse_mode='HTML'
            )
            
            # Step 4: More work
            await asyncio.sleep(1)
            
            # Step 5: Final result
            await send_or_edit_message(
                message,
                "✅ Jarayon muvaffaqiyatli tugadi!",
                state,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await reply_with_error(message, state, f"Xatolik: {e}")
    
    return router


# Usage examples for different scenarios:

"""
1. ODDIY XABAR YUBORISH:
await send_or_edit_message(message, "Xabar matni", state)

2. XATOLIK XABARI:
await reply_with_error(message, state, "Xatolik matni")

3. MUVAFFAQIYAT XABARI:
await reply_with_success(message, state, "Muvaffaqiyat matni")

4. CALLBACK QUERY JAVOBI:
await answer_callback_query(callback, "Javob matni")

5. INLINE RESPONSE:
await handle_inline_response(callback, state, "Response matni")

6. TASDIQLASH XABARI:
await send_confirmation_message(
    message, 
    state, 
    "Tasdiqlash matni",
    "confirm_callback",
    "cancel_callback"
)

7. RO'YXAT XABARI:
await send_list_message(
    message,
    state,
    "Ro'yxat sarlavhasi",
    items_list,
    item_formatter=format_function
)

8. SAHIFALI XABAR:
await send_paginated_message(
    message,
    state,
    "Sahifa sarlavhasi",
    items_list,
    page=1,
    items_per_page=10
)

9. YUKLASH XABARI:
await reply_with_loading(message, state, "Yuklanmoqda...")

10. STATE TOZALASH:
await clear_message_state(state)
"""