"""
Main Handlers Module - Simplified Implementation

This module sets up all role-based routers with clean integration.
All modules have been simplified to focus on core functionality.
"""

from aiogram import Router

# Import all role routers
from .start_handler import get_start_router
from .client import get_client_router
from .manager import get_manager_router
from .warehouse import get_warehouse_router
from .technician import get_technician_router
from .call_center import get_call_center_router
from .call_center_supervisor import get_call_center_supervisor_router
from .controller import get_controller_router
from .junior_manager import get_junior_manager_router

def setup_handlers(dp):
    """Setup all handlers"""
    try:
        # Include all role routers
        dp.include_router(get_start_router())
        dp.include_router(get_client_router())
        dp.include_router(get_manager_router())
        dp.include_router(get_warehouse_router())
        dp.include_router(get_technician_router())
        dp.include_router(get_call_center_router())
        dp.include_router(get_call_center_supervisor_router())
        dp.include_router(get_controller_router())
        dp.include_router(get_junior_manager_router())
        
        print("✅ All handlers setup successfully")
        
    except Exception as e:
        print(f"❌ Error setting up handlers: {e}")
        raise
