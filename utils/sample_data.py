"""
Sample Data Module

This module provides functions to initialize the database with sample data
for testing and development purposes.
"""

import asyncio
import logging
from typing import List, Dict, Any
from utils.database import (
    create_user, create_order, get_inventory, add_inventory_item, update_inventory_quantity,
    add_feedback, log_activity
)

logger = logging.getLogger(__name__)

async def initialize_sample_data():
    """Initialize database with sample data"""
    try:
        logger.info("Initializing sample data...")
        
        # Create sample users
        await create_sample_users()
        
        # Create sample orders
        await create_sample_orders()
        
        # Create sample inventory
        await create_sample_inventory()
        
        # Create sample feedback
        await create_sample_feedback()
        
        logger.info("Sample data initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error initializing sample data: {e}")
        raise

async def create_sample_users():
    """Create sample users"""
    sample_users = [
        {
            'user_id': 123456789,
            'username': 'admin_user',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'phone': '+998901234567',
            'email': 'admin@alfaconnect.uz'
        },
        {
            'user_id': 987654321,
            'username': 'manager_user',
            'first_name': 'Manager',
            'last_name': 'User',
            'role': 'manager',
            'phone': '+998901234568',
            'email': 'manager@alfaconnect.uz'
        },
        {
            'user_id': 111222333,
            'username': 'client_user',
            'first_name': 'Client',
            'last_name': 'User',
            'role': 'client',
            'phone': '+998901234569',
            'email': 'client@example.com'
        },
        {
            'user_id': 444555666,
            'username': 'technician_user',
            'first_name': 'Technician',
            'last_name': 'User',
            'role': 'technician',
            'phone': '+998901234570',
            'email': 'technician@alfaconnect.uz'
        }
    ]
    
    for user_data in sample_users:
        try:
            await create_user(user_data)
            logger.info(f"Created sample user: {user_data['username']}")
        except Exception as e:
            logger.warning(f"Could not create user {user_data['username']}: {e}")

async def create_sample_orders():
    """Create sample orders"""
    sample_orders = [
        {
            'user_id': 111222333,
            'order_type': 'internet_connection',
            'description': 'Yangi internet ulanish so\'rovi',
            'priority': 'high',
            'location': 'Toshkent shahri, Chilonzor tumani',
            'contact_phone': '+998901234569'
        },
        {
            'user_id': 111222333,
            'order_type': 'technical_support',
            'description': 'Internet tezligi past, texnik yordam kerak',
            'priority': 'normal',
            'location': 'Toshkent shahri, Chilonzor tumani',
            'contact_phone': '+998901234569'
        },
        {
            'user_id': 987654321,
            'order_type': 'equipment_installation',
            'description': 'Antenna o\'rnatish',
            'priority': 'high',
            'location': 'Toshkent shahri, Sergeli tumani',
            'contact_phone': '+998901234568'
        }
    ]
    
    for order_data in sample_orders:
        try:
            order_id = await create_order(order_data)
            if order_id:
                logger.info(f"Created sample order: {order_data['order_type']}")
        except Exception as e:
            logger.warning(f"Could not create order {order_data['order_type']}: {e}")

async def create_sample_inventory():
    """Create sample inventory items"""
    sample_inventory = [
        {
            'name': 'Antenna 2.4GHz 9dBi',
            'category': 'Antennalar',
            'quantity': 50,
            'unit': 'dona',
            'price': 95000,
            'min_stock': 10
        },
        {
            'name': 'Antenna 5GHz 16dBi',
            'category': 'Antennalar',
            'quantity': 30,
            'unit': 'dona',
            'price': 145000,
            'min_stock': 5
        },
        {
            'name': 'Router TP-Link Archer C6',
            'category': 'Routerlar',
            'quantity': 25,
            'unit': 'dona',
            'price': 350000,
            'min_stock': 8
        },
        {
            'name': 'Cable UTP Cat6 100m',
            'category': 'Kabellar',
            'quantity': 100,
            'unit': 'metr',
            'price': 2500,
            'min_stock': 20
        },
        {
            'name': 'Connector RJ45',
            'category': 'Konnektorlar',
            'quantity': 200,
            'unit': 'dona',
            'price': 500,
            'min_stock': 50
        }
    ]
    
    for item_data in sample_inventory:
        try:
            success = await add_inventory_item(item_data)
            if success:
                logger.info(f"Created sample inventory item: {item_data['name']}")
        except Exception as e:
            logger.warning(f"Could not create inventory item {item_data['name']}: {e}")

async def create_sample_feedback():
    """Create sample feedback"""
    sample_feedback = [
        {
            'user_id': 111222333,
            'order_id': 1,
            'rating': 5,
            'comment': 'Juda yaxshi xizmat, tez va sifatli',
            'category': 'internet_connection'
        },
        {
            'user_id': 111222333,
            'order_id': 2,
            'rating': 4,
            'comment': 'Muammo hal qilindi, lekin biroz vaqt ketti',
            'category': 'technical_support'
        },
        {
            'user_id': 987654321,
            'order_id': 3,
            'rating': 5,
            'comment': 'Professional ish, tavsiya etaman',
            'category': 'equipment_installation'
        }
    ]
    
    for feedback_data in sample_feedback:
        try:
            success = await add_feedback(feedback_data)
            if success:
                logger.info(f"Created sample feedback for order {feedback_data['order_id']}")
        except Exception as e:
            logger.warning(f"Could not create feedback for order {feedback_data['order_id']}: {e}")

async def create_sample_activity_logs():
    """Create sample activity logs"""
    sample_activities = [
        (123456789, 'login', 'Admin user logged in'),
        (987654321, 'order_created', 'New order created for client'),
        (111222333, 'feedback_submitted', 'Client submitted feedback'),
        (444555666, 'order_assigned', 'Order assigned to technician')
    ]
    
    for user_id, action, details in sample_activities:
        try:
            success = await log_activity(user_id, action, details)
            if success:
                logger.info(f"Created sample activity log: {action}")
        except Exception as e:
            logger.warning(f"Could not create activity log {action}: {e}")

async def clear_sample_data():
    """Clear all sample data from database"""
    try:
        logger.info("Clearing sample data...")
        
        # This would require direct database access to clear tables
        # For now, we'll just log the intention
        logger.info("Sample data clear operation prepared")
        
    except Exception as e:
        logger.error(f"Error clearing sample data: {e}")
        raise

if __name__ == "__main__":
    # Run sample data initialization
    asyncio.run(initialize_sample_data())