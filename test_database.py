#!/usr/bin/env python3
"""
Database Test Script

This script tests the database functionality to ensure everything works correctly.
"""

import asyncio
import logging
from utils.database import (
    get_user, create_user, update_user, create_order, get_orders,
    update_order_status, get_inventory, add_inventory_item, update_inventory_quantity,
    add_feedback, log_activity, get_statistics
)
from utils.sample_data import initialize_sample_data

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_database():
    """Test all database functions"""
    try:
        print("🧪 Testing database functionality...")
        
        # Test 1: Create user
        print("\n1️⃣ Testing user creation...")
        user_data = {
            'user_id': 999888777,
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'client',
            'phone': '+998901234571',
            'email': 'test@example.com'
        }
        
        success = await create_user(user_data)
        if success:
            print("✅ User created successfully")
        else:
            print("❌ Failed to create user")
        
        # Test 2: Get user
        print("\n2️⃣ Testing user retrieval...")
        user = await get_user(999888777)
        if user:
            print(f"✅ User retrieved: {user['username']} - {user['role']}")
        else:
            print("❌ Failed to retrieve user")
        
        # Test 3: Update user
        print("\n3️⃣ Testing user update...")
        update_success = await update_user(999888777, {'phone': '+998901234572'})
        if update_success:
            print("✅ User updated successfully")
        else:
            print("❌ Failed to update user")
        
        # Test 4: Create order
        print("\n4️⃣ Testing order creation...")
        order_data = {
            'user_id': 999888777,
            'order_type': 'test_order',
            'description': 'Test order for database testing',
            'priority': 'high',
            'location': 'Test location',
            'contact_phone': '+998901234571'
        }
        
        order_id = await create_order(order_data)
        if order_id:
            print(f"✅ Order created successfully with ID: {order_id}")
        else:
            print("❌ Failed to create order")
        
        # Test 5: Get orders
        print("\n5️⃣ Testing order retrieval...")
        orders = await get_orders(user_id=999888777)
        if orders:
            print(f"✅ Retrieved {len(orders)} orders")
            for order in orders:
                print(f"   - Order {order['order_id']}: {order['order_type']} ({order['status']})")
        else:
            print("❌ Failed to retrieve orders")
        
        # Test 6: Update order status
        if order_id:
            print("\n6️⃣ Testing order status update...")
            status_success = await update_order_status(order_id, 'in_progress', 999888777)
            if status_success:
                print("✅ Order status updated successfully")
            else:
                print("❌ Failed to update order status")
        
        # Test 7: Add inventory item
        print("\n7️⃣ Testing inventory item creation...")
        inventory_data = {
            'name': 'Test Item',
            'category': 'Test Category',
            'quantity': 100,
            'unit': 'dona',
            'price': 1000,
            'min_stock': 10
        }
        
        inventory_success = await add_inventory_item(inventory_data)
        if inventory_success:
            print("✅ Inventory item created successfully")
        else:
            print("❌ Failed to create inventory item")
        
        # Test 8: Get inventory
        print("\n8️⃣ Testing inventory retrieval...")
        inventory = await get_inventory()
        if inventory:
            print(f"✅ Retrieved {len(inventory)} inventory items")
            for item in inventory[:3]:  # Show first 3 items
                print(f"   - {item['name']}: {item['quantity']} {item['unit']}")
        else:
            print("❌ Failed to retrieve inventory")
        
        # Test 9: Add feedback
        print("\n9️⃣ Testing feedback creation...")
        feedback_data = {
            'user_id': 999888777,
            'order_id': order_id if order_id else 1,
            'rating': 5,
            'comment': 'Great service!',
            'category': 'test_order'
        }
        
        feedback_success = await add_feedback(feedback_data)
        if feedback_success:
            print("✅ Feedback created successfully")
        else:
            print("❌ Failed to create feedback")
        
        # Test 10: Log activity
        print("\n🔟 Testing activity logging...")
        activity_success = await log_activity(999888777, 'test_action', 'Database test completed')
        if activity_success:
            print("✅ Activity logged successfully")
        else:
            print("❌ Failed to log activity")
        
        # Test 11: Get statistics
        print("\n1️⃣1️⃣ Testing statistics retrieval...")
        stats = await get_statistics()
        if stats:
            print("✅ Statistics retrieved successfully:")
            for key, value in stats.items():
                print(f"   - {key}: {value}")
        else:
            print("❌ Failed to retrieve statistics")
        
        print("\n🎉 Database test completed successfully!")
        
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        print(f"❌ Database test failed: {e}")
        raise

async def test_sample_data():
    """Test sample data initialization"""
    try:
        print("\n📊 Testing sample data initialization...")
        await initialize_sample_data()
        print("✅ Sample data initialization completed")
        
    except Exception as e:
        logger.error(f"Sample data test failed: {e}")
        print(f"❌ Sample data test failed: {e}")
        raise

async def main():
    """Main test function"""
    try:
        # Test basic database functionality
        await test_database()
        
        # Test sample data initialization
        await test_sample_data()
        
        print("\n🎯 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())