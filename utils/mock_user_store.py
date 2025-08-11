<<'PATCH'
*** Begin Patch
*** Add File: utils/mock_user_store.py
+"""
+Mock User Store
+
+In-memory user registry for development without a real database.
+Thread-safe with asyncio.Lock for concurrent access.
+"""
+
+from __future__ import annotations
+
+import asyncio
+from datetime import datetime
+from typing import Dict, Any, Optional, Tuple
+import logging
+
+
+logger = logging.getLogger(__name__)
+
+_users: Dict[int, Dict[str, Any]] = {}
+_lock = asyncio.Lock()
+
+
+def _now_iso() -> str:
+    return datetime.now().isoformat(timespec="seconds")
+
+
+async def upsert_user(user_id: int, user_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
+    """
+    Create or update a user record.
+
+    Returns (is_created, saved_record)
+    """
+    async with _lock:
+        is_created = user_id not in _users
+        if is_created:
+            user_data.setdefault("created_at", _now_iso())
+            user_data.setdefault("tags", [])
+            user_data.setdefault("notes", "")
+            _users[user_id] = user_data.copy()
+            logger.info(f"Mock user created: {user_id}")
+        else:
+            # Preserve immutable fields
+            existing = _users[user_id]
+            preserved = {"created_at": existing.get("created_at"), "tags": existing.get("tags", []), "notes": existing.get("notes", "")}
+            existing.update(user_data)
+            existing.update(preserved)
+            _users[user_id] = existing
+            logger.info(f"Mock user updated: {user_id}")
+
+        return is_created, _users[user_id].copy()
+
+
+async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
+    async with _lock:
+        user = _users.get(user_id)
+        return user.copy() if user else None
+
+
+async def all_users() -> Dict[int, Dict[str, Any]]:
+    async with _lock:
+        # Return a shallow copy to avoid accidental mutations outside
+        return {uid: data.copy() for uid, data in _users.items()}
+
+
+async def clear_users() -> None:
+    async with _lock:
+        _users.clear()
+        logger.warning("Mock user store cleared")
+
*** End Patch
PATCH