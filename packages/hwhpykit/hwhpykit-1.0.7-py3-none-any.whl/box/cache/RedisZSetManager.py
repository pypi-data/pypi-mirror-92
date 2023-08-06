

class RedisZSetManager(object):
    __redis = None
    __pool = None

    @classmethod
    def config(cls, redis):
        cls.__redis = redis
        return cls
