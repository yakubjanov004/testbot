import asyncio
import time
from typing import Dict, Optional
from collections import defaultdict

class RateLimiter:
    """Telegram Bot API uchun rate limiter"""
    
    def __init__(self):
        # Har bir chat uchun oxirgi xabar vaqti
        self.last_message_time: Dict[int, float] = defaultdict(float)
        # Har bir chat uchun xabarlar soni (daqiqada)
        self.message_count: Dict[int, list] = defaultdict(list)
        # Global xabarlar soni (soniyada)
        self.global_messages: list = []
        
    async def check_and_wait(self, chat_id: int, is_group: bool = False) -> None:
        """Rate limit tekshirish va kutish"""
        current_time = time.time()
        
        # 1. Global limit - 30 xabar/soniya
        self.global_messages = [t for t in self.global_messages if current_time - t < 1]
        if len(self.global_messages) >= 30:
            wait_time = 1 - (current_time - self.global_messages[0])
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        # 2. Per-chat limit - 1 xabar/soniya
        last_time = self.last_message_time.get(chat_id, 0)
        time_diff = current_time - last_time
        if time_diff < 1:
            await asyncio.sleep(1 - time_diff)
        
        # 3. Guruhlar uchun - 20 xabar/daqiqa
        if is_group:
            self.message_count[chat_id] = [
                t for t in self.message_count[chat_id] 
                if current_time - t < 60
            ]
            if len(self.message_count[chat_id]) >= 20:
                wait_time = 60 - (current_time - self.message_count[chat_id][0])
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
        
        # Vaqtlarni yangilash
        current_time = time.time()
        self.last_message_time[chat_id] = current_time
        self.global_messages.append(current_time)
        if is_group:
            self.message_count[chat_id].append(current_time)

# Global instance
rate_limiter = RateLimiter()