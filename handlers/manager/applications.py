"""
Applications Main Router - Soddalashtirilgan versiya

Bu modul barcha applications sub-routerlarini birlashtiradi.
"""

from aiogram import Router

def get_manager_applications_router():
    """Main applications router that combines all sub-routers"""
    router = Router()

    # Import and include all sub-routers
    from handlers.manager.applications_list import get_manager_applications_list_router
    from handlers.manager.applications_search import get_manager_applications_search_router
    from handlers.manager.applications_actions import get_manager_applications_actions_router
    from handlers.manager.applications_callbacks import get_manager_applications_callbacks_router
    
    # Include all sub-routers
    router.include_router(get_manager_applications_list_router())
    router.include_router(get_manager_applications_search_router())
    router.include_router(get_manager_applications_actions_router())
    router.include_router(get_manager_applications_callbacks_router())

    return router