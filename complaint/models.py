from django.db import models
from django.conf import settings
from django.urls import reverse
from blog.models import Post, Comment
from shop.models import Product, Comment
from announcement.models import Announcement, Comment
from account.models import Profile


class Complaint(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_complaint', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_complaint', blank=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='announcement_complaint')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_complaint', blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_complaint', blank=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    author = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='author_complaint') 
    description = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('complaint:complaint', args=[self.id, self.slug])
