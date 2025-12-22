from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, EventViewSet, SavedPlaceViewSet

router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'events', EventViewSet)
router.register(r'saved', SavedPlaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
