from rest_framework import serializers
from .models import User, UserBehavior


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 
                  'profile_picture', 'favorite_categories', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserBehaviorSerializer(serializers.ModelSerializer):
    """Serializer for UserBehavior model"""
    
    class Meta:
        model = UserBehavior
        fields = ['id', 'user', 'interaction_type', 'content_type', 'content_id', 
                  'tags', 'timestamp']
        read_only_fields = ['id', 'timestamp']
