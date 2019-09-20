import os
import time
import requests
import yaml
from celery import Celery


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='start_job')
def start_job(user: str, session: int, conf_url: str) -> str:
    
    # Create the folder in the users_code storage
    code_basedir = "/storage/users_code/{}/{}".format(user, session)
    os.makedirs(code_basedir)
    # Download the conìfiguration file
    os.system("curl -o {}/{} {}".format(code_basedir,"config.yaml",conf_url))
    # Read the conf file
    conf = yaml.load(open(code_basedir+ "/config.yaml"), Loader=yaml.FullLoader)

    



