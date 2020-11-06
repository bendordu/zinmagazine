from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class TypePr(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_type_pr', args=[self.slug])

class PriceType(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_price_type', args=[self.slug])

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    author_product = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='products/image', blank=True)
    image_dop1 = models.ImageField(upload_to='products/image', blank=True)
    image_dop2 = models.ImageField(upload_to='products/image', blank=True)
    file_product = models.FileField(upload_to='products/file', blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    quantity_pr = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_created') 
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_liked', blank=True)
    count_order = models.IntegerField(validators=[MinValueValidator(0)], default=0, blank=True)
    buyers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_buyers', blank=True)
    type_pr = models.ForeignKey(TypePr, on_delete=models.CASCADE, related_name='type_pr', default=1)
    bye_paper = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bye_paper', blank=True)
    price_type = models.ForeignKey(PriceType, on_delete=models.CASCADE, related_name='pice_type', default=1)
    donate_sum = models.IntegerField(validators=[MinValueValidator(0)], default=0)


    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author') 
    image0 = models.ImageField(upload_to='comment_image', blank=True)
    image1 = models.ImageField(upload_to='comment_image', blank=True)
    image2 = models.ImageField(upload_to='comment_image', blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    comment_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_likes')

    class Meta:
        ordering = ('created',)






