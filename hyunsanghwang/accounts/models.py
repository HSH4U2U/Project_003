from django.db import models
from django.conf import settings


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='사용자')
    email = models.CharField(blank=True, max_length=30, verbose_name='소식 받을 이메일')
    telegram_id = models.CharField(blank=True, max_length=30, verbose_name='소식 받을 텔레그램')
    my_tags = models.TextField(blank=True, verbose_name='내가 선택한 태그')
    my_jokbo = models.TextField(blank=True, verbose_name='내가 선택한 족보')
