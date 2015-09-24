#!/usr/bin/env python

# AMQP Python Logging Handler Example
import logging
import pika
import os, uuid, logging, pika
from   ceeEvent import CEEEvent

from time import time, strftime, localtime

my_uuid = str(uuid.uuid1())

def amqpTopicChannel(p_exchange,host='localhost',port=5672,virtual_host='/',username='guest',password='guest'):
        connectionParams = pika.ConnectionParameters(credentials=pika.PlainCredentials(username,password),host='localhost')
        connection = pika.BlockingConnection(connectionParams)
        channel = connection.channel()
        channel.exchange_declare(exchange=p_exchange,type='topic',durable=True)
        return channel

class Producer():
    def __init__(self,exchange):
        self.exchange = exchange
        self.channel = amqpTopicChannel(self.exchange,host='localhost',username='guest',password='guest')

    def message(self, record):
        # if topic key isn't specified, we use the severity level
        if self.topic_key:
            self.topic = self.base_topic + self.topic_key
        else:
            self.topic = self.base_topic + record.levelname

        # do it
        self.channel.basic_publish(exchange=self.exchange,routing_key=self.topic,body=record.getMessage())

#class Consumer():
#    def __init__(self, callback_function=None):
#        self.channel = setup_amqp('r',queue_name="logger_"+my_uuid)
#        self.callback_function = callback_function
    
#    def callback(self, msg):
#        message = pickle.loads(msg.body)
#        if(self.callback_function):
#            self.callback_function(message)

#    def consume_forever(self):
#        self.ch.basic_consume("logger_"+my_uuid, callback=self.callback, no_ack=True)
#        while self.ch.callbacks:
#            self.ch.wait()

#    def close(self):
#        self.ch.close()


class AMQP_Handler(logging.Handler):
    def __init__(self,exchange):
        self.broadcaster = Producer(exchange)
        self.level = 0
        self.filters = []
        self.lock = 0
        #self.machine = os.uname()[1]

    def emit(self, record):
        # Send the log message to the broadcast queue
        #message = {"source":"logger","machine":self.machine, "message":record.msg % record.args, "level":record.levelname, "pathname":record.pathname, "lineno":record.lineno, "exception":record.exc_info}
        # other messages create the final message at the broadcaster.  We've already created it.
        self.broadcaster.message(record)

def SetupAMQPHandler(logger,exchange,base_topic,topic_key=None):
    "Factory function for a logging.StreamHandler instance connected to your namespace."
    amqpHandler = AMQP_Handler(exchange)
    bcast = amqpHandler.broadcaster
    bcast.base_topic = base_topic
    bcast.topic_key = topic_key

    logger.addHandler(amqpHandler)


# Do the test

# create a logger
logger = logging.getLogger('org.test')  # org.test namespace unrelated to AMQP
logger.setLevel(logging.INFO)

# configure it for AMQP
SetupAMQPHandler(logger,exchange='org.logs.topics',base_topic='org.')

# log a couple CEE events.  these events automagically get the default baseline settings /w timestamp
# they are routed according to the specified topic
# they are rendered with the default CEE JSON syntax (spec'd by __str__ for CEEEvent)

# The following examples use the autopopulation and initialization options of the CEE event constructor.   
# If logging in a relatively tight loop, create the log event and set the fields manually, eg:
# newev = CEEEvent(id='itc_system', p_prod_id='linux_kern')
# while k.inode == 0:
#   newev.fields.text = "kernel: filesystem 'usr-host-1f377c21' inodes exhuasted"
#   newev.fields.action = 'allocate'
#   newev.fields.status = 'failure'
#   logger.critical(newev)
#   yield 1
#
# CEEEvent can be constructed with a "use_fields = <fieldgroup> + <fieldgroup> .."
# to prepopulate it with common system and application logging fields.
# Please see the files ceeFields.py and ceeEvent.py for further documentation

logger.warn(CEEEvent(text="kernel: filesystem 'usr-host-1f377c21' 5% inodes remaining",id="org_storagewarn",action='allocate',status='success'))
logger.critical(CEEEvent(text="kernel: filesystem 'usr-host-1f377c21' inodes exhuasted",id="org_storagewarn",p_prod_id="linux_kern",action='allocate',status='failure'))

# Do that using field manipulation

# autopopulate and mark with current timestamp
newev = CEEEvent(id='org_storagewarn', p_prod_id='linux_kern')

# send out the warning
newev.field.action = 'allocate'
newev.field.status = 'success'
newev.field.text = "kernel: filesystem 'usr-host-8f397c21' 5% inodes remaining"
logger.warn(newev)

# send out the failure (still an attempted 'allocate')
# change values
newev.field.status = 'failure'
newev.field.text = "kernel: filesystem 'usr-host-8f397c21' inodes exhuasted"
# apply the current timestamp
newev.mark()    
logger.critical(newev)
