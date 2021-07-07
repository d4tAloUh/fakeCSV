release: python manage.py makemigrations && python manage.py migrate
web: gunicorn planeks.wsgi
worker: celery -A planeks.celery worker --loglevel=DEBUG