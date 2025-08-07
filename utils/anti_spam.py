import time
from typing import Dict, Optional
from collections import defaultdict

class AntiSpam:
    """Foydalanuvchilar spam qilishini oldini olish"""
    
    def __init__(self, cooldown_seconds: float = 2.0):
        self.cooldown_seconds = cooldown_seconds
        self.user_last_action: Dict[int, float] = defaultdict(float)
        self.user_warnings: Dict[int, int] = defaultdict(int)
        
    def check_user(self, user_id: int) -> tuple[bool, Optional[str]]:
        """
        Foydalanuvchini tekshirish
        Returns: (is_allowed, warning_message)
        """
        current_time = time.time()
        last_action = self.user_last_action[user_id]
        
        if current_time - last_action < self.cooldown_seconds:
            self.user_warnings[user_id] += 1
            remaining_time = self.cooldown_seconds - (current_time - last_action)
            
            if self.user_warnings[user_id] >= 5:
                return False, "⚠️ Siz juda ko'p harakat qilyapsiz! Iltimos, biroz kuting."
            else:
                return False, f"⏳ Iltimos, {remaining_time:.1f} soniya kuting."
        
        # Reset warnings if user is behaving
        if current_time - last_action > self.cooldown_seconds * 2:
            self.user_warnings[user_id] = 0
            
        self.user_last_action[user_id] = current_time
        return True, None

# Global instance
anti_spam = AntiSpam(cooldown_seconds=1.5)