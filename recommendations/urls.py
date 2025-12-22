from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRecommendationViewSet, RecommendationFeedbackViewSet

router = DefaultRouter()
router.register(r'recommendations', UserRecommendationViewSet)
router.register(r'feedback', RecommendationFeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
