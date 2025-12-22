from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model for Spire application.
    Extends Django's AbstractUser to add profile and preference fields.
    """
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # User preferences for recommendations
    favorite_categories = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username


class UserBehavior(models.Model):
    """
    Track user behavior for recommendation engine.
    Records what users interact with to suggest relevant places.
    """
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('save', 'Save'),
        ('share', 'Share'),
        ('like', 'Like'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behaviors')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    content_type = models.CharField(max_length=50)  # 'post', 'board', 'place'
    content_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional metadata for recommendation algorithm
    tags = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['content_type', 'content_id']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.content_type}"

