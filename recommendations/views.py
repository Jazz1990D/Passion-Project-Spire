from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserRecommendation, RecommendationFeedback
from .serializers import UserRecommendationSerializer, RecommendationFeedbackSerializer


class UserRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing personalized recommendations.
    """
    queryset = UserRecommendation.objects.all()
    serializer_class = UserRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter to current user's recommendations, excluding dismissed ones"""
        return UserRecommendation.objects.filter(
            user=self.request.user,
            dismissed=False
        ).order_by('-score')
    
    @action(detail=True, methods=['post'])
    def mark_viewed(self, request, pk=None):
        """Mark a recommendation as viewed"""
        recommendation = self.get_object()
        recommendation.viewed = True
        recommendation.save()
        return Response({'status': 'recommendation marked as viewed'})
    
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Dismiss a recommendation"""
        recommendation = self.get_object()
        recommendation.dismissed = True
        recommendation.save()
        return Response({'status': 'recommendation dismissed'})


class RecommendationFeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for submitting feedback on recommendations.
    """
    queryset = RecommendationFeedback.objects.all()
    serializer_class = RecommendationFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter to current user's feedback"""
        return RecommendationFeedback.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically set the user to the current user"""
        serializer.save(user=self.request.user)

