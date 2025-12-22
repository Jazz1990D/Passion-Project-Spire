from django.db import models
from django.conf import settings


class Board(models.Model):
    """
    Boards are collections of posts, similar to Pinterest boards.
    Users can create boards to organize their saved content by theme or mood.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='board_covers/', null=True, blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Tags to help with recommendations
    tags = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"


class Post(models.Model):
    """
    Posts are user-uploaded photos/videos or saved content.
    This is the core content that reflects a user's aesthetic and interests.
    """
    CONTENT_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='image')
    
    # Media file
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)
    
    # Optional external URL (for saving content from elsewhere)
    source_url = models.URLField(blank=True)
    
    # Metadata for recommendations
    tags = models.JSONField(default=list, blank=True)
    mood = models.CharField(max_length=100, blank=True)  # e.g., "cozy", "minimalist", "vibrant"
    aesthetic = models.CharField(max_length=100, blank=True)  # e.g., "modern", "vintage", "boho"
    
    # Engagement metrics
    likes_count = models.IntegerField(default=0)
    saves_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Post by {self.user.username} - {self.title or 'Untitled'}"


class BoardPost(models.Model):
    """
    Many-to-many relationship between Boards and Posts.
    A post can be saved to multiple boards.
    """
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_boards')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['board', 'post']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.post} in {self.board}"


class Like(models.Model):
    """
    Track which users liked which posts.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.post}"

