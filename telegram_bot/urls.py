from django.conf import settings
from django.urls import path
from .views import webhook

urlpatterns = [
    path(f'webhook/{settings.TGBOT_TOKEN}', webhook, name='webhook'),
]