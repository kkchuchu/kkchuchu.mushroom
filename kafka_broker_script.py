#!/usr/bin/env python

"""
Deploying kafka to Google Compute Engine
requirement:
- ubuntu 16.04 LTS
- 1 CPU
- 3.75 GB Mem
- Kafka version is 2.11-0.10.1.0
"""
from subprocess import call
import sys, os

# install java
os.system("apt-get update")
os.system("apt-get -y install default-jre")

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

server_url = sys.argv[1]
broker_id = sys.argv[2]
with open(KAFKA_SERVER_CONFIG) as ramp:
    with open("./kafka/config/server.properties", "w+") as sink:
        for line in ramp:
            url_parameter = "{SERVER_URL}"
            id_parameter = "{BROKER_ID}"
            if url_parameter  in line:
                line = line.replace(url_parameter, server_url)
                sink.write(line + "\n")
            if id_parameter in line:
                line = line.replace(id_parameter, broker_id)
                sink.write(line + "\n")

os.system("./kafka/bin/kafka-server-stop.sh")
os.system("./kafka/bin/kafka-server-start.sh -daemon ./kafka/config/server.properties")
