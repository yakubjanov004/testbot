from rest_framework import serializers
from .models import ServiceRequest, OrderHistory, Equipment
from users.serializers import UserSerializer


class EquipmentSerializer(serializers.ModelSerializer):
    """Equipment serializer"""
    
    class Meta:
        model = Equipment
        fields = '__all__'
        read_only_fields = ['added_at']


class OrderHistorySerializer(serializers.ModelSerializer):
    """Order history serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = OrderHistory
        fields = '__all__'
        read_only_fields = ['created_at']


class ServiceRequestSerializer(serializers.ModelSerializer):
    """Service request serializer"""
    client = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)
    history = OrderHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'request_id']


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    """Service request creation serializer"""
    
    class Meta:
        model = ServiceRequest
        fields = [
            'workflow_type', 'client', 'title', 'description',
            'location', 'contact_phone', 'priority', 'region'
        ]
    
    def create(self, validated_data):
        # Request ID generatsiya qilish
        import uuid
        validated_data['request_id'] = f"REQ-{uuid.uuid4().hex[:8].upper()}"
        return super().create(validated_data)


class ServiceRequestUpdateSerializer(serializers.ModelSerializer):
    """Service request update serializer"""
    
    class Meta:
        model = ServiceRequest
        fields = [
            'current_status', 'priority', 'assigned_to', 'assigned_role',
            'description', 'location', 'contact_phone'
        ]
    
    def update(self, instance, validated_data):
        # Status o'zgarganini tekshirish
        old_status = instance.current_status
        new_status = validated_data.get('current_status', old_status)
        
        if old_status != new_status:
            # Tarixga yozish
            OrderHistory.objects.create(
                order=instance,
                user=self.context['request'].user,
                action=f"Status o'zgartirildi",
                old_status=old_status,
                new_status=new_status
            )
        
        return super().update(instance, validated_data)