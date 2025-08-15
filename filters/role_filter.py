from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from utils.role_system import get_cached_role
from loader import get_user_role
from utils.role_system import cache_role
import logging
import time
from typing import Dict

logger = logging.getLogger(__name__)

class RoleFilter(BaseFilter):
    def __init__(self, role: str):
        self.role = role
        self._failure_cache: Dict[int, float] = {}
        self._cache_duration = 300  # 5 minutes
        self._last_check_cache: Dict[int, float] = {}
        self._check_interval = 0.5  # 0.5 seconds between checks for same user

    def _should_log_failure(self, user_id: int) -> bool:
        """Only log failed access once per cache duration to reduce spam"""
        current_time = time.time()
        cache_key = f"{user_id}_{self.role}_fail"
        
        if cache_key in self._failure_cache:
            if current_time - self._failure_cache[cache_key] < self._cache_duration:
                return False
        
        self._failure_cache[cache_key] = current_time
        return True

    def _should_log_success(self, user_id: int) -> bool:
        """Only log successful access occasionally to reduce spam"""
        current_time = time.time()
        cache_key = f"{user_id}_{self.role}_success"
        
        if cache_key in self._failure_cache:  # Reuse failure cache for success
            if current_time - self._failure_cache[cache_key] < self._cache_duration:
                return False
        
        self._failure_cache[cache_key] = current_time
        return True

    def _should_check_role(self, user_id: int) -> bool:
        """Check if we should perform role check to reduce redundant checks"""
        current_time = time.time()
        
        if user_id in self._last_check_cache:
            if current_time - self._last_check_cache[user_id] < self._check_interval:
                return False
        
        self._last_check_cache[user_id] = current_time
        return True

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        try:
            user_id = event.from_user.id
            
            # Check global cache first to reduce database queries
            cached_role = get_cached_role(user_id)
            if cached_role is not None:
                result = cached_role == self.role
                # Only log successful access, not failures to reduce spam
                if result and self._should_log_success(user_id):
                    logger.debug(f"Access granted for user {user_id}. Role: {self.role}")
                return result
            
            # Reduce redundant checks for same user
            if not self._should_check_role(user_id):
                # Return cached result for this user
                return False
            
            # Get role from database if not cached
            user_role = await get_user_role(user_id)
            if user_role:
                cache_role(user_id, user_role)
            
            result = user_role == self.role
            
            # Only log successful access, not failures
            if result and self._should_log_success(user_id):
                logger.debug(f"Access granted for user {user_id}. Role: {self.role}")
            
            return result
        except Exception as e:
            logger.error(f"Error in RoleFilter: {str(e)}")
            return False 