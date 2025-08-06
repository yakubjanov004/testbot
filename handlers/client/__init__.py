"""
Client Module - Complete Implementation

This module provides complete client functionality including:
- Start and registration
- Contact management
- Feedback system
- Help and support
- Language settings
- Main menu and navigation
- Connection orders
- Service orders
- Profile management
- Order utilities
"""

from utils.role_system import get_role_router
from .start import get_client_start_router
from .contact import get_client_contact_router
from .feedback import get_client_feedback_router
from .help import get_client_help_router
from .language import get_client_language_router
from .main_menu import get_client_main_menu_router
from .connection_order import get_connection_order_router
from .service_order import get_service_order_router
from .profile import get_client_profile_router
from .orders import get_orders_router

# Use role router for client functionality
client_router = get_role_router("client")

# Include all client routers
client_router.include_router(get_client_start_router())
client_router.include_router(get_client_contact_router())
client_router.include_router(get_client_feedback_router())
client_router.include_router(get_client_help_router())
client_router.include_router(get_client_language_router())
client_router.include_router(get_client_main_menu_router())
client_router.include_router(get_connection_order_router())
client_router.include_router(get_service_order_router())
client_router.include_router(get_client_profile_router())
client_router.include_router(get_orders_router())

def get_client_router():
    """Get the complete client router with all handlers"""
    return client_router

