from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'panel.settings')
app = Celery('panel')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'run-my-task-every-minute': {
        'task': 'order.tasks.min',
        'schedule': crontab(minute='*/1'),  # every minute
    },
}
app.conf.timezone = 'UTC'
app.autodiscover_tasks()