from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZelfHack1.settings')

app = Celery('ZelfHack1')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.timezone = 'Asia/Dhaka'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.result_backend = 'django-db'

# app.conf.beat_schedule = {
#     'daily_update_posts': {
#         'task': 'api.utils.tasks.daily_update_posts',
#         'schedule': crontab(hour=13, minute=00),  # Runs daily at midnight
#     },
# }