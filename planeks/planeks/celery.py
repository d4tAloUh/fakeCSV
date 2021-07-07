import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planeks.settings')

app = Celery('generator', namespace='CELERY')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
