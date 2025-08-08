"""
Client Module - Simplified Implementation

This module provides core client functionality including:
- Start and registration
- Contact management
- Feedback system
- Help and support
- Language settings
- Main menu and navigation
- Connection orders
- Service orders
- Profile management
- Order utilities
"""

from aiogram import Router
from .contact import get_client_contact_router
# from .feedback import get_client_feedback_router
from .help import get_client_help_router
from .language import get_client_language_router
from .main_menu import get_client_main_menu_router
from .connection_order import get_connection_order_router
from .service_order import get_service_order_router
from .profile import get_client_profile_router
from .orders import get_orders_router

def get_client_router():
    """Get the complete client router with all handlers"""
    from aiogram import Router
    router = Router()
    
    # Include handlers in priority order
    router.include_router(get_client_main_menu_router())  
    router.include_router(get_connection_order_router())
    router.include_router(get_service_order_router())
    router.include_router(get_orders_router())
    router.include_router(get_client_profile_router())
    router.include_router(get_client_contact_router())
    router.include_router(get_client_help_router())
    router.include_router(get_client_language_router())
    # router.include_router(get_client_feedback_router())
    
    return router

