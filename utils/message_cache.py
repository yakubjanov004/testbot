import hashlib
import time
from typing import Dict, Optional
from collections import defaultdict

class MessageCache:
    """Xabarlarni keshlash va takrorlanishini oldini olish"""
    
    def __init__(self, ttl_seconds: float = 5.0):
        """
        :param ttl_seconds: Kesh yashash vaqti (soniyalarda)
        """
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, float] = {}
        self.user_last_message: Dict[int, str] = {}
        
    def _generate_hash(self, user_id: int, text: str, chat_id: int) -> str:
        """Xabar uchun unique hash generatsiya qilish"""
        content = f"{user_id}:{chat_id}:{text}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _clean_expired(self):
        """Eskirgan kesh elementlarini tozalash"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.cache.items()
            if current_time - timestamp > self.ttl_seconds
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def is_duplicate(self, user_id: int, text: str, chat_id: int) -> bool:
        """Xabar takroriy ekanligini tekshirish"""
        self._clean_expired()
        
        message_hash = self._generate_hash(user_id, text, chat_id)
        current_time = time.time()
        
        # Agar xuddi shu xabar yaqinda yuborilgan bo'lsa
        if message_hash in self.cache:
            time_diff = current_time - self.cache[message_hash]
            if time_diff < self.ttl_seconds:
                return True
        
        # Keshga qo'shish
        self.cache[message_hash] = current_time
        self.user_last_message[user_id] = message_hash
        
        return False
    
    def get_last_message_age(self, user_id: int) -> Optional[float]:
        """Foydalanuvchining oxirgi xabari qancha vaqt oldin yuborilganini olish"""
        if user_id not in self.user_last_message:
            return None
            
        message_hash = self.user_last_message[user_id]
        if message_hash not in self.cache:
            return None
            
        return time.time() - self.cache[message_hash]

# Global instance
message_cache = MessageCache(ttl_seconds=3.0)