from django.contrib import admin
from .models import Place, Event, SavedPlace


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'place_type', 'city', 'country', 'is_active', 'verified', 'views_count', 'saves_count']
    list_filter = ['place_type', 'is_active', 'verified', 'country', 'city']
    search_fields = ['name', 'description', 'city', 'address']
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'saves_count']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'city', 'start_date', 'end_date', 'is_active']
    list_filter = ['event_type', 'is_active', 'start_date', 'city']
    search_fields = ['title', 'description', 'city']
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'interested_count']


@admin.register(SavedPlace)
class SavedPlaceAdmin(admin.ModelAdmin):
    list_display = ['user', 'place', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'place__name']
    readonly_fields = ['created_at']

