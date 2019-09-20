# Docker task worker with telegram interface


### Build & Launch

```bash
docker-compose up -d --build
```

This will start the Telegram bot, the Celery task manager as well as a [Flower](https://github.com/mher/flower) server for monitoring workers on port `5555`

To add more workers:
```bash
docker-compose up -d --scale worker=5 --no-recreate
```

To shut down:

```bash
docker-compose down
```


Task changes should happen in [queue/tasks.py](celery-queue/tasks.py) 

