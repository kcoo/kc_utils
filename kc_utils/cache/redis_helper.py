# -*- coding: utf-8 -*-
from functools import wraps
import hashlib
import logging
import json
import redis


class KcRedis(object):
    def __init__(self, host, port, password, db=0):
        self.pool = redis.ConnectionPool(host=host, password=password, port=port, db=db)
        self.rs = redis.Redis(connection_pool=self.pool, db=db)

    def get_redis(self):
        return self.rs


def redising(time=0, redis_key_prefix="kc_utils_redising", redis_store=None):
    '''
    redis 装饰器
    :param time: ttl
    # time==0 or redis_store=None, 则不走缓存;
    # time > 0, 则走缓存,缓存时间为time;
    # time = -1, 则走缓存，缓存时间为永久.
    # time = -2, 则不走缓存，并覆盖现有缓存
    :param redis_key_prefix: redis key prefix
    :param redis_store: redis_store
    :return:
    '''
    def func_wrapper(func):

        def _get_func_info_md5(*args, **kwargs):
            func_info_str = "func[{func}]\t file[{file}{line}]\t args[{args}]\t kwargs[{kwargs}]".format(
                func=func.__code__.co_name,
                file=func.__code__.co_filename,
                line=func.__code__.co_firstlineno,
                args=args,
                kwargs=kwargs
            )
            m2 = hashlib.md5()
            m2.update(func_info_str.encode('utf-8'))
            func_info_str_md5 = m2.hexdigest()
            return func_info_str_md5

        def _get_func_result(*args, **kwargs):
            if redis_store is None:
                return func(*args, **kwargs)
            redis_key = "{redis_key_prefix}_{md5}".format(redis_key_prefix=redis_key_prefix,
                                                          md5=_get_func_info_md5(*args, **kwargs))
            if time == 0:
                func_result = func(*args, **kwargs)
                redis_store.delete(redis_key)
                logging.info("redising[exec-func]:del[{redis_key}]".format(redis_key=redis_key))
                return func_result
            if time == -1 or time > 0:
                if redis_store.exists(redis_key):
                    redis_result = redis_store.get(redis_key)
                    if redis_result is not None:
                        logging.info("redising[redis-result]:get[{redis_key}]".format(redis_key=redis_key))
                        func_result = json.loads(redis_result)
                        return func_result
                logging.info("redising[exec-func]:set[{redis_key}]".format(redis_key=redis_key))
                func_result = func(*args, **kwargs)
                redis_store.set(redis_key, json.dumps(func_result), time if time > 0 else None)
                return func_result
            if time == -2:
                logging.info("redising[exec-func]:set[{redis_key}]".format(redis_key=redis_key))
                func_result = func(*args, **kwargs)
                redis_store.set(redis_key, json.dumps(func_result))
                return func_result
            logging.info("redising[exec-func]:未知time[{time}]".format(time=time))
            return func(*args, **kwargs)

        @wraps(func)
        def return_wrapper(*args, **kwargs):
            return _get_func_result(*args, **kwargs)

        return return_wrapper
    return func_wrapper

