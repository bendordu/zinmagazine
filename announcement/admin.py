from django.contrib import admin
from .models import Announcement, Category, Comment

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['author_ann', 'title', 'created', 'active']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_comment_ann', 'announcement', 'created']