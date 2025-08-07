from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Union
import logging
from utils.anti_spam import anti_spam

logger = logging.getLogger(__name__)

class AntiSpamMiddleware(BaseMiddleware):
    """Anti-spam middleware"""
    
    async def __call__(
        self,
        handler: Callable,
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        try:
            user = event.from_user
            if not user:
                return await handler(event, data)
            
            # Anti-spam tekshirish
            is_allowed, warning_message = anti_spam.check_user(user.id)
            
            if not is_allowed:
                # Foydalanuvchiga ogohlantirish
                if isinstance(event, CallbackQuery):
                    await event.answer(warning_message, show_alert=True)
                elif isinstance(event, Message):
                    # Xabar yubormaslik, faqat callback'da ogohlantirish
                    pass
                
                # Handler'ni chaqirmaslik
                return None
            
            # Handler'ni chaqirish
            return await handler(event, data)
            
        except Exception as e:
            logger.error(f"Anti-spam middleware error: {e}")
            # Xatolik bo'lsa ham handler'ni chaqirish
            return await handler(event, data)