# Лучше выполнять все команды только вручную (велик риск, что что-то пойдет по пиZOVде)

# Переменные
MAIN_DOMEN=nepike.ru
SIDE_DOMEN=nepike.online # Other side domains are configured similarly.
GITHUB=https://github.com/Nepike/work_postovalova
PROJECT=postovalova
USER=user_postovalova
PARENT_DIR=/srv

# Создаем пользователя и устанавливаем зависимости
sudo adduser --disabled-password --gecos "" $USER
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv python3-dev libpq-dev nginx git curl -y
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2
sudo mkdir -p ${PARENT_DIR}/${PROJECT}
sudo chown ${USER}:${USER} ${PARENT_DIR}/${PROJECT}

# Развертываем Django
sudo -u $USER bash -c "
cd $PARENT_DIR
git clone $GITHUB $PROJECT
cd $PROJECT
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
sudo -u $USER pm2 delete gunicorn-${PROJECT} 2> /dev/null
sudo -u $USER pm2 start "gunicorn" \
    --name "gunicorn-${PROJECT}" \
    --interpreter ${PARENT_DIR}/${PROJECT}/virtualenv/bin/python \
    --env DJANGO_SETTINGS_MODULE=${PROJECT}.settings.prod \
    -- \
    --workers 3 \
    --worker-class gthread \
    --threads 2 \
    --bind unix:${PARENT_DIR}/${PROJECT}/gunicorn.sock \
    --chdir ${PARENT_DIR}/${PROJECT} \
    --log-file - \
    --access-logfile ${PARENT_DIR}/${PROJECT}/logs/gunicorn_access.log \
    --error-logfile - \
    ${PROJECT}.wsgi:application
sudo -u $USER pm2 save
sudo -u $USER pm2 status

# Настройка вебхука
sudo -u $USER pm2 delete deploy-${PROJECT} 2> /dev/null
sudo -u $USER pm2 start "${PARENT_DIR}/${PROJECT}/virtualenv/bin/python" \
    --name "deploy-${PROJECT}" \
    -- ${PARENT_DIR}/${PROJECT}/webhook_listener.py
sudo -u $USER pm2 save

# Настройка Nginx
sudo tee /etc/nginx/sites-available/${PROJECT} > /dev/null <<EOL
server {
    listen 80;
    server_name $MAIN_DOMEN;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias ${PARENT_DIR}/${PROJECT}/static/;
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
        proxy_pass http://unix:${PARENT_DIR}/${PROJECT}/gunicorn.sock;
    }
}
EOL

sudo ln -s /etc/nginx/sites-available/${PROJECT} /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Автозапуск PM2 при перезагрузке
sudo env PATH=\$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u $USER --hp /home/$USER
sudo -u $USER pm2 save


# SSL(только если есть домен кароч)
sudo apt install certbot python3-certbot-nginx -y

# Этот пункт надо делать вручную тк Certbot запрашивает email и принятие EULA
sudo certbot certonly --nginx -d ${MAIN_DOMEN} -d ${SIDE_DOMEN} # Other side domains enumeration here

sudo tee /etc/nginx/sites-available/${PROJECT} > /dev/null <<EOL
# Главный домен (HTTPS)
server {
    listen 443 ssl;
    server_name ${MAIN_DOMEN};

    ssl_certificate /etc/letsencrypt/live/${MAIN_DOMEN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${MAIN_DOMEN}/privkey.pem;
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
    server_name ${MAIN_DOMEN};
    return 301 https://$host$request_uri;
}


# Редиректы с побочных доменов на главный
server {
    listen 80;
    listen 443 ssl;
    server_name ${SIDE_DOMEN};

    ssl_certificate /etc/letsencrypt/live/${MAIN_DOMEN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${MAIN_DOMEN}/privkey.pem;

    return 301 https://${MAIN_DOMEN}$request_uri;
}
EOL

sudo nginx -t && sudo systemctl reload nginx
