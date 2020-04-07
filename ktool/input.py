import sys
import os
import json
import configparser
from pathlib import Path
import urllib
import pandas
import datetime
import logging


from joblib import dump, load
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base


import pandas as pd
from elasticsearch import Elasticsearch, helpers

from ktool.util import NotSupportedError, TS

logger = logging.getLogger("jupyter")


class BaseConnector(object):

    def __init__(self, timeout=30):
        self.timeout = timeout
        
    def read(self, path):
        pass
    
    def dump(self, df, path):
        pass


class ESConnector(BaseConnector):

    def __init__(self, host, port=9200, timeout=60, default_index=None):
        self.elasticsearch_hosts = [host]
        self.port = port
        self.timeout = timeout
        self.index = default_index
        self.scroll = "1h"
        self.size = 1000
        self.es = Elasticsearch(
            hosts=self.elasticsearch_hosts, port=self.port, timeout=self.timeout)

    def get_response_generator(self, query, index):
        if index is None:
            index = self.index
        res = helpers.scan(client=self.es, query=query, index=index, preserve_order=True,
                           scroll=self.scroll, size=self.size)
        return res

    def get_top_records(self, query, top=100000, index=None):
        res = self.get_response_generator(query, index)
        return pd.DataFrame((next(res)['_source'] for i in range(top)))
    
    def search(self, query, index=None):
        """ agg example:
        ddos_query = {
            "query": {
                "query_string" : {
                    "query" : "trailName:*DDOS* AND proto:udp AND type:session",
                }
            },
            "size": 0,
            "aggs": {
                "event_histogram": {
                    "date_histogram": {
                        "field": "lastPacket",
                        "interval": "1h",
                    },  
                },
            }
        }
        Get result from
        res['aggregations']['event_histogram']['buckets']
        Arguments:
            query {[string]} -- agg type.
        
        Keyword Arguments:
            index {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        res = self.es.search(body=query, index=index)
        return res


class ConnectionStringGenerator(object):

    def __init__(self, account, password, host, port, database):
        self._account = account
        self._password = password
        self._host = host
        self._port = str(port)
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


class SQLDBConnector(BaseConnector):

    def __init__(self, connection_str, autocommit=False, autoflush=False, pool_size=5, pool_recycle=7200, pool_timeout=7200,
                 auto_map=False, auto_map_tables=None):
        self.engine = create_engine(connection_str,
                                    pool_size=pool_size,
                                    pool_recycle=pool_recycle,
                                    pool_timeout=pool_timeout)

        if auto_map:
            Base = automap_base()
            metadata = MetaData()
            metadata.reflect(self.engine, only=auto_map_tables)
            Base = automap_base(metadata=metadata)
            Base.prepare()
            self.Base = Base
            # Account = Base.classes.account
            
        self.db_session = scoped_session(sessionmaker(
            autocommit=autocommit, autoflush=autoflush, bind=self.engine))
        

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
        return rows
    
    def get_df(self, sql_statement, columns:list=None):
        return pd.read_sql(sql_statement, con=self.engine)
    
    def read(self, sql_statement, columns:list=None):
        rows = self.raw_sql(sql_statement)
        return pd.DataFrame(rows, columns=columns)


class ServiceConnector(BaseConnector):

    def __init__(self, host):
        self.host = host
        super().__init__()

    def get(self, uri, **kwargs):
        full_url = (self.host + uri).format(**kwargs)
        response = urllib.request.urlopen(full_url, timeout=self.timeout)
        return json.loads(response.read().decode('utf-8'))


class SparkConnector(BaseConnector):
    
    def __init__(self, jars, master_url, app_name, sys_path, timeout=30, 
                 Serializer="org.apache.spark.serializer.KryoSerializer", 
                 RDDInputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
                 RDDKeyClass="org.apache.hadoop.io.NullWritable",
                 RDDValueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
                 ):
        super().__init__(timeout=timeout)
        
        
class FileConnector(BaseConnector):
    
    def __init__(self, folder_path=None):
        super().__init__()
        self.folder_path = Path(folder_path)
        self._create_folder_without_error(self.folder_path)
        logger.debug("create folder: %r", self.folder_path)
        
    def read(self, file_name):
        file_path = self.folder_path / Path(file_name)
        return pd.read_json(file_path)
    
    def dump_df(self, df, file_name):
        file_path = self.folder_path / Path(file_name)
        df.to_json(file_path)
        
    def get_file_content(self, file_name):
        file_path = self.fold_path / Path(file_name)
        with open(file_path) as f:
            for line in f:
                yield line
                
    def read_json(self, file, is_full_file_path=True):
        if is_full_file_path:
            file_path = file
        else:
            file_path = self.folder_path / Path(file)
        return load(file_path)
    
    def dump_json(self, file, is_full_file_path=True):
        if is_full_file_path:
            file_path = file
        else:
            file_path = self.folder_path / Path(file)
        dump(file_path)
        
    def read_json_v1(self, file, is_full_file_path=True):
        if is_full_file_path:
            file_path = file
        else:
            file_path = self.folder_path / Path(file)
        with open(file_path) as f:
            return json.load(f)
        
    def get_files(self, only_file_name=True, ignore_folder=False):
        return self._get_folder_file_with_latest_n_files_ordered_by_changed_time(-1, 
                                                                                 self.folder_path, 
                                                                                 only_file_name=only_file_name, 
                                                                                 ignore_folder=ignore_folder)
        
    def _get_folder_file_with_latest_n_files_ordered_by_changed_time(self, 
                                                                     n, 
                                                                     folder_path, 
                                                                     only_file_name=False,
                                                                     ignore_folder=True):
        if ignore_folder:
            files = [(os.path.join(folder_path, f), f) for f in os.listdir(folder_path) 
                    if os.path.isfile(os.path.join(folder_path, f))]
        else:
            files = [(os.path.join(folder_path, f), f) for f in os.listdir(folder_path)]
        files = sorted(files, key=lambda f: os.path.getmtime(f[0]), reverse=True)
        
        if n > 0:
            files = files[:n]
        if only_file_name:
            return [f[1] for f in files]
        else:
            return [f[0] for f in files]
        
    def _create_folder_without_error(self, full_file_path):
        folder_path = os.path.dirname(full_file_path)
        Path(folder_path).mkdir(exist_ok=True,  parents=True)
    
        
class DataManager(object):
    
    def __init__(self, project_name, root_folder, input_folder=None, metadata_folder=None, output_folder=None, created_time=None):
        super().__init__()
        if created_time is None:
            self._created_time = datetime.datetime.utcnow()
        else:
            self._created_time = created_time
        ts = int(TS.to(self._created_time, TS.TIMESTAMP))
            
        self._this_time_project_root_folder = Path(root_folder) / Path(project_name) / Path(str(ts))
        self.project_workspace = FileConnector(self._this_time_project_root_folder)
        if metadata_folder is not None:
            self.meta_workspace = FileConnector(metadata_folder)
        if input_folder is not None:
            self.input_workspace = FileConnector(input_folder)
        if output_folder is not None:
            self.output_workspace = FileConnector(self._output_folder)
        self.connectors = {}
            
    def _using_method_to_dest(self, dest, method, *args, **kwargs):
        connector = getattr(self, dest)
        access_data_method = getattr(connector, method)
        return access_data_method(*args, **kwargs)
    
    @staticmethod
    def create_connector_by_type(c_type):
        if c_type == "file":
            return FileConnector
        elif c_type == "spark":
            return SparkConnector
        elif c_type == "es":
            return ESConnector
        elif c_type == "service":
            return ServiceConnector
        else:
            raise NotSupportedError("Not supported connector type", c_type) 
        
        
    def add_resource(self, name, connector_type, **kwargs):
        Connector = DataManager.create_connector_by_type(connector_type)
        connector = Connector(**kwargs)
        if name in self.connectors:
            raise Exception("connector name duplicated", name)
        else:
            self.connectors[name] = connector
            
    def __enter__(self):
        pass
    
    def __exit__(self, type, value, traceback):
        pass
        