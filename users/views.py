from rest_framework import viewsets, permissions
from .models import User, UserBehavior
from .serializers import UserSerializer, UserBehaviorSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing user profiles.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserBehaviorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for tracking user behavior.
    """
    queryset = UserBehavior.objects.all()
    serializer_class = UserBehaviorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter behaviors to current user"""
        return UserBehavior.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically set the user to the current user"""
        serializer.save(user=self.request.user)

