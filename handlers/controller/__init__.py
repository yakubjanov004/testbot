from aiogram import Router
from .main_menu import get_controller_main_menu_router
from .orders import get_controller_orders_router
from .quality import get_controller_quality_router
from .reports import get_controller_reports_router
from .technician import get_controller_technician_router
from .technicians import get_controller_technicians_router
from .language import get_controller_language_router
from .inbox import get_controller_inbox_router
from .technical_service import get_controller_technical_service_router
from .staff_application_creation import get_controller_staff_application_router
from .application_creator import get_controller_application_creator_router
from .monitoring import get_controller_monitoring_router
from .realtime_monitoring import get_controller_realtime_monitoring_router

def get_controller_router():
    """Get the complete controller router with all handlers"""
    router = Router()
    
    # Include all controller routers
    router.include_router(get_controller_main_menu_router())
    router.include_router(get_controller_orders_router())
    router.include_router(get_controller_quality_router())
    router.include_router(get_controller_reports_router())
    router.include_router(get_controller_technician_router())
    router.include_router(get_controller_technicians_router())
    router.include_router(get_controller_language_router())
    router.include_router(get_controller_inbox_router())
    router.include_router(get_controller_technical_service_router())
    router.include_router(get_controller_staff_application_router())
    router.include_router(get_controller_application_creator_router())
    router.include_router(get_controller_monitoring_router())
    router.include_router(get_controller_realtime_monitoring_router())
    
    return router

__all__ = ['get_controller_router']
