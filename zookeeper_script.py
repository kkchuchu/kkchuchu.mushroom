#!/usr/bin/env python

"""
Deploying zookeeper to Google Compute Engine
"""

# download kafka 
wget http://apache.stu.edu.tw/kafka/0.10.1.0/kafka_2.11-0.10.1.0.tgz

# untar package
tar -xzf kafka_2.11-0.10.1.0.tgz

ln -s kafka kafka_2.11-0.10.1.0

cd kafka

# download server.config
wget 
