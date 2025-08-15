"""
API Client for Telegram Bot

Bu modul Django REST API bilan bog'lanish uchun ishlatiladi.
"""

import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
from config import API_BASE_URL


class AlfaConnectAPIClient:
    """API client for AlfaConnect Django REST API"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or API_BASE_URL or "http://localhost:8000/api"
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with self.session.request(method, url, **kwargs) as response:
                data = await response.json()
                
                if response.status >= 400:
                    raise Exception(f"API Error: {data.get('detail', 'Unknown error')}")
                
                return data
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
    
    # User methods
    async def get_or_create_user(self, telegram_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get or create user by telegram data"""
        return await self._request(
            "POST",
            "users/telegram-auth/",
            json=telegram_data
        )
    
    async def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user by ID"""
        return await self._request("GET", f"users/{user_id}/")
    
    async def update_user(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user data"""
        return await self._request(
            "PATCH",
            f"users/{user_id}/",
            json=data
        )
    
    # Order methods
    async def create_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new service request"""
        return await self._request(
            "POST",
            "orders/",
            json=data
        )
    
    async def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order by ID"""
        return await self._request("GET", f"orders/{order_id}/")
    
    async def update_order(self, order_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update order"""
        return await self._request(
            "PATCH",
            f"orders/{order_id}/",
            json=data
        )
    
    async def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's orders"""
        return await self._request(
            "GET",
            "orders/",
            params={"client": user_id}
        )
    
    async def get_orders_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get orders by status"""
        return await self._request(
            "GET",
            "orders/",
            params={"current_status": status}
        )
    
    # Statistics methods
    async def get_statistics(self, region: str = None) -> Dict[str, Any]:
        """Get statistics"""
        params = {}
        if region:
            params["region"] = region
        
        return await self._request(
            "GET",
            "reports/statistics/",
            params=params
        )
    
    async def get_staff_activity(self, user_id: int = None) -> List[Dict[str, Any]]:
        """Get staff activity"""
        params = {}
        if user_id:
            params["user_id"] = user_id
        
        return await self._request(
            "GET",
            "reports/staff-activity/",
            params=params
        )


# Global client instance
api_client = AlfaConnectAPIClient()


# Helper functions for bot handlers
async def authenticate_telegram_user(telegram_user) -> Dict[str, Any]:
    """Authenticate telegram user through API"""
    async with AlfaConnectAPIClient() as client:
        return await client.get_or_create_user({
            "telegram_id": telegram_user.id,
            "first_name": telegram_user.first_name or "",
            "last_name": telegram_user.last_name or "",
            "username": telegram_user.username or ""
        })


async def create_connection_order(user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create connection order"""
    async with AlfaConnectAPIClient() as client:
        order_data = {
            "client": user_id,
            "workflow_type": "connection_request",
            **data
        }
        return await client.create_order(order_data)


async def create_service_order(user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create service order"""
    async with AlfaConnectAPIClient() as client:
        order_data = {
            "client": user_id,
            "workflow_type": "technical_service",
            **data
        }
        return await client.create_order(order_data)


async def get_user_orders(user_id: int) -> List[Dict[str, Any]]:
    """Get user orders"""
    async with AlfaConnectAPIClient() as client:
        return await client.get_user_orders(user_id)