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
from .main_menu import router as main_menu_router
from .inbox_handler import router as inbox_router
from .view_applications import router as view_applications_router
from .create_connection import router as create_connection_router
from .create_technical import router as create_technical_router
from .realtime_monitoring_handler import router as realtime_monitoring_router
from .monitoring_handler import router as monitoring_router
from .staff_activity_handler import router as staff_activity_router
from .export_handler import router as export_router
from .language_handler import router as language_router

# Eski handlerlar (callback va boshqa funksiyalar uchun)
from .inbox import router as inbox_callbacks_router
from .export import router as export_callbacks_router
from .realtime_monitoring import router as realtime_callbacks_router
from .monitoring import router as monitoring_callbacks_router
from .language import router as language_callbacks_router
from .staff_application_creation import router as staff_app_router
from .application_creator import router as app_creator_router
from .technician import router as technician_router

def get_controller_router():
    """Controller uchun barcha routerlarni birlashtirib qaytaradi"""
    router = Router()
    
    # Asosiy reply handlerlar
    router.include_router(main_menu_router)
    router.include_router(inbox_router)
    router.include_router(view_applications_router)
    router.include_router(create_connection_router)
    router.include_router(create_technical_router)
    router.include_router(realtime_monitoring_router)
    router.include_router(monitoring_router)
    router.include_router(staff_activity_router)
    router.include_router(export_router)
    router.include_router(language_router)
    
    # Callback va boshqa handlerlar
    router.include_router(inbox_callbacks_router)
    router.include_router(export_callbacks_router)
    router.include_router(realtime_callbacks_router)
    router.include_router(monitoring_callbacks_router)
    router.include_router(language_callbacks_router)
    router.include_router(staff_app_router)
    router.include_router(app_creator_router)
    router.include_router(technician_router)
    
    return router

__all__ = ['get_controller_router']
