"""
Main Handlers Module - Simplified Implementation

This module sets up all role-based routers with clean integration.
All modules have been simplified to focus on core functionality.
"""

from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    """Setup all role-based handlers with proper priority"""
    try:
        # Import start handler first (highest priority)
        from handlers.start_handler import get_start_router
        start_router = get_start_router()
        dp.include_router(start_router)
        
        # Include only client router for this task
        from handlers.client import get_client_router
        client_router = get_client_router()
        dp.include_router(client_router)
        
        # Fallback unhandled
        from handlers.unhandled import get_unhandled_router
        unhandled_router = get_unhandled_router()
        dp.include_router(unhandled_router)
        
        print("✅ All handlers setup completed successfully")
        
    except Exception as e:
        print(f"❌ Error setting up handlers: {e}")
        raise

def get_global_instances():
    """Get global instances for use in handlers (simplified)"""
    return {
        'mock_data': True  # Indicate mock data usage
    }
