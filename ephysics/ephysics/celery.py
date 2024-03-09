import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ephysics.settings')

# Create a Celery instance.
app = Celery('ephysics', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Specify the working directory
app.conf.update(
    workdir='/mnt/c/Users/Galaxy Book Ion/Documents/GitHub/Advanced-Web-Dev-Final/ephysics'
)
# Auto-discover tasks in all apps.
app.autodiscover_tasks()