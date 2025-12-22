from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserBehaviorViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'behavior', UserBehaviorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
