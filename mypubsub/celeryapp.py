# from __future__ import absolute_import, unicode_literals

import os
import kombu
from celery import Celery, bootsteps

from utils.twilio import notify_twilio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypubsub.settings')

app = Celery('weather_notify')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='weather_exchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()

    sfqueue = kombu.Queue(
        name='sfqueue',
        exchange=exchange,
        routing_key='sfkey',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    sfqueue.declare()
    
    nyqueue = kombu.Queue(
        name='nyqueue',
        exchange=exchange,
        routing_key='nykey',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    nyqueue.declare()



class SFConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [kombu.Consumer(channel,
                               queues=[sfqueue],
                               callbacks=[self.handle_message],
                               accept=['json'])]

    def handle_message(self, body, message):
            print('Received message on Channel_1: {0!r}'.format(body))
            notify_twilio(data = body['weather_data'], phone_number=body['phone_number'])
            message.ack()
        
app.steps['consumer'].add(SFConsumerStep)



class NYConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [kombu.Consumer(channel,
                               queues=[nyqueue],
                               callbacks=[self.handle_message2],
                               accept=['json'])]

    def handle_message(self, body, message):
            print('Received message on Channel_2: {0!r}'.format(body))
            try: 
                print("Message forwarded")
                notify_twilio(data = body['weather_data'], phone_number=body['phone_number'])               
                message.ack()
            except Exception as e:
                print(e)
                return None

app.steps['consumer'].add(NYConsumerStep)