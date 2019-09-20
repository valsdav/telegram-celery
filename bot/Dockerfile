FROM python:3.6

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

ENV HOST 0.0.0.0
ENV PORT 5001
ENV DEBUG true

COPY ./requirements.txt .

# install requirements
RUN pip3 install -r requirements.txt

# expose the app port
EXPOSE 5001


# run the app server
CMD ["python", "/bot/bot.py"]