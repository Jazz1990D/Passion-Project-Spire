from django.contrib import admin
from .models import UserRecommendation, RecommendationFeedback


@admin.register(UserRecommendation)
class UserRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'place', 'score', 'viewed', 'dismissed', 'created_at']
    list_filter = ['viewed', 'dismissed', 'created_at']
    search_fields = ['user__username', 'place__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RecommendationFeedback)
class RecommendationFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommendation', 'feedback_type', 'created_at']
    list_filter = ['feedback_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']

