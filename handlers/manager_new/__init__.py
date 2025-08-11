from .main_menu import router as main_menu_router
from .inbox import router as inbox_router
from .export import router as export_router
from .realtime_monitoring import router as realtime_router
from .staff_activity import router as staff_activity_router
from .view_applications import router as view_applications_router
from .monitoring import router as monitoring_router
from .language_change import router as language_change_router
from .create_connection import router as create_connection_router
from .create_technical import router as create_technical_router

manager_new_routers = [
    main_menu_router,
    inbox_router,
    export_router,
    realtime_router,
    staff_activity_router,
    view_applications_router,
    monitoring_router,
    language_change_router,
    create_connection_router,
    create_technical_router
]

__all__ = [
    "manager_new_routers",
    "main_menu_router",
    "inbox_router",
    "export_router",
    "realtime_router",
    "staff_activity_router",
    "view_applications_router",
    "monitoring_router",
    "language_change_router",
    "create_connection_router",
    "create_technical_router"
]