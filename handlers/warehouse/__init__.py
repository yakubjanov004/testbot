"""
Warehouse Module - Complete Implementation

This module provides complete warehouse functionality including:
- Main menu and navigation
- Orders management
- Inventory management
- Export functionality
- Language settings
- Statistics and reports
- Inbox management
- Workflow integration
- Role integration
"""

from utils.role_system import get_role_router
from .main_menu import get_warehouse_main_menu_router
from .orders import get_warehouse_orders_router
from .inventory import get_warehouse_inventory_router
from .export import get_warehouse_export_router
from .statistics import get_warehouse_statistics_router
from .inbox import get_warehouse_inbox_router
from .workflow_integration import get_warehouse_workflow_router
from .role_integration import get_warehouse_role_integration_router

warehouse_router = get_role_router("warehouse")

# Include all warehouse routers
warehouse_router.include_router(get_warehouse_main_menu_router())
warehouse_router.include_router(get_warehouse_orders_router())
warehouse_router.include_router(get_warehouse_inventory_router())
warehouse_router.include_router(get_warehouse_export_router())
warehouse_router.include_router(get_warehouse_statistics_router())
warehouse_router.include_router(get_warehouse_inbox_router())
warehouse_router.include_router(get_warehouse_workflow_router())

# Include role integration router for all roles
role_integration_router = get_warehouse_role_integration_router()

def get_warehouse_router():
    """Get the complete warehouse router with all handlers"""
    return warehouse_router

def get_warehouse_role_integration():
    """Get the warehouse role integration router"""
    return role_integration_router
