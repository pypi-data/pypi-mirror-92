
class RedisSetManager(object):
    __redis = None
    __key = None

    @classmethod
    def config(cls, redis, key=None):
        cls.__redis = redis
        return cls