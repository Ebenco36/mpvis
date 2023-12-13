from celery_app import celery
import time

@celery.task
def add(x, y):
    time.sleep(5)  # Simulate a time-consuming task
    return x + y
