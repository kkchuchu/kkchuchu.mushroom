import sys
import os
import json
import configparser
from pathlib import Path

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, scoped_session


import pandas as pd
from elasticsearch import Elasticsearch, helpers


class ESConnector(object):

    def __init__(self, config: dict, timeout=60, default_index=None):
        """[summary]

        Arguments:
            config {dict} -- {'host': '', 'port': 9200}

        Keyword Arguments:
            timeout {int} -- [description] (default: {60})
            default_index {[type]} -- [description] (default: {None})
        """
        host = config['host']
        self.elasticsearch_hosts = [host]
        self.port = config['port']
        self.timeout = timeout
        self.index = default_index
        self.scroll = "1h"
        self.size = 1000
        self.es = Elasticsearch(
            hosts=self.elasticsearch_hosts, port=self.port, timeout=self.timeout)

    def get_response_generator(self, query):
        res = helpers.scan(client=self.es, query=query, index=self.index, preserve_order=True,
                           scroll=self.scroll, size=self.size)
        return res

    def get_top_records(self, query, top=100000):
        res = self.get_response_generator(query)
        return pd.DataFrame((next(res)['_source'] for i in range(top)))


class ConnectionStringGenerator(object):

    def __init__(self, account, password, host, port, database):
        self._account = account
        self._password = password
        self._host = host
        self._port = port
        self._database = database

    def get_postgresql_psycopg2(self):
        return 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (
            self._account,
            self._password,
            self._host,
            self._port,
            self._database)
        
    def get_sqlite(self):
        pass
    
    def get_mysql(self):
        pass


class SQLDBConnector(object):

    def __init__(self, connection_str, autocommit=False, autoflush=False, pool_size=5, pool_recycle=7200, pool_timeout=7200):
        self.engine = create_engine(connection_str,
                                    pool_size=pool_size,
                                    pool_recycle=pool_recycle,
                                    pool_timeout=pool_timeout)

        self.db_session = scoped_session(sessionmaker(
            autocommit=autocommit, autoflush=autoflush, bind=engine))

    def getSession(self):
        return self.db_session

    def closeSession(self):
        return self.db_session.close()

    def __enter__(self):
        return self.getSession()

    def __exit__(self, type, value, traceback):
        self.db_session.commit()
        self.closeSession()

    def raw_sql(self, sql_statement):
        statement = text(sql_statement)
        con = self.engine.connect()
        rows = con.execute(statement)
