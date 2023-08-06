

class RedisZSetManager(object):
    __redis = None
    __pool = None

    @classmethod
    def config(cls, redis, key=None):
        cls.__redis = redis
        cls.__key = key
        return cls
