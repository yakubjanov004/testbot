"""
Database CRUD Operations

This module provides CRUD (Create, Read, Update, Delete) operations
for all database models.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date
from sqlalchemy import select, update, delete, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import logging

from .models import (
    User, UserRole,
    Application, ApplicationStatus,
    Order, OrderStatus,
    TechnicalService,
    ConnectionService,
    Notification, NotificationType,
    Feedback,
    Statistics,
    ServiceType
)

logger = logging.getLogger(__name__)


class UserCRUD:
    """CRUD operations for User model"""
    
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> User:
        """Create a new user"""
        user = User(**kwargs)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Created user: {user.telegram_id}")
        return user
    
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_telegram_id(db: AsyncSession, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID"""
        result = await db.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username"""
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_role(db: AsyncSession, role: UserRole) -> List[User]:
        """Get all users with specific role"""
        result = await db.execute(
            select(User).where(User.role == role)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        result = await db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def update(db: AsyncSession, user_id: int, **kwargs) -> Optional[User]:
        """Update user"""
        await db.execute(
            update(User).where(User.id == user_id).values(**kwargs)
        )
        await db.commit()
        return await UserCRUD.get_by_id(db, user_id)
    
    @staticmethod
    async def update_last_active(db: AsyncSession, telegram_id: int) -> None:
        """Update user's last active timestamp"""
        await db.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(last_active=datetime.utcnow())
        )
        await db.commit()
    
    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        """Delete user"""
        result = await db.execute(
            delete(User).where(User.id == user_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def search(db: AsyncSession, query: str) -> List[User]:
        """Search users by name, phone, or username"""
        search_pattern = f"%{query}%"
        result = await db.execute(
            select(User).where(
                or_(
                    User.full_name.ilike(search_pattern),
                    User.username.ilike(search_pattern),
                    User.phone_number.ilike(search_pattern),
                    User.company_name.ilike(search_pattern)
                )
            )
        )
        return result.scalars().all()


class ApplicationCRUD:
    """CRUD operations for Application model"""
    
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Application:
        """Create a new application"""
        # Generate application number
        count = await db.execute(select(func.count(Application.id)))
        app_number = f"APP{datetime.now().strftime('%Y%m%d')}{count.scalar() + 1:04d}"
        kwargs['application_number'] = app_number
        
        application = Application(**kwargs)
        db.add(application)
        await db.commit()
        await db.refresh(application)
        logger.info(f"Created application: {application.application_number}")
        return application
    
    @staticmethod
    async def get_by_id(db: AsyncSession, app_id: int) -> Optional[Application]:
        """Get application by ID with relationships"""
        result = await db.execute(
            select(Application)
            .options(selectinload(Application.user))
            .where(Application.id == app_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_number(db: AsyncSession, app_number: str) -> Optional[Application]:
        """Get application by number"""
        result = await db.execute(
            select(Application)
            .options(selectinload(Application.user))
            .where(Application.application_number == app_number)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: int) -> List[Application]:
        """Get all applications for a user"""
        result = await db.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_by_status(db: AsyncSession, status: ApplicationStatus) -> List[Application]:
        """Get applications by status"""
        result = await db.execute(
            select(Application)
            .options(selectinload(Application.user))
            .where(Application.status == status)
            .order_by(Application.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Application]:
        """Get all applications with pagination"""
        result = await db.execute(
            select(Application)
            .options(selectinload(Application.user))
            .order_by(Application.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def update(db: AsyncSession, app_id: int, **kwargs) -> Optional[Application]:
        """Update application"""
        await db.execute(
            update(Application).where(Application.id == app_id).values(**kwargs)
        )
        await db.commit()
        return await ApplicationCRUD.get_by_id(db, app_id)
    
    @staticmethod
    async def update_status(db: AsyncSession, app_id: int, status: ApplicationStatus) -> Optional[Application]:
        """Update application status"""
        updates = {'status': status}
        if status == ApplicationStatus.COMPLETED:
            updates['completed_at'] = datetime.utcnow()
        
        return await ApplicationCRUD.update(db, app_id, **updates)
    
    @staticmethod
    async def delete(db: AsyncSession, app_id: int) -> bool:
        """Delete application"""
        result = await db.execute(
            delete(Application).where(Application.id == app_id)
        )
        await db.commit()
        return result.rowcount > 0


class OrderCRUD:
    """CRUD operations for Order model"""
    
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Order:
        """Create a new order"""
        # Generate order number
        count = await db.execute(select(func.count(Order.id)))
        order_number = f"ORD{datetime.now().strftime('%Y%m%d')}{count.scalar() + 1:04d}"
        kwargs['order_number'] = order_number
        
        order = Order(**kwargs)
        db.add(order)
        await db.commit()
        await db.refresh(order)
        logger.info(f"Created order: {order.order_number}")
        return order
    
    @staticmethod
    async def get_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
        """Get order by ID with relationships"""
        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.client),
                selectinload(Order.technician),
                selectinload(Order.application)
            )
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_number(db: AsyncSession, order_number: str) -> Optional[Order]:
        """Get order by number"""
        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.client),
                selectinload(Order.technician)
            )
            .where(Order.order_number == order_number)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_client(db: AsyncSession, client_id: int) -> List[Order]:
        """Get all orders for a client"""
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.technician))
            .where(Order.client_id == client_id)
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_by_technician(db: AsyncSession, technician_id: int) -> List[Order]:
        """Get all orders assigned to a technician"""
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.client))
            .where(Order.technician_id == technician_id)
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_by_status(db: AsyncSession, status: OrderStatus) -> List[Order]:
        """Get orders by status"""
        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.client),
                selectinload(Order.technician)
            )
            .where(Order.status == status)
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_unassigned(db: AsyncSession) -> List[Order]:
        """Get unassigned orders"""
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.client))
            .where(
                and_(
                    Order.technician_id.is_(None),
                    Order.status == OrderStatus.NEW
                )
            )
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def assign_technician(db: AsyncSession, order_id: int, technician_id: int) -> Optional[Order]:
        """Assign technician to order"""
        return await OrderCRUD.update(
            db, order_id,
            technician_id=technician_id,
            status=OrderStatus.ASSIGNED,
            assigned_at=datetime.utcnow()
        )
    
    @staticmethod
    async def start_order(db: AsyncSession, order_id: int) -> Optional[Order]:
        """Start working on order"""
        return await OrderCRUD.update(
            db, order_id,
            status=OrderStatus.IN_PROGRESS,
            started_at=datetime.utcnow()
        )
    
    @staticmethod
    async def complete_order(db: AsyncSession, order_id: int, **kwargs) -> Optional[Order]:
        """Complete order"""
        kwargs.update({
            'status': OrderStatus.COMPLETED,
            'completed_at': datetime.utcnow()
        })
        return await OrderCRUD.update(db, order_id, **kwargs)
    
    @staticmethod
    async def update(db: AsyncSession, order_id: int, **kwargs) -> Optional[Order]:
        """Update order"""
        await db.execute(
            update(Order).where(Order.id == order_id).values(**kwargs)
        )
        await db.commit()
        return await OrderCRUD.get_by_id(db, order_id)
    
    @staticmethod
    async def delete(db: AsyncSession, order_id: int) -> bool:
        """Delete order"""
        result = await db.execute(
            delete(Order).where(Order.id == order_id)
        )
        await db.commit()
        return result.rowcount > 0


