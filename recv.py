#!/usr/bin/env python
import pika,sys

# AMQP consumer test

rx = 0

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    global rx
    
    if body:
        rx += 1
        print " [%i] Received %r" % (rx,body,)
    else:
        sys.exit("done!")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='org-logs', durable=True)

channel.basic_consume(callback,
    queue='org-logs',
    no_ack=True)

channel.start_consuming()

