from django.db import models
from django.conf import settings
from django.urls import reverse
from chats.models import Chat
from announcement.models import Announcement
from blog.models import Post

class CategoryMinors(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Minor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='minor')
    category = models.ManyToManyField(CategoryMinors, related_name='category_minors', blank=True) 
    
    class Meta:
        ordering = ('user',)

    def __str__(self):
        return self.user.username


class Proect(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='proects/image/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    start = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    minors = models.ManyToManyField(Minor, related_name='minors', blank=True, null=True) 
    major = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='major')
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE, related_name='chat_proect')
    announcement = models.OneToOneField(Chat, on_delete=models.CASCADE, related_name='announcement', blank=True, null=True)
    product = models.ForeignKey(Announcement, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    timetable = models.TextField(blank=True)
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='curator', blank=True, null=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('proect:proect_detail', args=[self.id, self.slug])

