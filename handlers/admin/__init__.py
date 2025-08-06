"""
Admin Module - Complete Implementation

This module provides complete admin functionality including:
- Main menu and navigation
- User management
- Order management
- Statistics and reports
- Settings management
- Language settings
- Workflow recovery
- Callback handlers
"""

from .callbacks import get_admin_callbacks_router
from .language import get_admin_language_router
from .main_menu import get_admin_main_menu_router
from .orders import get_admin_orders_router
from .settings import get_admin_settings_router
from .statistics import get_admin_statistics_router
from .users import get_admin_users_router
from .workflow_recovery import get_admin_workflow_recovery_router

def get_admin_router():
    """Get the complete admin router with all handlers"""
    from aiogram import Router
    
    router = Router()
    
    # Include all admin routers
    router.include_router(get_admin_callbacks_router())
    router.include_router(get_admin_language_router())
    router.include_router(get_admin_main_menu_router())
    router.include_router(get_admin_orders_router())
    router.include_router(get_admin_settings_router())
    router.include_router(get_admin_statistics_router())
    router.include_router(get_admin_users_router())
    router.include_router(get_admin_workflow_recovery_router())
    
    return router


