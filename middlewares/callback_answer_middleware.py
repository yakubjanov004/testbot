"""
Callback Answer Middleware

Bu middleware barcha callback query'larni avtomatik javob beradi.
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery


class CallbackAnswerMiddleware(BaseMiddleware):
    """
    Middleware to automatically answer all callback queries.
    This ensures that all inline and reply buttons provide feedback when clicked.
    """
    
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """
        Process callback query and automatically answer it.
        
        Args:
            handler: The handler function
            event: The callback query event
            data: Additional data
            
        Returns:
            Handler result
        """
        try:
            # Automatically answer the callback query to remove loading state
            # This prevents the "clock" icon from appearing on the button
            if not event.answered:
                await event.answer()
        except Exception as e:
            # Log error but don't stop processing
            print(f"Error answering callback query: {e}")
        
        # Continue processing with the handler
        return await handler(event, data)