class TechnicalServiceCRUD:
    """CRUD operations for TechnicalService model"""
    
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> TechnicalService:
        """Create a new technical service record"""
        service = TechnicalService(**kwargs)
        db.add(service)
        await db.commit()
        await db.refresh(service)
        return service
    
    @staticmethod
    async def get_by_order(db: AsyncSession, order_id: int) -> List[TechnicalService]:
        """Get all technical services for an order"""
        result = await db.execute(
            select(TechnicalService)
            .where(TechnicalService.order_id == order_id)
            .order_by(TechnicalService.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def update(db: AsyncSession, service_id: int, **kwargs) -> Optional[TechnicalService]:
        """Update technical service"""
        await db.execute(
            update(TechnicalService)
            .where(TechnicalService.id == service_id)
            .values(**kwargs)
        )
        await db.commit()
        
        result = await db.execute(
            select(TechnicalService).where(TechnicalService.id == service_id)
        )
        return result.scalar_one_or_none()


class ConnectionServiceCRUD:
    """CRUD operations for ConnectionService model"""
    
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> ConnectionService:
        """Create a new connection service record"""
        service = ConnectionService(**kwargs)
        db.add(service)
        await db.commit()
        await db.refresh(service)
        return service
    
    @staticmethod
    async def get_by_order(db: AsyncSession, order_id: int) -> Optional[ConnectionService]:
        """Get connection service for an order"""
        result = await db.execute(
            select(ConnectionService)
            .where(ConnectionService.order_id == order_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def activate(db: AsyncSession, service_id: int) -> Optional[ConnectionService]:
        """Activate connection service"""
        await db.execute(
            update(ConnectionService)
            .where(ConnectionService.id == service_id)
            .values(
                is_activated=True,
                activation_date=datetime.utcnow()
            )
        )
        await db.commit()
        
        result = await db.execute(
            select(ConnectionService).where(ConnectionService.id == service_id)
        )
        return result.scalar_one_or_none()


class NotificationCRUD:
    """CRUD operations for Notification model"""
    
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Notification:
        """Create a new notification"""
        notification = Notification(**kwargs)
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        logger.info(f"Created notification for user {notification.user_id}")
        return notification
    
    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: int, unread_only: bool = False) -> List[Notification]:
        """Get notifications for a user"""
        query = select(Notification).where(Notification.user_id == user_id)
        
        if unread_only:
            query = query.where(Notification.is_read == False)
        
        query = query.order_by(Notification.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def mark_as_read(db: AsyncSession, notification_id: int) -> Optional[Notification]:
        """Mark notification as read"""
        await db.execute(
            update(Notification)
            .where(Notification.id == notification_id)
            .values(
                is_read=True,
                read_at=datetime.utcnow()
            )
        )
        await db.commit()
        
        result = await db.execute(
            select(Notification).where(Notification.id == notification_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def mark_all_as_read(db: AsyncSession, user_id: int) -> int:
        """Mark all notifications as read for a user"""
        result = await db.execute(
            update(Notification)
            .where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False
                )
            )
            .values(
                is_read=True,
                read_at=datetime.utcnow()
            )
        )
        await db.commit()
        return result.rowcount
    
    @staticmethod
    async def delete_old(db: AsyncSession, days: int = 30) -> int:
        """Delete notifications older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = await db.execute(
            delete(Notification)
            .where(Notification.created_at < cutoff_date)
        )
        await db.commit()
        return result.rowcount


class FeedbackCRUD:
    """CRUD operations for Feedback model"""
    
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Feedback:
        """Create a new feedback"""
        feedback = Feedback(**kwargs)
        db.add(feedback)
        await db.commit()
        await db.refresh(feedback)
        return feedback
    
    @staticmethod
    async def get_by_id(db: AsyncSession, feedback_id: int) -> Optional[Feedback]:
        """Get feedback by ID"""
        result = await db.execute(
            select(Feedback)
            .options(
                selectinload(Feedback.user),
                selectinload(Feedback.responded_by)
            )
            .where(Feedback.id == feedback_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: int) -> List[Feedback]:
        """Get all feedback from a user"""
        result = await db.execute(
            select(Feedback)
            .where(Feedback.user_id == user_id)
            .order_by(Feedback.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_unresolved(db: AsyncSession) -> List[Feedback]:
        """Get all unresolved feedback"""
        result = await db.execute(
            select(Feedback)
            .options(selectinload(Feedback.user))
            .where(Feedback.is_resolved == False)
            .order_by(Feedback.created_at.desc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def respond(db: AsyncSession, feedback_id: int, response: str, responded_by_id: int) -> Optional[Feedback]:
        """Add response to feedback"""
        await db.execute(
            update(Feedback)
            .where(Feedback.id == feedback_id)
            .values(
                response=response,
                responded_by_id=responded_by_id,
                responded_at=datetime.utcnow(),
                is_resolved=True
            )
        )
        await db.commit()
        return await FeedbackCRUD.get_by_id(db, feedback_id)


class StatisticsCRUD:
    """CRUD operations for Statistics model"""
    
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Statistics:
        """Create a new statistics record"""
        stats = Statistics(**kwargs)
        db.add(stats)
        await db.commit()
        await db.refresh(stats)
        return stats
    
    @staticmethod
    async def get_by_date_range(
        db: AsyncSession,
        start_date: date,
        end_date: date,
        user_id: Optional[int] = None
    ) -> List[Statistics]:
        """Get statistics for date range"""
        query = select(Statistics).where(
            and_(
                Statistics.date >= start_date,
                Statistics.date <= end_date
            )
        )
        
        if user_id:
            query = query.where(Statistics.user_id == user_id)
        
        query = query.order_by(Statistics.date.desc())
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_summary(
        db: AsyncSession,
        start_date: date,
        end_date: date,
        metric_type: str
    ) -> Dict[str, Any]:
        """Get summary statistics for a metric"""
        result = await db.execute(
            select(
                func.sum(Statistics.metric_value).label('total'),
                func.avg(Statistics.metric_value).label('average'),
                func.min(Statistics.metric_value).label('minimum'),
                func.max(Statistics.metric_value).label('maximum'),
                func.count(Statistics.id).label('count')
            )
            .where(
                and_(
                    Statistics.date >= start_date,
                    Statistics.date <= end_date,
                    Statistics.metric_type == metric_type
                )
            )
        )
        
        row = result.first()
        return {
            'total': row.total or 0,
            'average': row.average or 0,
            'minimum': row.minimum or 0,
            'maximum': row.maximum or 0,
            'count': row.count or 0
        }


# Import timedelta for notification cleanup
from datetime import timedelta