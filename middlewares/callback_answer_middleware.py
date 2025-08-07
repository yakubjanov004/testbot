from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from typing import Callable, Dict, Any
import logging
import asyncio

logger = logging.getLogger(__name__)

class CallbackAnswerMiddleware(BaseMiddleware):
    """Callback query'larga avtomatik javob berish middleware'i"""
    
    def __init__(self, auto_answer_delay: float = 0.1):
        """
        :param auto_answer_delay: Callback'ga avtomatik javob berish uchun kutish vaqti (soniyalarda)
        """
        self.auto_answer_delay = auto_answer_delay
    
    async def __call__(
        self,
        handler: Callable,
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Faqat CallbackQuery uchun ishlaydi
        if not isinstance(event, CallbackQuery):
            return await handler(event, data)
        
        # Callback answered flag
        callback_answered = False
        
        async def auto_answer():
            """Avtomatik javob berish funksiyasi"""
            await asyncio.sleep(self.auto_answer_delay)
            if not callback_answered:
                try:
                    await event.answer()
                    logger.debug(f"Auto-answered callback from user {event.from_user.id}")
                except Exception as e:
                    logger.error(f"Failed to auto-answer callback: {e}")
        
        # Avtomatik javob berish task'ini boshlash
        auto_answer_task = asyncio.create_task(auto_answer())
        
        try:
            # Original answer metodini wrap qilish
            original_answer = event.answer
            
            async def wrapped_answer(*args, **kwargs):
                nonlocal callback_answered
                callback_answered = True
                auto_answer_task.cancel()
                return await original_answer(*args, **kwargs)
            
            event.answer = wrapped_answer
            
            # Handler'ni chaqirish
            result = await handler(event, data)
            
            # Agar handler tugagandan keyin ham javob berilmagan bo'lsa
            if not callback_answered:
                callback_answered = True
                auto_answer_task.cancel()
                try:
                    await event.answer()
                except Exception as e:
                    logger.error(f"Failed to answer callback after handler: {e}")
            
            return result
            
        except Exception as e:
            # Xatolik bo'lsa ham callback'ga javob berish
            if not callback_answered:
                try:
                    await event.answer("❌ Xatolik yuz berdi", show_alert=True)
                except:
                    pass
            raise
        finally:
            # Task'ni bekor qilish
            if not auto_answer_task.done():
                auto_answer_task.cancel()