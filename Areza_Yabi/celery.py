# Areze_yab/Areze_Yabi/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Areza_Yabi.settings')

app = Celery('Areza_Yabi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
