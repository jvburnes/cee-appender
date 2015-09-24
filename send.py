#!/usr/bin/env python
import pika

# AMQP send test
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='org-logs', durable=True)

# create a persistant property
persist =   properties=pika.BasicProperties(delivery_mode = 2)

# send 12k persistant messages to a durable queue
for i in xrange(1,12000):
    channel.basic_publish(exchange='',routing_key='org-logs', body='Hello World!', properties=persist)

# send an end-of-stream msg
channel.basic_publish(exchange='',routing_key='org-logs', body='')

print " [x] Sent 12000 'Hello World!' messages"

connection.close()

