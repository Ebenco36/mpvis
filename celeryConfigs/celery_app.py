from celery import Celery

# Create a Celery instance
celery = Celery(
    'tasks',
    broker='pyamqp://user:password@rabbitmq:5672//',
    backend='rpc://',
)

# Include tasks from other modules
celery.config_from_object('celeryConfigs.celeryconfig')
