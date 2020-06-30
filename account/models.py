from django.db import models
from django.conf import settings
from django.urls import reverse

class CategoryProfile(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profile_list_by_category', args=[self.slug])

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    category = models.ManyToManyField(CategoryProfile, related_name='category', null=True, blank=True)
    about = models.TextField(blank=True) 
    slug = models.SlugField(max_length=200, db_index=True, default=user)
    
    class Meta:
        index_together = (('id', 'slug'),)

    def __str__(self):
        return 'Profile by {} {}'.format(self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return reverse('profile_detail', args=[self.id, self.slug])
