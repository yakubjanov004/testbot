from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model for AlfaConnect"""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('junior_manager', 'Junior Manager'),
        ('controller', 'Controller'),
        ('technician', 'Technician'),
        ('warehouse', 'Warehouse'),
        ('call_center', 'Call Center'),
        ('call_center_supervisor', 'Call Center Supervisor'),
        ('client', 'Client'),
        ('blocked', 'Blocked'),
    ]
    
    LANGUAGE_CHOICES = [
        ('uz', 'O\'zbek'),
        ('ru', 'Русский'),
    ]
    
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='client')
    abonent_id = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='uz')
    address = models.TextField(blank=True)
    region = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"
