import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptothreads.settings')
app = Celery('cryptothreads')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_db_daily': {
        'task': 'update_db',
        'schedule': crontab(hour='0')
    }
}