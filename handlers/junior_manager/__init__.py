"""
Junior Manager Module - Complete Implementation

This module provides junior manager functionality including:
- Application creation and management
- Application viewing and tracking
- Client search functionality
- Details input and processing
- Inbox management and viewing
- Language settings
- Main menu and dashboard
- Order management
- Staff application creation
- Statistics and analytics
- Workflow management
"""

from aiogram import Router
from .main_menu import get_junior_manager_main_menu_router
from .application_viewing import get_junior_manager_application_viewing_router
from .connection_order import get_junior_manager_connection_order_router

def get_junior_manager_router():
    """Get the complete junior manager router with consolidated handlers"""
    router = Router()
    
    # Include essential handlers only
    router.include_router(get_junior_manager_main_menu_router())
    router.include_router(get_junior_manager_application_viewing_router())
    router.include_router(get_junior_manager_connection_order_router())
    
    return router
