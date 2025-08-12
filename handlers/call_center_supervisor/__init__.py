"""
Call Center Supervisor Module - Complete Implementation

This module provides call center supervisor functionality including:
- Application management
- Feedback system
- Inbox management
- Language settings
- Main menu and dashboard
- Notification management
- Order management
- Staff application creation
- Statistics and reports
- Workflow management
"""

from aiogram import Router
from .main_menu import get_call_center_supervisor_main_menu_router
from .inbox import get_call_center_supervisor_inbox_router
from .language import get_call_center_supervisor_language_router
from .orders import get_call_center_supervisor_orders_router
from .connection_order_ccs import get_call_center_supervisor_staff_application_creation_router
from .statistics import get_call_center_supervisor_statistics_router
from .staff_activity import get_call_center_supervisor_staff_activity_router
from .technicial_order_ccs import get_call_center_supervisor_technical_order_router
from .export import get_call_center_supervisor_export_router

def get_call_center_supervisor_router():
    """Get the complete call center supervisor router with all handlers"""
    from aiogram import Router
    router = Router()
    
    router.include_router(get_call_center_supervisor_main_menu_router())
    router.include_router(get_call_center_supervisor_inbox_router())
    router.include_router(get_call_center_supervisor_language_router())
    router.include_router(get_call_center_supervisor_orders_router())
    router.include_router(get_call_center_supervisor_staff_application_creation_router())
    router.include_router(get_call_center_supervisor_staff_activity_router())
    router.include_router(get_call_center_supervisor_technical_order_router())
    router.include_router(get_call_center_supervisor_statistics_router())
    router.include_router(get_call_center_supervisor_export_router())
    
    return router 
