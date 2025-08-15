from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ServiceRequest(models.Model):
    """Service Request model"""
    
    WORKFLOW_TYPES = [
        ('connection_request', 'Ulanish so\'rovi'),
        ('technical_service', 'Texnik xizmat'),
        ('staff_created', 'Xodim yaratgan'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('in_progress', 'Jarayonda'),
        ('assigned', 'Tayinlangan'),
        ('completed', 'Bajarilgan'),
        ('cancelled', 'Bekor qilingan'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Past'),
        ('medium', 'O\'rta'),
        ('high', 'Yuqori'),
        ('urgent', 'Shoshilinch'),
    ]
    
    # Asosiy maydonlar
    request_id = models.CharField(max_length=50, unique=True)
    workflow_type = models.CharField(max_length=30, choices=WORKFLOW_TYPES, default='connection_request')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Ma'lumotlar
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.TextField()
    contact_phone = models.CharField(max_length=20)
    
    # Tayinlash
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_requests')
    assigned_role = models.CharField(max_length=30, blank=True)
    
    # Yaratish ma'lumotlari
    created_by_staff = models.BooleanField(default=False)
    staff_creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_requests')
    
    # Vaqtlar
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Qo'shimcha
    region = models.CharField(max_length=50, blank=True)
    completion_rating = models.IntegerField(null=True, blank=True)
    feedback_comments = models.TextField(blank=True)
    
    class Meta:
        db_table = 'service_requests'
        ordering = ['-created_at']
        verbose_name = 'Xizmat so\'rovi'
        verbose_name_plural = 'Xizmat so\'rovlari'
        
    def __str__(self):
        return f"{self.request_id} - {self.title}"


class OrderHistory(models.Model):
    """Order history tracking"""
    
    order = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'order_history'
        ordering = ['-created_at']
        verbose_name = 'Buyurtma tarixi'
        verbose_name_plural = 'Buyurtma tarixlari'


class Equipment(models.Model):
    """Equipment used in orders"""
    
    order = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'equipment'
        verbose_name = 'Uskuna'
        verbose_name_plural = 'Uskunalar'
