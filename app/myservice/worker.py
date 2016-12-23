import os
from celery import Celery


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL',
                                   'amqp://guest@localhost:5672//')

celery_worker = Celery('thumb_worker', broker=CELERY_BROKER_URL)
