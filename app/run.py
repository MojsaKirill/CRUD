import time

from celery import Celery

app = Celery(__name__)
app.conf.broker_url = 'redis://172.16.100.227:6379/0'
app.conf.result_backend = 'redis://172.16.100.227:6379/0'


@app.task(name='create_task')
def create_task(a, b, c):
    time.sleep(a)
    return b + c
