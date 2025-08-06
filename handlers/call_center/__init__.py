"""
Call Center Module - Simplified Implementation

This module provides core call center functionality including:
- Main menu and navigation
- Chat management
- Client management
- Direct resolution
- Feedback system
- Inbox management
- Language settings
- Order management
- Staff application creation
- Statistics and reports
- Supervisor functionality
"""

from .chat import get_call_center_chat_router
from .clients import get_call_center_clients_router
from .direct_resolution import get_call_center_direct_resolution_router
from .feedback import get_call_center_feedback_router
from .inbox import get_call_center_inbox_router
from .language import get_call_center_language_router
from .main_menu import get_call_center_main_menu_router
from .orders import get_call_center_orders_router
from .staff_application_creation import get_call_center_staff_application_creation_router
from .statistics import get_call_center_statistics_router
from .supervisor import get_call_center_supervisor_router

def get_call_center_router():
    """Get the complete call center router with all handlers"""
    from aiogram import Router
    
    router = Router()
    
    # Include all call center routers
    router.include_router(get_call_center_main_menu_router())
    router.include_router(get_call_center_language_router())
    router.include_router(get_call_center_inbox_router())
    router.include_router(get_call_center_orders_router())
    router.include_router(get_call_center_clients_router())
    router.include_router(get_call_center_chat_router())
    router.include_router(get_call_center_feedback_router())
    router.include_router(get_call_center_statistics_router())
    router.include_router(get_call_center_direct_resolution_router())
    router.include_router(get_call_center_supervisor_router())
    router.include_router(get_call_center_staff_application_creation_router())
    
    return router
