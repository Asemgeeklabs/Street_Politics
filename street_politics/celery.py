import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','street_politics.settings')

## instnce of celery application ##
app = Celery('street_politics')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()