from django.db import models
from django.conf import settings
from django.urls import reverse

class Chat(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chats:chat', args=[self.slug])

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    message = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_readed = models.BooleanField(default=False)
    image0 = models.ImageField(upload_to='messages/image', blank=True)
    image1 = models.ImageField(upload_to='messages/image', blank=True)
    image2 = models.ImageField(upload_to='messages/image', blank=True)
    image3 = models.ImageField(upload_to='messages/image', blank=True)
    image4 = models.ImageField(upload_to='messages/image', blank=True)
    file_message = models.FileField(upload_to='messages/file', blank=True)
    
    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return '{} {}'.format(self.author.username, self.pub_date)