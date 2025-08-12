"""
Call Center Module - Complete Implementation

This module provides call center functionality including:
- Chat management
- Client interactions
- Client rating and feedback
- Direct problem resolution
- Feedback collection
- Inbox management
- Language settings
- Main menu and dashboard
- Order management
- Staff application creation
- Statistics and reports
- Supervisor functions
"""

from aiogram import Router
from .main_menu import get_call_center_main_menu_router
from .inbox import get_call_center_inbox_router
from .language import get_call_center_language_router
from .orders import get_call_center_orders_router
from .statistics import get_call_center_statistics_router
from .connection_order_cc import get_call_center_connection_order_router
from .technician_order_cc import get_call_center_technical_service_router

def get_call_center_router():
    """Get the complete call center router with all handlers"""
    from aiogram import Router
    router = Router()
    
    # Include handlers in priority order
    router.include_router(get_call_center_main_menu_router())
    router.include_router(get_call_center_inbox_router())
    router.include_router(get_call_center_language_router())
    router.include_router(get_call_center_orders_router())
    router.include_router(get_call_center_connection_order_router())
    router.include_router(get_call_center_technical_service_router())
    router.include_router(get_call_center_statistics_router())
    
    return router
