# Лучше выполнять все команды только вручную (велик риск, что что-то пойдет по пиZOVде)

# Переменные
MAIN_DOMEN=nepike.ru
SIDE_DOMEN=nepike.online # Other side domains are configured similarly.
GITHUB=https://github.com/Nepike/work_postovalova
PROJECT=postovalova
USER=user_postovalova
PARENT_DIR=/srv

# Создаем пользователя и устанавливаем зависимости
sudo adduser --disabled-password --gecos "" user_postovalova
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv python3-dev libpq-dev nginx git curl -y
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2
sudo mkdir -p /srv/postovalova
sudo chown user_postovalova:user_postovalova /srv/postovalova

# Развертываем Django
sudo -u user_postovalova bash -c "
cd /srv
git clone https://github.com/Nepike/work_postovalova postovalova
cd postovalova
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
mkdir -p logs
mv config_sample.yml config.yml
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
"

# Настройка Gunicorn под PM2
sudo -u user_postovalova -i
pm2 delete gunicorn-postovalova 2> /dev/null
pm2 start "gunicorn" \
    --name "gunicorn-postovalova" \
    --interpreter /srv/postovalova/virtualenv/bin/python \
    --env DJANGO_SETTINGS_MODULE=postovalova.settings.prod \
    -- \
    --workers 3 \
    --worker-class gthread \
    --threads 2 \
    --bind unix:/srv/postovalova/gunicorn.sock \
    --chdir /srv/postovalova \
    --log-file - \
    --access-logfile /srv/postovalova/logs/gunicorn_access.log \
    --error-logfile - \
    postovalova.wsgi:application
pm2 save
pm2 status

# Настройка вебхука
sudo -u user_postovalova pm2 delete deploy-postovalova 2> /dev/null
sudo -u user_postovalova pm2 start "/srv/postovalova/virtualenv/bin/python" \
    --name "deploy-postovalova" \
    -- /srv/postovalova/webhook_listener.py
sudo -u user_postovalova pm2 save

# Настройка Nginx
sudo tee /etc/nginx/sites-available/postovalova > /dev/null <<EOL
server {
    listen 80;
    server_name nepike.ru;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /srv/postovalova/static/;
    }

    location /deploy_webhook {
        proxy_pass http://0.0.0.0:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/srv/postovalova/gunicorn.sock;
    }
}
EOL

sudo ln -s /etc/nginx/sites-available/postovalova /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Автозапуск PM2 при перезагрузке
sudo env PATH=\$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u user_postovalova --hp /home/user_postovalova
sudo -u user_postovalova pm2 save


# SSL(только если есть домен кароч)
sudo apt install certbot python3-certbot-nginx -y

# Этот пункт надо делать вручную тк Certbot запрашивает email и принятие EULA
sudo certbot certonly --nginx -d nepike.ru -d nepike.online # Other side domains enumeration here

sudo tee /etc/nginx/sites-available/postovalova > /dev/null <<EOL
# Главный домен (HTTPS)
server {
    listen 443 ssl;
    server_name nepike.ru;

    ssl_certificate /etc/letsencrypt/live/nepike.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nepike.ru/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /srv/postovalova/static/;
    }

    location /deploy_webhook {
        proxy_pass http://0.0.0.0:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/srv/postovalova/gunicorn.sock;
    }

}


# HTTP -> HTTPS редирект главного домена
server {
    listen 80;
    server_name nepike.ru;
    return 301 https://$host$request_uri;
}


# Редиректы с побочных доменов на главный
server {
    listen 80;
    listen 443 ssl;
    server_name nepike.online;

    ssl_certificate /etc/letsencrypt/live/nepike.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nepike.ru/privkey.pem;

    return 301 https://nepike.ru$request_uri;
}
EOL

sudo nginx -t && sudo systemctl reload nginx
