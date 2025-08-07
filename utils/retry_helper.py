import asyncio
import logging
from typing import Any, Callable, Optional
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest

logger = logging.getLogger(__name__)

class RetryHelper:
    """Telegram API xatolari uchun retry mexanizmi"""
    
    @staticmethod
    async def retry_on_flood(
        func: Callable,
        *args,
        max_retries: int = 3,
        initial_delay: float = 0.5,
        **kwargs
    ) -> Optional[Any]:
        """
        Flood control xatolari uchun avtomatik qayta urinish
        
        :param func: Chaqiriladigan funksiya
        :param max_retries: Maksimal urinishlar soni
        :param initial_delay: Boshlang'ich kutish vaqti
        :return: Funksiya natijasi yoki None
        """
        delay = initial_delay
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Funksiyani chaqirish
                result = await func(*args, **kwargs)
                
                # Muvaffaqiyatli bo'lsa, natijani qaytarish
                if attempt > 0:
                    logger.info(f"Retry successful after {attempt} attempts")
                
                return result
                
            except TelegramRetryAfter as e:
                # Telegram o'zi qancha kutishni aytsa
                wait_time = e.retry_after
                logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                last_error = e
                
            except TelegramBadRequest as e:
                # Bad request xatolari (masalan, xabar o'chirilgan)
                if "message to reply not found" in str(e):
                    logger.error("Original message not found, cannot reply")
                    return None
                elif "message is not modified" in str(e):
                    logger.warning("Message content unchanged, skipping")
                    return None
                else:
                    logger.error(f"Bad request error: {e}")
                    last_error = e
                    break
                    
            except Exception as e:
                # Boshqa xatoliklar
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                last_error = e
                
                if attempt < max_retries - 1:
                    # Exponential backoff
                    await asyncio.sleep(delay)
                    delay *= 2  # Har safar 2 baravar ko'paytirish
                else:
                    break
        
        # Barcha urinishlar muvaffaqiyatsiz
        logger.error(f"All {max_retries} retry attempts failed. Last error: {last_error}")
        return None

# Global instance
retry_helper = RetryHelper()