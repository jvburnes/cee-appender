#!/bin/sh
java -jar logstash-1.0.17-monolithic.jar agent -f indexer.conf -- web

