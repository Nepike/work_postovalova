
# 1. TODO
- полировка админки




# 2. Как поднять сайт у себя?
## 2.1 Зависимости
- Python 3.11+

## 2.2 Ubuntu 20.04 + 2.3 Windows 10

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


3. Как настроить удаленный сервер с автодеплоем

3.1 Лучше создать отдельного пользователя для операции над каждым сайтом


__DOMEN__ = olgapostovalova.ru
__GITHUB__ = https://github.com/Nepike/work_postovalova
__PROJECT__ = postovalova

```bash
adduser user-__DOMEN__

sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv python3-dev libpq-dev nginx git -y

cd ~
git clone __GITHUB__ __PROJECT__
cd __PROJECT__

python3 -m venv virtualenv
. virtualenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

#/etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon for Django project
After=network.target

[Service]
User=maxve
Group=www-data
WorkingDirectory=/home/maxve/post
ExecStart=/home/maxve/post/virtualenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/maxve/post/gunicorn.sock --umask 007 post.wsgi:application

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

#/etc/nginx/sites-available/post
server {
    listen 80;
    server_name <ваш_IP_или_домен>;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/maxve/post/static/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/maxve/post/gunicorn.sock;
    }
}

sudo ln -s /etc/nginx/sites-available/post /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Дать право заходить в домашнюю папку maxve (выполнение для всех)
chmod 711 /home/maxve

# Дать права на папку проекта, если нужно
chmod 755 /home/maxve/post

# Дать права на сокет (в gunicorn.service можно добавить параметр --umask=007)
sudo chown maxve:www-data /home/maxve/post/gunicorn.sock
sudo chmod 660 /home/maxve/post/gunicorn.sock


#deploy.sh
#!/bin/bash
echo "Deploy started at $(date)" >> /home/maxve/post/deploy.log
cd /home/maxve/post || exit
git pull origin main
# Добавьте сюда любые другие команды, например, миграции, сборки и перезапуск серверов

git update-index --chmod=+x deploy.sh
git commit -m "Make deploy.sh executable"
git push


#webhook_listener.py
#!/usr/bin/env python3
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Запускаем deploy.sh через bash, чтобы избежать проблем с правами
    subprocess.Popen(['/bin/bash', '/home/maxve/post/deploy.sh'])
    return "Deploy triggered", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


cd /home/maxve/post
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install flask
deactivate

#/etc/systemd/system/webhook.service
[Unit]
Description=GitHub webhook listener for Django deploy
After=network.target

[Service]
User=maxve
WorkingDirectory=/home/maxve/post
ExecStart=/home/maxve/post/virtualenv/bin/python /home/maxve/post/webhook_listener.py
Restart=always

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl enable webhook.service
sudo systemctl start webhook.service
sudo systemctl status webhook.service

#/etc/nginx/sites-available/webhook
server {
    listen 80;
    server_name your_domain_or_ip;

    location /webhook {
        proxy_pass http://127.0.0.1:5000/webhook;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

sudo ln -s /etc/nginx/sites-available/webhook /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```
