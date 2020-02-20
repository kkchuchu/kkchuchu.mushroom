from multiprocessing import Pool, TimeoutError

from elasticsearch import helpers


class Mapper(object):

    def __init__(self, map_type="async_process", number_of_workers=4, timeout=5, 
                 es_client=None, es_index=None):
        self.pool = self._decide_worker(map_type, es_client=es_client)
        self.map_type = map_type
        self.number_of_workers = number_of_workers
        self.timeout = timeout
        self.es_index = es_index

    def _decide_worker(self, map_type, es_client=None):
        if map_type == "async_process":
            return Pool(self.number_of_workers)
        elif map_type == "es_bulk":
            return es_client

    def map(self, func, params:tuple=None):
        if self.map_type == "async_process":
            return self._async_map(func, params)
        elif self.map_type == "es_bulk":
            return self._es_parallel_bulk(func)

    def _async_map(self, func, params):
        """
        Reference: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.multiprocessing.Pool.map
        """
        res = self.pool.apply_async(func, params)
        try:
            return res.get(timeout=self.timeout)
        except TimeoutError:
            return None
            
    def _es_parallel_bulk(self, func):
        """
        Reference: https://discuss.elastic.co/t/helpers-parallel-bulk-in-python-not-working/39498
        """
        return helpers.parallel_bulk(client=self.pool, actions=func, thread_count=self.number_of_workers, index=self.es_index)        
