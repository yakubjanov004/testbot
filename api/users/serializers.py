from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'telegram_id', 'phone', 'role', 'abonent_id', 'language',
            'address', 'region', 'is_active', 'last_activity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """User creation serializer"""
    
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password',
            'telegram_id', 'phone', 'role', 'language', 'address', 'region'
        ]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class TelegramAuthSerializer(serializers.Serializer):
    """Telegram authentication serializer"""
    
    telegram_id = serializers.IntegerField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    
    def validate(self, attrs):
        telegram_id = attrs.get('telegram_id')
        
        try:
            user = User.objects.get(telegram_id=telegram_id)
            attrs['user'] = user
        except User.DoesNotExist:
            # Yangi user yaratish
            user = User.objects.create(
                telegram_id=telegram_id,
                username=attrs.get('username', f"user_{telegram_id}"),
                first_name=attrs.get('first_name', ''),
                last_name=attrs.get('last_name', ''),
                role='client'
            )
            attrs['user'] = user
            
        return attrs