##!/usr/bin/bash
#
#script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#
## Change to that directory
#cd "$script_dir"
#
#PYTHON_EXEC="../v/bin/python"
#CELERY_EXEC="../v/bin/celery"
#
## TODO: make backup
#
#touch ../maintenance
#
#sudo systemctl stop knt-mipt.ru-uwsgi.service
#
#export STATIC_VERSION=$(date +%s)
#echo "STATIC_VERSION=$STATIC_VERSION" > ../.env
#
#
#git pull origin main
#$PYTHON_EXEC -m pip install -r requirements.txt
#$PYTHON_EXEC manage.py makemigrations
#$PYTHON_EXEC manage.py migrate
#$PYTHON_EXEC manage.py set_telegram_webhook
#$PYTHON_EXEC manage.py collectstatic --noinput -v 0
#
##pkill -f "celery -A knt worker"
##$CELERY_EXEC -A knt worker --loglevel=info --detach
#
#sudo systemctl start knt-mipt.ru-uwsgi.service
#
#rm ../maintenance
