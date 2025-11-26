from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'bot'


urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
    path('set-webhook/', views.set_webhook_view, name='set_webhook'),
    path('webhook-info/', views.webhook_info_view, name='webhook_info'),
    path('health/', views.health_check, name='health'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)