from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from django.urls import reverse


class Command(BaseCommand):
    help = 'Устанавливает вебхук Telegram бота'

    def handle(self, *args, **kwargs):
        if not settings.TGBOT_TOKEN:
            self.stdout.write(self.style.ERROR('TG TOKEN NOT FOUND'))
            return

        webhook_url = f'{settings.SITE_URL}{reverse("webhook")}'
        url = f'https://api.telegram.org/bot{settings.TGBOT_TOKEN}/setWebhook'
        data = {'url': webhook_url}

        response = requests.post(url, data=data)
        if response.status_code == 200:
            description = response.json().get("description", "")
            self.stdout.write(self.style.SUCCESS(f'Webhook установлен: {webhook_url} ({description})'))
        else:
            self.stdout.write(self.style.ERROR(f'Не удалось установить webhook ({response.status_code})'))
