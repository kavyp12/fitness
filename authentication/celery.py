import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gfg.settings')

# Define the Celery app.
app = Celery('gfg')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all Django apps.
app.autodiscover_tasks()

# Run the Celery app.



