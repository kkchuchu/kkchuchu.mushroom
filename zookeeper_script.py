#!/usr/bin/env python

"""
Deploying zookeeper to Google Compute Engine
"""
from subprocess import call
# download kafka 
KAFKA_LOCATION = "http://apache.stu.edu.tw/kafka/0.10.1.0/kafka_2.11-0.10.1.0.tgz"
KAFKA_SERVER_CONFIG_LOCATION = "https://raw.githubusercontent.com/kkchuchu/kkchuchu.mushroom/master/config/server.properties.kafka_2.11-0.10.1.0"

call(["wget", KAFKA_LOCATION])

# untar package
call(["tar", "-xzf", "kafka_2.11-0.10.1.0.tgz"])

call(["ln", "-s", "kafka", "kafka_2.11-0.10.1.0"])

cd kafka/config

# download kafka server.properties
call(["wget", KAFKA_SERVER_CONFIG_LOCATION])
call(["./kafka/bin/zookeeper-server-stop.sh"])
call(["./kafka/bin/zookeeper-server-start.sh", "--daemon", "./kafka/config/zookeeper.properties"])

call(["./kafka/bin/kafka-server-stop.sh"])
call(["./kafka/bin/kafka-server-start.sh --daemon config/server.properties"])
