from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_comment', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('author_comment', 'body')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish','status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [CommentInline]
