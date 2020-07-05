from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('announcement:announcement_list_by_category', args=[self.slug])

class Announcement(models.Model):
    category = models.ManyToManyField(Category, related_name='category', blank=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author_ann = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_ann')
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='announcement/%Y/%m/%d', blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)
    

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('announcement:announcement_detail', args=[self.id, self.slug])


class Comment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    author_comment_ann = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_comment_ann', on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='announcement/comment_image/%Y/%m/%d', blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author_comment.first_name, self.post)
