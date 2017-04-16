from __future__ import absolute_import

import os, sys
import argparse

from kafka import KafkaProducer, KafkaConsumer

from runnable import Runnable, ArgumentHandler

TOPIC = 'prm-test'
BOOTSTRAPSERVER = '104.199.234.41:9092'
CONSUMER_GROUP_ID = 'PRM-demo'


class FMArgumentHandler(ArgumentHandler):
    def __init__(self, *args, **kwargs):
        super(FMArgumentHandler, self).__init__(*args, **kwargs)
        self._parser.add_argument('-file', help='producer comma csv file location')
        self._parseargs()

class FM(Runnable):
    def producer(self):
        """
        Import type: csv file with comma 
        """
        file_path = self._arguments.file
        assert file_path is not None, 'No provide producer file path'
        producer = KafkaProducer(bootstrap_servers=BOOTSTRAPSERVER)
        with open(file_path) as f:
            for line in f:
                producer.send(TOPIC, line)
        producer.flush()

    def consumer(self):
        consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAPSERVER)
        consumer.subscribe(topics=(TOPIC))
        for msg in consumer:
            print msg.value, msg.topic, msg.partition, msg.offset, msg.key


if __name__ == '__main__':
    args = FMArgumentHandler(sys.argv)
    fm = FM(args.arguments)
    eval("fm.{0}()".format(fm._arguments.producer_consumer))


