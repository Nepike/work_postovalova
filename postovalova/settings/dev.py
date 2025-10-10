from .base import *
import yaml
from telegram import Bot

LOG_PATH = BASE_DIR / 'logs'

CONFIG_PATH = BASE_DIR / 'config.yml'
with open(CONFIG_PATH) as f:
    SITE_CONFIG = yaml.safe_load(f.read())


SECRET_KEY = 'django-insecure-=co5+e^zqbmsc0q1*+y#!dpbbmf*_id45_4z&e9l5_&(h4i48m'
DEBUG = True

# ngrok http 8000
SITE_URL = 'https://ca3cf0e54110.ngrok-free.app'  # any ngrok url (for tg webhook)
CSRF_TRUSTED_ORIGINS = [
    SITE_URL,
]

ALLOWED_HOSTS = ['*']

STATIC_URL = 'static/'
STATIC_ROOT = 'static/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

TGBOT_TOKEN = SITE_CONFIG["telegram_bot"].get("token", None)

AKISMET_API_KEY = None