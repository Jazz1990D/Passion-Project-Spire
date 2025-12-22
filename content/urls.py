from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet, PostViewSet, LikeViewSet

router = DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
