from django.contrib import admin
from .models import Profile


# Register your models here.
@admin.register(Profile)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'telegram_id', 'my_tags', 'my_jokbo']
