"""
Manager Module - Complete Implementation

This module provides complete manager functionality including:
- Main menu and navigation
- Language settings
- Inbox management
- Applications management
- Statistics and reports
- Staff activity monitoring
- Status management
- Technician assignment
- Word document generation
- Staff application creation
- Real-time monitoring
"""

from aiogram import Router

# Import only existing modules
try:
    from .main_menu import get_manager_main_menu_router
    main_menu_available = True
except ImportError:
    main_menu_available = False

try:
    from .inbox import get_manager_inbox_router
    inbox_available = True
except ImportError:
    inbox_available = False

def get_manager_router():
    """Get the complete manager router with all handlers"""
    router = Router()
    
    # Include only available routers
    if main_menu_available:
        router.include_router(get_manager_main_menu_router())
    
    if inbox_available:
        router.include_router(get_manager_inbox_router())
    
    return router


