The configuration and test scripts in this directory enable an engineer to construct a centralized log 
messaging pipeline, from event formatting and generation to aggregation, filtering, search and reporting.

The current test rig consists of the following:

1. Event generation: Log4net, Log4j and Python Log Event Generation.   CEE-standard events are encoded in JSON
syntax.  A log4(x) appender encapsulates the CEE/JSON event in an AMQP topic stream which is forwarded to an
AMQP exchange broker.

2. The AMQP event stream from each appender is sent to a RabbitMQ topic exchange as "org.<infosystem>.<severity>" which is then subscribed to by the aggregator/filter.

3. LogStash acts as the aggregator/filter and protocol translator to the backend.  LogStash is configurable
to accept inputs from approximately 10 different source types and output the events to about the same number
of outputs.  In this case LogStash uses an AMQP input and subscribes to event topics (eg: org.myapp.WARN)
and waits for the events in JSON format.   The events can be filtered if necessary and are then forwarded
(output) to the backend database / reporting tool. 

4. ElasticSearch is the backend.  ElasticSearch accepts each CEE/JSON event, indexes every contained keyword
and makes it available for REST-based queries (HTTP GET).  The result sets are JSON objects that can be
used with any reporting tool or website.  ElasticSearch can be deployed on a single server, or can be
deployed in a cluster which autodisover each other and participate in indexing and searching.  LogStash offers
a simple web application to generate ElasticSearch queries and display the output.

This represents the entire log chain from generation to reporting.

This modular architecture allows an organization to deploy a minimal, but powerful system and replace 
components with point solutions as time, budget or needs allow.

Please read the INSTALL.txt file for the software and test components that are required to be installed
and configured to start up the test rig.

5. The AMQP appender test requires the pika Python AMQP library



