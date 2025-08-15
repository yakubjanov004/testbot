"""
Database Module - SQLite Implementation

This module provides database functionality for the Telegram bot.
Uses SQLite for simplicity and easy deployment.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import aiosqlite

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "bot_database.db"):
        self.db_path = db_path
        self._lock = asyncio.Lock()
        self._initialized = False
    
    async def ensure_initialized(self):
        """Ensure database is initialized"""
        if not self._initialized:
            await self._init_database()
            self._initialized = True
    
    async def _init_database(self):
        """Initialize database tables"""
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                # Users table
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        role TEXT DEFAULT 'client',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1,
                        phone TEXT,
                        email TEXT,
                        notes TEXT
                    )
                ''')
                
                # Orders table
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        order_type TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        assigned_to INTEGER,
                        priority TEXT DEFAULT 'normal',
                        location TEXT,
                        contact_phone TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (user_id),
                        FOREIGN KEY (assigned_to) REFERENCES users (user_id)
                    )
                ''')
                
                # Inventory table
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS inventory (
                        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT,
                        quantity INTEGER DEFAULT 0,
                        unit TEXT,
                        price REAL,
                        min_stock INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Feedback table
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS feedback (
                        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        order_id INTEGER,
                        rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                        comment TEXT,
                        category TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id),
                        FOREIGN KEY (order_id) REFERENCES orders (order_id)
                    )
                ''')
                
                # Activity logs table
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS activity_logs (
                        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        action TEXT,
                        details TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ip_address TEXT,
                        user_agent TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                
                await conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    async def execute_query(self, query: str, params: tuple = ()) -> List[Tuple]:
        """Execute a query and return results"""
        await self.ensure_initialized()
        async with self._lock:
            try:
                async with aiosqlite.connect(self.db_path) as conn:
                    cursor = await conn.execute(query, params)
                    
                    if query.strip().upper().startswith('SELECT'):
                        result = await cursor.fetchall()
                        return result
                    else:
                        await conn.commit()
                        return []
                        
            except Exception as e:
                logger.error(f"Database query error: {e}")
                raise
    
    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = ?"
        result = await self.execute_query(query, (user_id,))
        
        if result:
            columns = ['user_id', 'username', 'first_name', 'last_name', 'role', 
                      'created_at', 'updated_at', 'is_active', 'phone', 'email', 'notes']
            return dict(zip(columns, result[0]))
        return None
    
    async def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Create a new user"""
        query = '''
            INSERT INTO users (user_id, username, first_name, last_name, role, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        try:
            await self.execute_query(query, (
                user_data['user_id'],
                user_data.get('username'),
                user_data.get('first_name'),
                user_data.get('last_name'),
                user_data.get('role', 'client'),
                user_data.get('phone'),
                user_data.get('email')
            ))
            return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    async def update_user(self, user_id: int, update_data: Dict[str, Any]) -> bool:
        """Update user data"""
        set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
        query = f"UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?"
        
        try:
            params = list(update_data.values()) + [user_id]
            await self.execute_query(query, tuple(params))
            return True
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False
    
    async def create_order(self, order_data: Dict[str, Any]) -> Optional[int]:
        """Create a new order"""
        async with self._lock:
            try:
                async with aiosqlite.connect(self.db_path) as conn:
                    await self.ensure_initialized()
                    
                    cursor = await conn.execute('''
                        INSERT INTO orders (user_id, order_type, description, priority, location, contact_phone)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        order_data['user_id'],
                        order_data['order_type'],
                        order_data.get('description'),
                        order_data.get('priority', 'normal'),
                        order_data.get('location'),
                        order_data.get('contact_phone')
                    ))
                    
                    await conn.commit()
                    
                    # Get the created order ID
                    result = await conn.execute("SELECT last_insert_rowid()")
                    row = await result.fetchone()
                    return row[0] if row else None
                    
            except Exception as e:
                logger.error(f"Error creating order: {e}")
                return None
    
    async def get_orders(self, user_id: Optional[int] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get orders with optional filters"""
        query = "SELECT * FROM orders WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        try:
            result = await self.execute_query(query, tuple(params))
            columns = ['order_id', 'user_id', 'order_type', 'status', 'description', 
                      'created_at', 'updated_at', 'assigned_to', 'priority', 'location', 'contact_phone']
            
            return [dict(zip(columns, row)) for row in result]
            
        except Exception as e:
            logger.error(f"Error getting orders: {e}")
            return []
    
    async def update_order_status(self, order_id: int, status: str, assigned_to: Optional[int] = None) -> bool:
        """Update order status"""
        query = "UPDATE orders SET status = ?, assigned_to = ?, updated_at = CURRENT_TIMESTAMP WHERE order_id = ?"
        try:
            await self.execute_query(query, (status, assigned_to, order_id))
            return True
        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            return False
    
    async def get_inventory(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get inventory items"""
        query = "SELECT * FROM inventory"
        params = []
        
        if category:
            query += " WHERE category = ?"
            params.append(category)
        
        query += " ORDER BY name"
        
        try:
            result = await self.execute_query(query, tuple(params))
            columns = ['item_id', 'name', 'category', 'quantity', 'unit', 'price', 
                      'min_stock', 'created_at', 'updated_at']
            
            return [dict(zip(columns, row)) for row in result]
            
        except Exception as e:
            logger.error(f"Error getting inventory: {e}")
            return []
    
    async def add_inventory_item(self, item_data: Dict[str, Any]) -> bool:
        """Add new inventory item"""
        query = '''
            INSERT INTO inventory (name, category, quantity, unit, price, min_stock)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        try:
            await self.execute_query(query, (
                item_data['name'],
                item_data.get('category'),
                item_data.get('quantity', 0),
                item_data.get('unit'),
                item_data.get('price', 0),
                item_data.get('min_stock', 0)
            ))
            return True
        except Exception as e:
            logger.error(f"Error adding inventory item: {e}")
            return False
    
    async def update_inventory_quantity(self, item_id: int, quantity: int) -> bool:
        """Update inventory quantity"""
        query = "UPDATE inventory SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE item_id = ?"
        try:
            await self.execute_query(query, (quantity, item_id))
            return True
        except Exception as e:
            logger.error(f"Error updating inventory: {e}")
            return False
    
    async def add_feedback(self, feedback_data: Dict[str, Any]) -> bool:
        """Add feedback"""
        query = '''
            INSERT INTO feedback (user_id, order_id, rating, comment, category)
            VALUES (?, ?, ?, ?, ?)
        '''
        try:
            await self.execute_query(query, (
                feedback_data['user_id'],
                feedback_data.get('order_id'),
                feedback_data['rating'],
                feedback_data.get('comment'),
                feedback_data.get('category')
            ))
            return True
        except Exception as e:
            logger.error(f"Error adding feedback: {e}")
            return False
    
    async def log_activity(self, user_id: int, action: str, details: str = "") -> bool:
        """Log user activity"""
        query = '''
            INSERT INTO activity_logs (user_id, action, details)
            VALUES (?, ?, ?)
        '''
        try:
            await self.execute_query(query, (user_id, action, details))
            return True
        except Exception as e:
            logger.error(f"Error logging activity: {e}")
            return False
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        try:
            stats = {}
            
            # User count
            result = await self.execute_query("SELECT COUNT(*) FROM users")
            stats['total_users'] = result[0][0] if result else 0
            
            # Active users
            result = await self.execute_query("SELECT COUNT(*) FROM users WHERE is_active = 1")
            stats['active_users'] = result[0][0] if result else 0
            
            # Total orders
            result = await self.execute_query("SELECT COUNT(*) FROM orders")
            stats['total_orders'] = result[0][0] if result else 0
            
            # Pending orders
            result = await self.execute_query("SELECT COUNT(*) FROM orders WHERE status = 'pending'")
            stats['pending_orders'] = result[0][0] if result else 0
            
            # Completed orders
            result = await self.execute_query("SELECT COUNT(*) FROM orders WHERE status = 'completed'")
            stats['completed_orders'] = result[0][0] if result else 0
            
            # Total inventory items
            result = await self.execute_query("SELECT COUNT(*) FROM inventory")
            stats['total_inventory_items'] = result[0][0] if result else 0
            
            # Low stock items
            result = await self.execute_query("SELECT COUNT(*) FROM inventory WHERE quantity <= min_stock")
            stats['low_stock_items'] = result[0][0] if result else 0
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}

# Global database instance
db = Database()

# Convenience functions
async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    return await db.get_user(user_id)

async def create_user(user_data: Dict[str, Any]) -> bool:
    return await db.create_user(user_data)

async def update_user(user_id: int, update_data: Dict[str, Any]) -> bool:
    return await db.update_user(user_id, update_data)

async def create_order(order_data: Dict[str, Any]) -> Optional[int]:
    return await db.create_order(order_data)

async def get_orders(user_id: Optional[int] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    return await db.get_orders(user_id, status)

async def update_order_status(order_id: int, status: str, assigned_to: Optional[int] = None) -> bool:
    return await db.update_order_status(order_id, status, assigned_to)

async def get_inventory(category: Optional[str] = None) -> List[Dict[str, Any]]:
    return await db.get_inventory(category)

async def add_inventory_item(item_data: Dict[str, Any]) -> bool:
    return await db.add_inventory_item(item_data)

async def update_inventory_quantity(item_id: int, quantity: int) -> bool:
    return await db.update_inventory_quantity(item_id, quantity)

async def add_feedback(feedback_data: Dict[str, Any]) -> bool:
    return await db.add_feedback(feedback_data)

async def log_activity(user_id: int, action: str, details: str = "") -> bool:
    return await db.log_activity(user_id, action, details)

async def get_statistics() -> Dict[str, Any]:
    return await db.get_statistics()