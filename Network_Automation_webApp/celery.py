import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Network_Automation_webApp.settings')

app = Celery('Network_Automation_webApp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()