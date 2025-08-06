"""
Junior Manager Module - Simplified Implementation

This module provides core junior manager functionality including:
- Main menu and navigation
- Language settings
- Order management
- Statistics and reports
- Inbox viewing
- Application management
- Staff application creation
- Workflow management
- Client search
- Application creation and viewing
- Details input
"""

from aiogram import Router
from .main_menu import get_junior_manager_main_menu_router
from .language import get_junior_manager_language_router
from .orders import get_junior_manager_orders_router
from .statistics import get_junior_manager_statistics_router
from .inbox_viewing import get_junior_manager_inbox_viewing_router
from .applications import get_applications_router
from .staff_application_creation import get_junior_manager_staff_application_router
from .workflow_management import get_junior_manager_workflow_router
from .client_search import get_junior_manager_client_search_router
from .application_creation import get_junior_manager_application_creation_router
from .application_viewing import get_junior_manager_application_viewing_router
from .details_input import get_junior_manager_details_input_router

def get_junior_manager_router():
    """Get the complete junior manager router with all handlers"""
    router = Router()
    
    router.include_router(get_junior_manager_main_menu_router())
    router.include_router(get_junior_manager_language_router())
    router.include_router(get_junior_manager_orders_router())
    router.include_router(get_junior_manager_statistics_router())
    router.include_router(get_junior_manager_inbox_viewing_router())
    router.include_router(get_applications_router())
    router.include_router(get_junior_manager_staff_application_router())
    router.include_router(get_junior_manager_workflow_router())
    router.include_router(get_junior_manager_client_search_router())
    router.include_router(get_junior_manager_application_creation_router())
    router.include_router(get_junior_manager_application_viewing_router())
    router.include_router(get_junior_manager_details_input_router())
    
    return router
