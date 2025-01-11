from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'panel.settings')
app = Celery('panel')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-my-daily-task': {
        'task': 'order.tasks.my_daily_task',
        'schedule': crontab(hour=0, minute=0),  # every day at midnight
    },
    'run-my-weekly-task': {
        'task': 'order.tasks.send_weekly_orders',
        'schedule': crontab(day_of_week='saturday', hour=18, minute=58),  # every friday at midnight
    },
}
app.conf.timezone = 'UTC'
