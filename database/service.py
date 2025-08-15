"""
Database Service Module

This module provides high-level database operations for use in handlers.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from .base import async_session_maker
from .models import (
    User, UserRole,
    Application, ApplicationStatus,
    Order, OrderStatus, ServiceType,
    Notification, NotificationType
)
from .crud import (
    UserCRUD,
    ApplicationCRUD,
    OrderCRUD,
    NotificationCRUD,
    FeedbackCRUD,
    StatisticsCRUD
)
import logging

logger = logging.getLogger(__name__)


class DatabaseService:
    """High-level database service for handlers"""
    
    @staticmethod
    async def get_or_create_user(telegram_id: int, **user_data) -> User:
        """Get existing user or create new one"""
        async with async_session_maker() as db:
            user = await UserCRUD.get_by_telegram_id(db, telegram_id)
            
            if not user:
                # Set default values
                user_data.setdefault('telegram_id', telegram_id)
                user_data.setdefault('role', UserRole.CLIENT)
                user_data.setdefault('language', 'uz')
                user_data.setdefault('is_active', True)
                
                user = await UserCRUD.create(db, **user_data)
                logger.info(f"Created new user: {telegram_id}")
                
                # Send welcome notification
                await NotificationCRUD.create(
                    db,
                    user_id=user.id,
                    type=NotificationType.INFO,
                    title="Xush kelibsiz!",
                    message="AlfaConnect tizimiga xush kelibsiz! Sizga qanday yordam bera olamiz?"
                )
            else:
                # Update last active
                await UserCRUD.update_last_active(db, telegram_id)
            
            return user
    
    @staticmethod
    async def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID"""
        async with async_session_maker() as db:
            return await UserCRUD.get_by_telegram_id(db, telegram_id)
    
    @staticmethod
    async def update_user(telegram_id: int, **updates) -> Optional[User]:
        """Update user information"""
        async with async_session_maker() as db:
            user = await UserCRUD.get_by_telegram_id(db, telegram_id)
            if user:
                return await UserCRUD.update(db, user.id, **updates)
            return None
    
    @staticmethod
    async def create_application(user_telegram_id: int, **app_data) -> Optional[Application]:
        """Create new application"""
        async with async_session_maker() as db:
            user = await UserCRUD.get_by_telegram_id(db, user_telegram_id)
            if not user:
                logger.error(f"User not found: {user_telegram_id}")
                return None
            
            app_data['user_id'] = user.id
            application = await ApplicationCRUD.create(db, **app_data)
            
            # Create notification for user
            await NotificationCRUD.create(
                db,
                user_id=user.id,
                type=NotificationType.SUCCESS,
                title="Ariza qabul qilindi",
                message=f"Sizning {application.application_number} raqamli arizangiz qabul qilindi.",
                related_application_id=application.id
            )
            
            # Create notification for managers
            managers = await UserCRUD.get_by_role(db, UserRole.MANAGER)
            for manager in managers:
                await NotificationCRUD.create(
                    db,
                    user_id=manager.id,
                    type=NotificationType.TASK,
                    title="Yangi ariza",
                    message=f"Yangi ariza keldi: {application.application_number}",
                    related_application_id=application.id
                )
            
            return application
    
    @staticmethod
    async def get_user_applications(telegram_id: int) -> List[Application]:
        """Get all applications for a user"""
        async with async_session_maker() as db:
            user = await UserCRUD.get_by_telegram_id(db, telegram_id)
            if user:
                return await ApplicationCRUD.get_by_user(db, user.id)
            return []
    
    @staticmethod
    async def create_order_from_application(app_id: int, **order_data) -> Optional[Order]:
        """Create order from application"""
        async with async_session_maker() as db:
            application = await ApplicationCRUD.get_by_id(db, app_id)
            if not application:
                logger.error(f"Application not found: {app_id}")
                return None
            
            # Create order
            order_data.update({
                'application_id': app_id,
                'client_id': application.user_id,
                'order_type': application.service_type,
                'title': application.title,
                'description': application.description,
                'address': application.client_address,
                'priority': application.priority
            })
            
            order = await OrderCRUD.create(db, **order_data)
            
            # Update application status
            await ApplicationCRUD.update_status(db, app_id, ApplicationStatus.IN_PROGRESS)
            
            # Notify client
            await NotificationCRUD.create(
                db,
                user_id=application.user_id,
                type=NotificationType.INFO,
                title="Buyurtma yaratildi",
                message=f"Sizning arizangiz asosida {order.order_number} raqamli buyurtma yaratildi.",
                related_order_id=order.id
            )
            
            return order
    
    @staticmethod
    async def get_user_orders(telegram_id: int) -> List[Order]:
        """Get all orders for a user"""
        async with async_session_maker() as db:
            user = await UserCRUD.get_by_telegram_id(db, telegram_id)
            if user:
                if user.role == UserRole.CLIENT:
                    return await OrderCRUD.get_by_client(db, user.id)
                elif user.role == UserRole.TECHNICIAN:
                    return await OrderCRUD.get_by_technician(db, user.id)
            return []
    
    @staticmethod
    async def assign_order_to_technician(order_id: int, technician_telegram_id: int) -> Optional[Order]:
        """Assign order to technician"""
        async with async_session_maker() as db:
            technician = await UserCRUD.get_by_telegram_id(db, technician_telegram_id)
            if not technician or technician.role != UserRole.TECHNICIAN:
                logger.error(f"Invalid technician: {technician_telegram_id}")
                return None
            
            order = await OrderCRUD.assign_technician(db, order_id, technician.id)
            
            if order:
                # Notify technician
                await NotificationCRUD.create(
                    db,
                    user_id=technician.id,
                    type=NotificationType.TASK,
                    title="Yangi buyurtma",
                    message=f"Sizga {order.order_number} raqamli buyurtma biriktirildi.",
                    related_order_id=order.id
                )
                
                # Notify client
                await NotificationCRUD.create(
                    db,
                    user_id=order.client_id,
                    type=NotificationType.INFO,
                    title="Texnik tayinlandi",
                    message=f"Sizning {order.order_number} buyurtmangizga texnik tayinlandi.",
                    related_order_id=order.id
                )
            
            return order
    
    @staticmethod
    async def complete_order(order_id: int, **completion_data) -> Optional[Order]:
        """Complete an order"""
        async with async_session_maker() as db:
            order = await OrderCRUD.complete_order(db, order_id, **completion_data)
            
            if order:
                # Update application if exists
                if order.application_id:
                    await ApplicationCRUD.update_status(
                        db, order.application_id, ApplicationStatus.COMPLETED
                    )
                
                # Notify client
                await NotificationCRUD.create(
                    db,
                    user_id=order.client_id,
                    type=NotificationType.SUCCESS,
                    title="Buyurtma yakunlandi",
                    message=f"Sizning {order.order_number} raqamli buyurtmangiz muvaffaqiyatli yakunlandi.",
                    related_order_id=order.id
                )
            
            return order
    
    @staticmethod
    async def get_unread_notifications(telegram_id: int) -> List[Notification]:
        """Get unread notifications for user"""
        async with async_session_maker() as db:
            user = await UserCRUD.get_by_telegram_id(db, telegram_id)
            if user:
                return await NotificationCRUD.get_by_user(db, user.id, unread_only=True)
            return []
    
    @staticmethod
    async def mark_notifications_as_read(telegram_id: int) -> int:
        """Mark all notifications as read for user"""
        async with async_session_maker() as db:
            user = await UserCRUD.get_by_telegram_id(db, telegram_id)
            if user:
                return await NotificationCRUD.mark_all_as_read(db, user.id)
            return 0
    
    @staticmethod
    async def search_users(query: str) -> List[User]:
        """Search users by query"""
        async with async_session_maker() as db:
            return await UserCRUD.search(db, query)
    
    @staticmethod
    async def get_pending_applications() -> List[Application]:
        """Get all pending applications"""
        async with async_session_maker() as db:
            return await ApplicationCRUD.get_by_status(db, ApplicationStatus.NEW)
    
    @staticmethod
    async def get_unassigned_orders() -> List[Order]:
        """Get all unassigned orders"""
        async with async_session_maker() as db:
            return await OrderCRUD.get_unassigned(db)
    
    @staticmethod
    async def get_statistics(start_date: date, end_date: date, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get statistics for date range"""
        async with async_session_maker() as db:
            stats = await StatisticsCRUD.get_by_date_range(db, start_date, end_date, user_id)
            
            # Calculate summary
            total_orders = sum(s.total_orders for s in stats)
            completed_orders = sum(s.completed_orders for s in stats)
            cancelled_orders = sum(s.cancelled_orders for s in stats)
            total_revenue = sum(s.total_revenue for s in stats)
            
            return {
                'period': f"{start_date} - {end_date}",
                'total_orders': total_orders,
                'completed_orders': completed_orders,
                'cancelled_orders': cancelled_orders,
                'completion_rate': (completed_orders / total_orders * 100) if total_orders > 0 else 0,
                'total_revenue': total_revenue,
                'daily_stats': [
                    {
                        'date': s.date,
                        'orders': s.total_orders,
                        'completed': s.completed_orders,
                        'revenue': s.total_revenue
                    }
                    for s in stats
                ]
            }
    
    @staticmethod
    async def create_feedback(telegram_id: int, **feedback_data) -> Optional[Any]:
        """Create feedback from user"""
        async with async_session_maker() as db:
            user = await UserCRUD.get_by_telegram_id(db, telegram_id)
            if not user:
                return None
            
            feedback_data['user_id'] = user.id
            feedback = await FeedbackCRUD.create(db, **feedback_data)
            
            # Notify managers about new feedback
            managers = await UserCRUD.get_by_role(db, UserRole.MANAGER)
            for manager in managers:
                await NotificationCRUD.create(
                    db,
                    user_id=manager.id,
                    type=NotificationType.INFO,
                    title="Yangi fikr-mulohaza",
                    message=f"{user.full_name} dan yangi fikr-mulohaza keldi",
                )
            
            return feedback