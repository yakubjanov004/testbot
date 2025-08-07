from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Union
import logging
from utils.rate_limiter import rate_limiter

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseMiddleware):
    """Rate limiting middleware"""
    
    async def __call__(
        self,
        handler: Callable,
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        try:
            # Chat ID ni olish
            if isinstance(event, Message):
                chat_id = event.chat.id
                is_group = event.chat.type in ['group', 'supergroup']
            elif isinstance(event, CallbackQuery) and event.message:
                chat_id = event.message.chat.id
                is_group = event.message.chat.type in ['group', 'supergroup']
            else:
                # Agar chat_id topilmasa, to'g'ridan-to'g'ri handler'ga o'tkazish
                return await handler(event, data)
            
            # Rate limit tekshirish
            await rate_limiter.check_and_wait(chat_id, is_group)
            
            # Handler'ni chaqirish
            return await handler(event, data)
            
        except Exception as e:
            logger.error(f"Rate limit middleware error: {e}")
            # Xatolik bo'lsa ham handler'ni chaqirish
            return await handler(event, data)