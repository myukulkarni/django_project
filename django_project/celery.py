# django_project/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')  # replace with your project name

app = Celery('django_project')  # replace with your project name
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
