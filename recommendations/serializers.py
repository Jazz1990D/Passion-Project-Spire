from rest_framework import serializers
from .models import UserRecommendation, RecommendationFeedback
from places.serializers import PlaceSerializer


class UserRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for UserRecommendation model"""
    place = PlaceSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = UserRecommendation
        fields = ['id', 'user', 'place', 'score', 'match_reasons', 'viewed', 
                  'dismissed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class RecommendationFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for RecommendationFeedback model"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = RecommendationFeedback
        fields = ['id', 'user', 'recommendation', 'feedback_type', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
