from django.db import models
from django.conf import settings
from places.models import Place


class UserRecommendation(models.Model):
    """
    Personalized place recommendations for users based on their behavior and aesthetics.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_recommendations')
    
    # Recommendation score (0-100)
    score = models.FloatField()
    
    # Reasoning for recommendation
    match_reasons = models.JSONField(default=list, blank=True)  # e.g., ["aesthetic match", "similar saved content"]
    
    # Status
    viewed = models.BooleanField(default=False)
    dismissed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'place']
        ordering = ['-score', '-created_at']
        indexes = [
            models.Index(fields=['user', '-score']),
        ]
    
    def __str__(self):
        return f"{self.place.name} recommended to {self.user.username} (score: {self.score})"


class RecommendationFeedback(models.Model):
    """
    Track user feedback on recommendations to improve the algorithm.
    """
    FEEDBACK_TYPES = [
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('visited', 'Visited'),
        ('saved', 'Saved'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendation_feedback')
    recommendation = models.ForeignKey(UserRecommendation, on_delete=models.CASCADE, related_name='feedback')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.feedback_type} - {self.recommendation.place.name}"

