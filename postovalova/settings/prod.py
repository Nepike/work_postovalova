from .base import *
import yaml

LOG_PATH = BASE_DIR / 'logs'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} [{asctime}] {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} [{asctime}] {message}',
            'style': '{',
        },
        'exceptions': {
            'format': '{levelname} [{asctime}] {message}\n\n',
            'style': '{',
        },
    },
    'handlers': {
        'file-error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_PATH, 'error.log'),
            'formatter': 'exceptions',
        },
        'file-access': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_PATH, 'access.log'),
            'formatter': 'simple',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file-error', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['file-error'],
            'propagate': False,
        },
        'core.views': {
            'handlers': ['file-access', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'root': {
            'handlers': ['file-error', 'console'],
            'level': 'WARNING',
        },

    },
}


CONFIG_PATH = BASE_DIR / 'config.yml'
with open(CONFIG_PATH) as f:
    SITE_CONFIG = yaml.safe_load(f.read())


SECRET_KEY = SITE_CONFIG["secret_key"]
DEBUG = True

SITE_URL = 'https://nepike.ru'  # главный домен вместе с https://
CSRF_TRUSTED_ORIGINS = [
    SITE_URL,
]


ALLOWED_HOSTS = [
    '194.87.43.18',
    '127.0.0.1',
    'localhost',
    'nepike.ru',
    'nepike.online'
]

ADMINS = [
    ('POSTOVALOVA Administration', 'maxventilator@yandex.ru'),
]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STATIC_URL = 'static/'
STATIC_ROOT = 'static/'


RECAPTCHA_PUBLIC_KEY = SITE_CONFIG["recaptcha"]["public_key"]
RECAPTCHA_PRIVATE_KEY = SITE_CONFIG["recaptcha"]["private_key"]

AKISMET_API_KEY = SITE_CONFIG["akismet"]["api_key"]
AKISMET_BLOG_URL = SITE_CONFIG["akismet"]["blog"]


TGBOT_TOKEN = SITE_CONFIG["telegram_bot"].get("token", None)




