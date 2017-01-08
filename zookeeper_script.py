#!/usr/bin/env python

"""
Deploying zookeeper and kafka to Google Compute Engine
"""
from subprocess import call

# install java
call(["apt-get", "update"])
call(["apt-get", "-y", "install", "default-jre"])

# download kafka 
KAFKA_FILE = "kafka_2.11-0.10.1.0.tgz"
KAFKA_LOCATION = "http://apache.stu.edu.tw/kafka/0.10.1.0/{file}".format(file=KAFKA_FILE)
KAFKA_SERVER_CONFIG = "server.properties.kafka_2.11-0.10.1.0" 
KAFKA_SERVER_CONFIG_LOCATION = "https://raw.githubusercontent.com/kkchuchu/kkchuchu.mushroom/master/config/{config}".format(config=KAFKA_SERVER_CONFIG)

os.system("wget " + KAFKA_LOCATION)

# untar package
os.system("tar -xzf kafka_2.11-0.10.1.0.tgz")

os.system("ln -s kafka_2.11-0.10.1.0 kafka")

# download kafka server.properties
os.system("wget " + KAFKA_SERVER_CONFIG_LOCATION)
os.system("mv " + KAFKA_SERVER_CONFIG + " ./kafka/config/server.properties")
os.system("./kafka/bin/zookeeper-server-stop.sh"])
os.system("./kafka/bin/zookeeper-server-start.sh -daemon ./kafka/config/zookeeper.properties")

os.system("./kafka/bin/kafka-server-stop.sh")
os.system("./kafka/bin/kafka-server-start.sh -daemon ./kafka/config/server.properties")
