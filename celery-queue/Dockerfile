FROM python:3.6

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

COPY ./requirements.txt .

RUN pip install -r requirements.txt
 
WORKDIR /celery-queue

ENTRYPOINT celery -A tasks worker --uid=worker --loglevel=info