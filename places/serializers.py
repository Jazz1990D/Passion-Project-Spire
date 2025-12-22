from rest_framework import serializers
from .models import Place, Event, SavedPlace


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for Place model"""
    
    class Meta:
        model = Place
        fields = ['id', 'name', 'description', 'place_type', 'address', 'city', 'state', 
                  'country', 'latitude', 'longitude', 'phone', 'website', 'instagram', 
                  'cover_image', 'aesthetic_tags', 'mood_tags', 'features', 'views_count', 
                  'saves_count', 'is_active', 'verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'views_count', 'saves_count', 'created_at', 'updated_at']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    place = PlaceSerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_type', 'place', 'location_name', 
                  'address', 'city', 'start_date', 'end_date', 'start_time', 'cover_image', 
                  'website', 'ticket_url', 'price_info', 'aesthetic_tags', 'mood_tags', 
                  'views_count', 'interested_count', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'views_count', 'interested_count', 'created_at', 'updated_at']


class SavedPlaceSerializer(serializers.ModelSerializer):
    """Serializer for SavedPlace model"""
    user = serializers.StringRelatedField(read_only=True)
    place = PlaceSerializer(read_only=True)
    
    class Meta:
        model = SavedPlace
        fields = ['id', 'user', 'place', 'notes', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
