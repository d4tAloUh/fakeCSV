release: python manage.py makemigrations && python manage.py migrate --no-input
web: gunicorn planeks.wsgi
worker: celery -A planeks.celery worker --loglevel=DEBUG