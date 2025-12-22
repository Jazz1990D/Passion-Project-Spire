from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Board, Post, BoardPost, Like
from .serializers import BoardSerializer, PostSerializer, BoardPostSerializer, LikeSerializer


class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing boards.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter to show public boards and user's own boards"""
        if self.request.user.is_authenticated:
            return Board.objects.filter(
                models.Q(is_private=False) | models.Q(user=self.request.user)
            )
        return Board.objects.filter(is_private=False)
    
    def perform_create(self, serializer):
        """Automatically set the user to the current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_post(self, request, pk=None):
        """Add a post to this board"""
        board = self.get_object()
        post_id = request.data.get('post_id')
        
        if not post_id:
            return Response({'error': 'post_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Post.objects.get(id=post_id)
            BoardPost.objects.get_or_create(board=board, post=post)
            return Response({'status': 'post added to board'}, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """Automatically set the user to the current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a post"""
        post = self.get_object()
        Like.objects.get_or_create(user=request.user, post=post)
        post.likes_count += 1
        post.save()
        return Response({'status': 'post liked'}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Unlike a post"""
        post = self.get_object()
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            post.save()
            return Response({'status': 'post unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'error': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing likes.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter to current user's likes if authenticated"""
        if self.request.user.is_authenticated:
            return Like.objects.filter(user=self.request.user)
        return Like.objects.none()

