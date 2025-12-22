from django.contrib import admin
from .models import Board, Post, BoardPost, Like


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_private', 'created_at', 'updated_at']
    list_filter = ['is_private', 'created_at']
    search_fields = ['title', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'content_type', 'mood', 'aesthetic', 'likes_count', 'saves_count', 'created_at']
    list_filter = ['content_type', 'mood', 'aesthetic', 'created_at']
    search_fields = ['title', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at', 'likes_count', 'saves_count']


@admin.register(BoardPost)
class BoardPostAdmin(admin.ModelAdmin):
    list_display = ['board', 'post', 'added_at']
    list_filter = ['added_at']
    search_fields = ['board__title', 'post__title']
    readonly_fields = ['added_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['created_at']

