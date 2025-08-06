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

from utils.role_system import get_role_router
from .main_menu import get_manager_main_menu_router
from .filters import get_manager_filters_router
from .language import get_manager_language_router
from .inbox import get_manager_inbox_router
from .statistics import get_manager_statistics_router
from .staff_activity import get_manager_staff_activity_router
from .status_management import get_manager_status_management_router
from .technician_assignment import get_manager_technician_assignment_router
from .word_documents import get_manager_word_documents_router
from .staff_application_creation import get_manager_staff_application_router
from .notifications import get_manager_notifications_router

manager_router = get_role_router("manager")

# Include all manager routers
manager_router.include_router(get_manager_main_menu_router())
manager_router.include_router(get_manager_filters_router())
manager_router.include_router(get_manager_language_router())
manager_router.include_router(get_manager_inbox_router())
manager_router.include_router(get_manager_statistics_router())
manager_router.include_router(get_manager_staff_activity_router())
manager_router.include_router(get_manager_status_management_router())
manager_router.include_router(get_manager_technician_assignment_router())
manager_router.include_router(get_manager_word_documents_router())
manager_router.include_router(get_manager_staff_application_router())
manager_router.include_router(get_manager_notifications_router())

def get_manager_router():
    """Get the complete manager router with all handlers"""
    return manager_router
