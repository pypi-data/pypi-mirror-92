import redis
from hwhpykit.cache.reids.base.RedisStringManager import RedisStringManager
from hwhpykit.cache.reids.base.RedisHashManager import RedisHashManager
from hwhpykit.cache.reids.base.RedisSetManager import RedisSetManager
from hwhpykit.cache.reids.base.RedisZSetManager import RedisZSetManager


class RedisManager(object):
    __redis = None
    __pool = None
    __tag = ""

    string = None
    hash = None
    set = None
    zset = None
    list = None

    @classmethod
    def config(cls, host='127.0.0.1', port=6379, db=0, password=''):
        cls.pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
        cls.redis = redis.Redis(connection_pool=cls.pool)
        cls.set = RedisSetManager.config(cls.redis)
        cls.hash = RedisHashManager.config(cls.redis)
        cls.zset = RedisZSetManager.config(cls.redis)
        cls.string = RedisStringManager.config(cls.redis)
        return cls

    @classmethod
    def string(cls):
        cls.check_connect()
        return RedisStringManager.config(cls.redis)

    @classmethod
    def hash(cls, key):
        cls.check_connect()
        return RedisHashManager.config(cls.redis, key)

    @classmethod
    def check_connect(cls):
        if cls.redis is None or cls.pool is None:
            raise Exception("redis config error")


