# celeryconfig.py

broker_url = 'pyamqp://user:password@rabbitmq:5672//'
result_backend = 'rpc://'
timezone = 'UTC'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
