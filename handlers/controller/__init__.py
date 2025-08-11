"""
Controller Module - Complete Implementation

This module provides controller functionality including:
- Application creation and management
- Inbox management
- Language settings
- Main menu and dashboard
- Monitoring and real-time tracking
- Order management
- Quality control
- Reports and analytics
- Staff application creation
- Technical service management
- Technician management
- Workflow management
"""

from aiogram import Router
from .main_menu import get_controller_main_menu_router
from .application_creator import get_controller_application_creator_router
from .inbox import get_controller_inbox_router
from .language import get_controller_language_router
from .monitoring import get_controller_monitoring_router
from .orders import get_controller_orders_router
from .quality import get_controller_quality_router
from .realtime_monitoring import get_realtime_monitoring_router
from .reports import get_controller_reports_router
from .staff_application_creation import get_controller_staff_application_router
from .technical_service import get_controller_technical_service_router
from .technician import get_controller_technician_management_router
from .technicians import get_controller_technicians_router
from .workflow_manager import get_workflow_manager_router
from .export import get_controller_export_router

def get_controller_router():
    """Get the complete controller router with all handlers"""
    from aiogram import Router
    router = Router()
    
    # Include handlers in priority order
    router.include_router(get_controller_main_menu_router())
    router.include_router(get_controller_application_creator_router())  # 🔌/🔧 yaratish
    router.include_router(get_controller_inbox_router())  # 📥 Inbox
    router.include_router(get_controller_language_router())  # 🌐 Til
    router.include_router(get_controller_monitoring_router())  # 📊 Monitoring
    router.include_router(get_realtime_monitoring_router())  # 🕐 Real vaqtda
    from .applications_list import get_controller_applications_list_router
    router.include_router(get_controller_applications_list_router())  # 📋 Arizalarni ko'rish
    from .staff_activity import get_controller_staff_activity_router
    router.include_router(get_controller_staff_activity_router())  # 👥 Xodimlar faoliyati (technicians only)
    router.include_router(get_controller_export_router())  # 📤 Export
    
    return router

__all__ = ['get_controller_router']
