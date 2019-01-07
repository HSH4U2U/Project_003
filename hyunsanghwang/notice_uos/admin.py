from django.contrib import admin
from .models import Notice


# Register your models here.
@admin.register(Notice)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['seq', 'sort', 'title', 'url', 'tags']
