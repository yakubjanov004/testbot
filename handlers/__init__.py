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
        
        # Import only available role routers
        try:
            from handlers.manager import get_manager_router
            manager_router = get_manager_router()
            dp.include_router(manager_router)
            print("✅ Manager router loaded")
        except Exception as e:
            print(f"⚠️ Manager router not loaded: {e}")
        
        try:
            from handlers.client import get_client_router
            client_router = get_client_router()
            dp.include_router(client_router)
            print("✅ Client router loaded")
        except Exception as e:
            print(f"⚠️ Client router not loaded: {e}")
        
        print("✅ Basic handlers setup completed successfully")
        
    except Exception as e:
        print(f"❌ Error setting up handlers: {e}")
        raise

def get_global_instances():
    """Get global instances for use in handlers"""
    from loader import USE_DATABASE
    
    if USE_DATABASE:
        from utils.database import (
            get_user, create_user, update_user, create_order, 
            get_orders, update_order_status, get_inventory,
            update_inventory_quantity, add_feedback, log_activity, get_statistics
        )
        return {
            'database_enabled': True,
            'get_user': get_user,
            'create_user': create_user,
            'update_user': update_user,
            'create_order': create_order,
            'get_orders': get_orders,
            'update_order_status': update_order_status,
            'get_inventory': get_inventory,
            'update_inventory_quantity': update_inventory_quantity,
            'add_feedback': add_feedback,
            'log_activity': log_activity,
            'get_statistics': get_statistics
        }
    else:
        from utils.mock_user_store import (
            get_user, upsert_user, all_users
        )
        return {
            'database_enabled': False,
            'get_user': get_user,
            'upsert_user': upsert_user,
            'all_users': all_users
        }
