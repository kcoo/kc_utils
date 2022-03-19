# kc_utils

### install

```shell script
pip install --upgrade kc_utils -i https://pypi.org/simple/
pip install --upgrade kc_utils['cache_redis'] -i https://pypi.org/simple/
```

### use

#### time
* get_time
```python
#:param num: 和unit配合使用计算时间
#:param sf: %Y%m%d%H%M%S
#:param unit: days = None, seconds = None, microseconds = None, milliseconds = None, minutes = None, hours = None, weeks = None
#:return: %Y%m%d%H%M%S 格式化时间
from kc_utils.time import get_time
get_time() #'20220320'
get_time(1) #'20220321'
get_time(-1) #'20220319'
get_time(-1, sf="%Y%m%d%H%M%S") #'20220319055451'
get_time(-1, sf="%Y%m%d%H%M%S", unit="hours") #'20220320045504'
```
* format_time
```python
#:param log_date: 字符串日期
#:param sf: %Y%m%d%H%M%S
#:param new_sf: %Y%m%d%H%M%S
#:return: 字符串日期
from kc_utils.time import get_time, format_time
format_time(get_time()) # '2022-03-20'
```

#### cache
```shell script
pip install --upgrade kc_utils['cache_redis'] -i https://pypi.org/simple/
```
* redis

```python
#redis 装饰器
#:param time: ttl
## time==0 or redis_store=None, 则不走缓存;
## time > 0, 则走缓存,缓存时间为time;
## time = -1, 则走缓存，缓存时间为永久.
## time = -2, 则不走缓存，并覆盖现有缓存
#:param redis_key_prefix: redis key prefix
#:param redis_store: redis_store

from kc_utils.cache.redis_helper import redising,KcRedis

db_redis = KcRedis(host='x', port=6379, password="xxx").get_redis()

@redising(time=10, redis_key_prefix="test", redis_store=db_redis)
def func_xxx(*args, **kwargs):
    return "xxx"

```