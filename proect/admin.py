from django.contrib import admin
from .models import CategoryMinors, Minor, Proect

@admin.register(Proect)
class ProectTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Minor)
class MinorTypeAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(CategoryMinors)
class CategoryMinorsAdmin(admin.ModelAdmin):
    list_display = ['name']

