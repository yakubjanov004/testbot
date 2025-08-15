"""
Database Models

This module defines all database models for the AlfaConnect system.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Text, Float,
    ForeignKey, Enum, JSON, Date, Time, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import Base


class UserRole(enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    MANAGER = "manager"
    JUNIOR_MANAGER = "junior_manager"
    CONTROLLER = "controller"
    TECHNICIAN = "technician"
    WAREHOUSE = "warehouse"
    CALL_CENTER = "call_center"
    CALL_CENTER_SUPERVISOR = "call_center_supervisor"
    CLIENT = "client"


class ApplicationStatus(enum.Enum):
    """Application status enumeration"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PENDING = "pending"
    REJECTED = "rejected"


class OrderStatus(enum.Enum):
    """Order status enumeration"""
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PENDING_PAYMENT = "pending_payment"


class ServiceType(enum.Enum):
    """Service type enumeration"""
    CONNECTION = "connection"
    TECHNICAL = "technical"
    CONSULTATION = "consultation"
    UPGRADE = "upgrade"
    REPAIR = "repair"


class NotificationType(enum.Enum):
    """Notification type enumeration"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    TASK = "task"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True)
    full_name = Column(String(200), nullable=False)
    phone_number = Column(String(20), index=True)
    email = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    language = Column(String(10), default="uz")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Additional fields
    address = Column(Text)
    passport_series = Column(String(20))
    passport_number = Column(String(20))
    company_name = Column(String(200))
    inn = Column(String(20))
    balance = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_active = Column(DateTime(timezone=True))
    
    # Relationships
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="client", foreign_keys="Order.client_id")
    assigned_orders = relationship("Order", back_populates="technician", foreign_keys="Order.technician_id")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    statistics = relationship("Statistics", back_populates="user", cascade="all, delete-orphan")


class Application(Base):
    """Application model"""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application_number = Column(String(50), unique=True, index=True)
    service_type = Column(Enum(ServiceType), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.NEW)
    
    # Application details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default="normal")
    
    # Client information
    client_name = Column(String(200))
    client_phone = Column(String(20))
    client_address = Column(Text)
    
    # Service details
    tariff_plan = Column(String(100))
    connection_type = Column(String(50))
    equipment_needed = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))
    scheduled_date = Column(Date)
    scheduled_time = Column(Time)
    
    # Additional fields
    notes = Column(Text)
    rejection_reason = Column(Text)
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="applications", foreign_keys=[user_id])
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    order = relationship("Order", back_populates="application", uselist=False)


class Order(Base):
    """Order model"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    technician_id = Column(Integer, ForeignKey("users.id"))
    
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    order_type = Column(Enum(ServiceType), nullable=False)
    
    # Order details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default="normal")
    
    # Location
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Pricing
    estimated_cost = Column(Float)
    actual_cost = Column(Float)
    payment_status = Column(String(20), default="pending")
    payment_method = Column(String(50))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    assigned_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Work details
    work_performed = Column(Text)
    materials_used = Column(JSON)
    time_spent_minutes = Column(Integer)
    
    # Additional fields
    notes = Column(Text)
    cancellation_reason = Column(Text)
    customer_signature = Column(Text)  # Base64 encoded signature
    
    # Relationships
    application = relationship("Application", back_populates="order")
    client = relationship("User", back_populates="orders", foreign_keys=[client_id])
    technician = relationship("User", back_populates="assigned_orders", foreign_keys=[technician_id])
    technical_services = relationship("TechnicalService", back_populates="order", cascade="all, delete-orphan")
    connection_services = relationship("ConnectionService", back_populates="order", cascade="all, delete-orphan")


class TechnicalService(Base):
    """Technical service model"""
    __tablename__ = "technical_services"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    service_code = Column(String(50), index=True)
    
    # Service details
    service_name = Column(String(200), nullable=False)
    problem_description = Column(Text)
    solution_description = Column(Text)
    
    # Equipment
    equipment_checked = Column(JSON)
    equipment_replaced = Column(JSON)
    
    # Measurements
    signal_strength_before = Column(Float)
    signal_strength_after = Column(Float)
    speed_test_before = Column(JSON)
    speed_test_after = Column(JSON)
    
    # Status
    is_resolved = Column(Boolean, default=False)
    requires_followup = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    order = relationship("Order", back_populates="technical_services")


class ConnectionService(Base):
    """Connection service model"""
    __tablename__ = "connection_services"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # Connection details
    connection_type = Column(String(50), nullable=False)
    tariff_plan = Column(String(100))
    bandwidth = Column(String(50))
    
    # Equipment
    router_model = Column(String(100))
    router_serial = Column(String(100))
    cable_length_meters = Column(Float)
    connectors_used = Column(Integer)
    
    # Network configuration
    ip_address = Column(String(50))
    subnet_mask = Column(String(50))
    gateway = Column(String(50))
    dns_primary = Column(String(50))
    dns_secondary = Column(String(50))
    
    # Testing
    speed_test_result = Column(JSON)
    ping_test_result = Column(JSON)
    
    # Status
    is_activated = Column(Boolean, default=False)
    activation_date = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="connection_services")


class Notification(Base):
    """Notification model"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    type = Column(Enum(NotificationType), default=NotificationType.INFO)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    # Status
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    
    # Related entities
    related_order_id = Column(Integer, ForeignKey("orders.id"))
    related_application_id = Column(Integer, ForeignKey("applications.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="notifications")


class Feedback(Base):
    """Feedback model"""
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    
    # Feedback details
    rating = Column(Integer)  # 1-5 stars
    category = Column(String(50))
    subject = Column(String(200))
    message = Column(Text, nullable=False)
    
    # Response
    response = Column(Text)
    responded_by_id = Column(Integer, ForeignKey("users.id"))
    responded_at = Column(DateTime(timezone=True))
    
    # Status
    is_resolved = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="feedbacks", foreign_keys=[user_id])
    responded_by = relationship("User", foreign_keys=[responded_by_id])


class Statistics(Base):
    """Statistics model"""
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Period
    date = Column(Date, nullable=False, index=True)
    period_type = Column(String(20))  # daily, weekly, monthly
    
    # Metrics
    metric_type = Column(String(50), nullable=False)
    metric_value = Column(Float, default=0)
    metric_data = Column(JSON)
    
    # Counts
    total_orders = Column(Integer, default=0)
    completed_orders = Column(Integer, default=0)
    cancelled_orders = Column(Integer, default=0)
    
    # Financial
    total_revenue = Column(Float, default=0)
    total_cost = Column(Float, default=0)
    
    # Performance
    average_completion_time = Column(Float)  # in hours
    customer_satisfaction_score = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="statistics")