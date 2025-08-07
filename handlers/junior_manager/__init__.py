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

from .application_creation import get_junior_manager_application_creation_router
from .application_viewing import get_junior_manager_application_viewing_router
from .client_search import get_junior_manager_client_search_router
from .details_input import get_junior_manager_details_input_router

from .inbox import get_junior_manager_inbox_router
from .language import get_junior_manager_language_router
from .orders import get_junior_manager_orders_router
from .staff_application_creation import get_junior_manager_staff_application_router
from .statistics import get_junior_manager_statistics_router
from .workflow_management import get_junior_manager_workflow_router
from .ticket_creation import get_junior_manager_ticket_creation_router

def get_junior_manager_router():
    """Get the complete junior manager router with all handlers"""
    from aiogram import Router
    router = Router()
    
    # Include handlers in priority order
    router.include_router(get_junior_manager_main_menu_router())

    router.include_router(get_junior_manager_application_creation_router())
    router.include_router(get_junior_manager_application_viewing_router())
    router.include_router(get_junior_manager_client_search_router())
    router.include_router(get_junior_manager_details_input_router())

    router.include_router(get_junior_manager_inbox_router())
    router.include_router(get_junior_manager_language_router())
    router.include_router(get_junior_manager_orders_router())
    router.include_router(get_junior_manager_staff_application_router())
    router.include_router(get_junior_manager_statistics_router())
    router.include_router(get_junior_manager_workflow_router())
    router.include_router(get_junior_manager_ticket_creation_router())
    
    return router
