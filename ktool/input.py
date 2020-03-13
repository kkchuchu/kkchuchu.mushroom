import sys
import os
import json
import configparser
from pathlib import Path
import urllib
import pandas
import datetime

from joblib import dump, load
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, scoped_session


import pandas as pd
from elasticsearch import Elasticsearch, helpers


class BaseConnector(object):

    def __init__(self, timeout=30):
        self.timeout = timeout


class ESConnector(object):

    def __init__(self, host, port=9200, timeout=60, default_index=None):
        self.elasticsearch_hosts = [host]
        self.port = port
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


class SQLDBConnector(object):

    def __init__(self, connection_str, autocommit=False, autoflush=False, pool_size=5, pool_recycle=7200, pool_timeout=7200):
        self.engine = create_engine(connection_str,
                                    pool_size=pool_size,
                                    pool_recycle=pool_recycle,
                                    pool_timeout=pool_timeout)

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
    
    def get_df(self, sql_statement):
        return pandas.read_sql(sql_statement, con=self.engine)


class ServiceConnector(BaseConnector):

    def __init__(self, host):
        self.host = host
        super().__init__()

    def get(self, uri, **kwargs):
        full_url = (host + uri).format(**kwargs)
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
    
    def __init__(self, folder_path, timeout=30):
        super().__init__(timeout=timeout)
        self.folder_path = Path(folder_path)
        self._create_folder_without_error(self.folder_path)
        
    def get_file_content(self, file_name):
        file_path = self.fold_path / Path(file_name)
        with open(file_path) as f:
            for line in f:
                yield line
                
    def read_json(self, file_name):
        file_path = self.fold_path / Path(file_name)
        return load(file_path)
    
    def dump_json(self, file_name):
        file_path = self.fold_path / Path(file_name)
        dump(file_path)
        
    def _get_folder_file_with_latest_n_files_ordered_by_changed_time(self, n, folder_path):
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                 if os.path.isfile(os.path.join(folder_path, f))]
        
        files = sorted([f for f in files], key=lambda f: os.path.getmtime(f), reverse=True)
        if n > 0:
            files = files[:n]
        return files
        
    def _create_folder_without_error(self, full_file_path):
        folder_path = os.path.dirname(full_file_path)
        Path(folder_path).mkdir(exist_ok=True,  parents=True)
    
        
class DataManager(object):
    
    def __init__(self, project_name, root_folder, output_folder=None, created_time=None):
        super().__init__()
        if created_time is None:
            self._created_time = datetime.datetime.now()
        else:
            self._created_time = created_time
        import calendar
        ts = calendar.timegm(self._created_time.timetuple())
            
        self._project_root_folder = Path(root_folder) / Path(project_name)
        self._this_time_project_root_folder = self._project_root_folder / Path(str(ts))
        self.project_workspace = FileConnector(self._this_time_project_root_folder)
        if output_folder is not None:
            self._output_folder = Path(output_folder)
            self.output_workspace = FileConnector(self._output_folder)
            
    def _using_method_to_dest(self, dest, method, *args, **kwargs):
        connector = getattr(self, dest)
        access_data_method = getattr(connector, method)
        return access_data_method(*args, **kwargs)
        
        
    @staticmethod
    def struct_connector(self):
        pass
        
    def __enter__(self):
        pass
    
    def __exit__(self, type, value, traceback):
        pass
        