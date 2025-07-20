import os
import ssl
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gemini_backend.settings')

app = Celery('gemini_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Add SSL settings for Redis
app.conf.broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE
}
app.conf.redis_backend_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE
}
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
