@echo off
python manage.py makemigrations --settings=config.settings.local
python manage.py migrate --settings=config.settings.local