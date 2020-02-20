import sys
import os
import json
import configparser
from pathlib import Path


import pandas as pd
from elasticsearch import Elasticsearch, helpers


PROJECT_ROOT = Path('../')

ELASTICSEARCH_CONFIG_PATH = PROJECT_ROOT / Path('./config/scp_edge.conf')


class SCPConnector(object):

    def __init__(self, config_path=ELASTICSEARCH_CONFIG_PATH, timeout=60, host=None, port=9200, default_index='filebeat_dns_logs'):

        if host is None:
            config = configparser.ConfigParser()
            config.read(config_path)
            host = config['elasticsearch']['Host']
            self.elasticsearch_hosts = [host]
            self.port = config['elasticsearch']['Port']
        else:
            self.port = port
            self.elasticsearch_hosts = [host]

        self.timeout = timeout
        self.index = default_index
        self.scroll = "12h"
        self.size = 1000
        self.es = Elasticsearch(hosts=self.elasticsearch_hosts, port=self.port, timeout=self.timeout)

    def get_response_generator(self, query):
        res = helpers.scan(client=self.es, query=query, index=self.index, preserve_order=True, 
                           scroll=self.scroll, size=self.size)
        return res

    def get_top_records(self, query, top=100000):
        res = self.get_response_generator(query)
        return pd.DataFrame((next(res)['_source'] for i in range(top)))

