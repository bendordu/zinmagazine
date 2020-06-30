from django.contrib import admin
from .models import Profile, CategoryProfile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

@admin.register(CategoryProfile)
class CategoryProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']