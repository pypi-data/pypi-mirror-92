

class RedisHashManager(object):
    __redis = None
    __hash_key = None

    @classmethod
    def config(cls, redis):
        cls.__redis = redis
        return cls
