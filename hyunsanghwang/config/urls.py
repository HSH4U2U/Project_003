from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notice_uos/', include('notice_uos.urls')),
    path('schedule_google/', include('schedule_google.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)