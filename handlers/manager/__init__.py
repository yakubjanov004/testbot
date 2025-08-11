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

from aiogram import Router
from .main_menu import router as main_menu_router
from .inbox_handler import router as inbox_router
from .view_applications import router as view_applications_router
from .create_connection import router as create_connection_router
from .create_technical import router as create_technical_router
from .realtime_monitoring_handler import router as realtime_monitoring_router
from .monitoring_handler import router as monitoring_router
from .staff_activity_handler import router as staff_activity_router
from .status_change_handler import router as status_change_router
from .export_handler import router as export_router
from .language_handler import router as language_router

# Eski handlerlar (callback va boshqa funksiyalar uchun)
from .inbox import router as inbox_callbacks_router
from .export import router as export_callbacks_router
from .realtime_monitoring import router as realtime_callbacks_router
from .reports import router as reports_callbacks_router
from .staff_activity import router as staff_activity_callbacks_router
from .status_management import router as status_callbacks_router
from .language import router as language_callbacks_router
from .staff_application_creation import router as staff_app_router
from .applications_actions import router as app_actions_router
from .applications_callbacks import router as app_callbacks_router

def get_manager_router():
    """Manager uchun barcha routerlarni birlashtirib qaytaradi"""
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
    router.include_router(status_change_router)
    router.include_router(export_router)
    router.include_router(language_router)
    
    # Callback va boshqa handlerlar
    router.include_router(inbox_callbacks_router)
    router.include_router(export_callbacks_router)
    router.include_router(realtime_callbacks_router)
    router.include_router(reports_callbacks_router)
    router.include_router(staff_activity_callbacks_router)
    router.include_router(status_callbacks_router)
    router.include_router(language_callbacks_router)
    router.include_router(staff_app_router)
    router.include_router(app_actions_router)
    router.include_router(app_callbacks_router)
    
    return router


