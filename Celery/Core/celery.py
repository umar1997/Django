from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
# core is the folder where settings.py is

app = Celery('Core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
# tasks.py file should be made because its dicovering tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))