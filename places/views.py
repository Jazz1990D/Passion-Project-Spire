from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Place, Event, SavedPlace
from .serializers import PlaceSerializer, EventSerializer, SavedPlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing places.
    """
    queryset = Place.objects.filter(is_active=True)
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        """Increment views count when retrieving a place"""
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def save_place(self, request, pk=None):
        """Save a place for later"""
        place = self.get_object()
        notes = request.data.get('notes', '')
        
        saved_place, created = SavedPlace.objects.get_or_create(
            user=request.user,
            place=place,
            defaults={'notes': notes}
        )
        
        if created:
            place.saves_count += 1
            place.save()
            return Response({'status': 'place saved'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'place already saved'}, status=status.HTTP_200_OK)


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing events.
    """
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        """Increment views count when retrieving an event"""
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SavedPlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing saved places.
    """
    queryset = SavedPlace.objects.all()
    serializer_class = SavedPlaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter to current user's saved places"""
        return SavedPlace.objects.filter(user=self.request.user)

