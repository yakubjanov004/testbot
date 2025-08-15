"""
Database Package

This package contains all database-related modules including models,
connection management, and CRUD operations.
"""

from .base import Base, get_db, init_db
from .models import (
    User,
    Application,
    Order,
    TechnicalService,
    ConnectionService,
    Notification,
    Statistics,
    Feedback
)
from .crud import (
    UserCRUD,
    ApplicationCRUD,
    OrderCRUD,
    TechnicalServiceCRUD,
    ConnectionServiceCRUD,
    NotificationCRUD,
    StatisticsCRUD,
    FeedbackCRUD
)

__all__ = [
    'Base',
    'get_db',
    'init_db',
    'User',
    'Application',
    'Order',
    'TechnicalService',
    'ConnectionService',
    'Notification',
    'Statistics',
    'Feedback',
    'UserCRUD',
    'ApplicationCRUD',
    'OrderCRUD',
    'TechnicalServiceCRUD',
    'ConnectionServiceCRUD',
    'NotificationCRUD',
    'StatisticsCRUD',
    'FeedbackCRUD'
]