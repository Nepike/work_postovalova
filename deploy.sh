#!/bin/bash

# Путь к проекту
PROJECT_DIR=/srv/postovalova
VENV_DIR=$PROJECT_DIR/virtualenv

# Лог файл деплоя
LOGFILE=$PROJECT_DIR/deploy.log

echo "=== DEPLOY START: $(date) ===" >> $LOGFILE

cd $PROJECT_DIR || { echo "No project dir"; exit 1; }

# Выключаем gunicorn перед обновлением
sudo systemctl stop gunicorn

# Сброс локальных изменений и обновление из git
git reset --hard
git pull origin main

# Активируем виртуальное окружение и ставим зависимости
source $VENV_DIR/bin/activate
pip install -r requirements.txt

# Собираем статику (если нужно)
python manage.py collectstatic --noinput

# Миграции
python manage.py makemigrations
python manage.py migrate

# Запускаем gunicorn + deploy webhook
pm2 restart "gunicorn-postovalova"
pm2 restart deploy-postovalova

echo "=== DEPLOY END: $(date) ===" >> $LOGFILE
