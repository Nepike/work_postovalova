
# 1. TODO
- полировка админки




# 2. Как поднять сайт у себя?
## 2.1 Зависимости
- Python 3.11+

## 2.2 Ubuntu 20.04 + 2.3 Windows 10

Клонировать репозиторий:
```bash
# Клонирование репозитория
git clone https://github.com/Nepike/work_postovalova post


# Переход в папку с проектом
cd post

# Создание и активация виртуального окружения Python
python3 -m venv virtualenv
. virtualenv/bin/activate

# Установка нужных пакетов Python
pip install -r requirements.txt

# Создание файла конфигурации
cp config_sample.yml config.yml

# Миграции
python manage.py makemigrations
python manage.py migrate
python manage.py set_telegram_webhook

# Запуск сервера:
python manage.py runserver

```
