from rest_framework import serializers
from .models import Board, Post, BoardPost, Like


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for Board model"""
    user = serializers.StringRelatedField(read_only=True)
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'user', 'title', 'description', 'cover_image', 'is_private', 
                  'tags', 'post_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_post_count(self, obj):
        return obj.board_posts.count()


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'description', 'content_type', 'image', 
                  'video', 'source_url', 'tags', 'mood', 'aesthetic', 'likes_count', 
                  'saves_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'likes_count', 'saves_count', 'created_at', 'updated_at']


class BoardPostSerializer(serializers.ModelSerializer):
    """Serializer for BoardPost model"""
    post = PostSerializer(read_only=True)
    
    class Meta:
        model = BoardPost
        fields = ['id', 'board', 'post', 'added_at']
        read_only_fields = ['id', 'added_at']


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
