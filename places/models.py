from django.db import models
from django.conf import settings


class Place(models.Model):
    """
    Real-world places to recommend to users based on their aesthetic and interests.
    These are not shopping ads, but genuine lifestyle recommendations.
    """
    PLACE_TYPES = [
        ('restaurant', 'Restaurant'),
        ('cafe', 'Cafe'),
        ('bar', 'Bar'),
        ('popup', 'Pop-up Shop'),
        ('gallery', 'Art Gallery'),
        ('museum', 'Museum'),
        ('park', 'Park'),
        ('event_space', 'Event Space'),
        ('boutique', 'Boutique'),
        ('bookstore', 'Bookstore'),
        ('market', 'Market'),
        ('theater', 'Theater'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    place_type = models.CharField(max_length=50, choices=PLACE_TYPES)
    
    # Location
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Contact and links
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    
    # Visual content
    cover_image = models.ImageField(upload_to='places/', null=True, blank=True)
    
    # Categorization for matching with user aesthetics
    aesthetic_tags = models.JSONField(default=list, blank=True)  # e.g., ["minimalist", "cozy", "industrial"]
    mood_tags = models.JSONField(default=list, blank=True)  # e.g., ["romantic", "lively", "peaceful"]
    features = models.JSONField(default=list, blank=True)  # e.g., ["outdoor seating", "live music", "pet-friendly"]
    
    # Engagement
    views_count = models.IntegerField(default=0)
    saves_count = models.IntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city', 'place_type']),
            models.Index(fields=['is_active', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.city}"


class Event(models.Model):
    """
    Time-limited events at places or standalone events.
    """
    EVENT_TYPES = [
        ('concert', 'Concert'),
        ('exhibition', 'Exhibition'),
        ('workshop', 'Workshop'),
        ('market', 'Market'),
        ('popup', 'Pop-up'),
        ('festival', 'Festival'),
        ('screening', 'Screening'),
        ('performance', 'Performance'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    
    # Can be linked to a place or have its own location
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    location_name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    
    # Timing
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    
    # Details
    cover_image = models.ImageField(upload_to='events/', null=True, blank=True)
    website = models.URLField(blank=True)
    ticket_url = models.URLField(blank=True)
    price_info = models.CharField(max_length=100, blank=True)
    
    # Categorization
    aesthetic_tags = models.JSONField(default=list, blank=True)
    mood_tags = models.JSONField(default=list, blank=True)
    
    # Engagement
    views_count = models.IntegerField(default=0)
    interested_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_date', 'start_time']
        indexes = [
            models.Index(fields=['city', 'start_date']),
            models.Index(fields=['is_active', 'start_date']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.start_date}"


class SavedPlace(models.Model):
    """
    Track which users saved which places.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_saves')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'place']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} saved {self.place.name}"

