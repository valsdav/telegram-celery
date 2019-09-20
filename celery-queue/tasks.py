import os
import time
import requests
import yaml
from celery import Celery


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='start_job')
def start_job(conf_url: str) -> str:
    
    # Download the conìfiguration file
    os.system("curl -o {} {}".format("./test.yaml",conf_url))
    # Read the conf file
    conf = yaml.load(open("./test.yaml","r"), Loader=yaml.FullLoader)

    



