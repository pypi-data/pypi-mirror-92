

class RedisStringManager(object):
    __redis = None
    __pool = None

    @classmethod
    def config(cls, redis):
        cls.__redis = redis
        return cls

    @classmethod
    def set(cls, key, value, seconds=None):
        if seconds is None:
            cls.__redis.set(key, value)
        else:
            cls.__redis.set(key, value, ex=seconds)

    @classmethod
    def get(cls, key, start=None, end=None):
        if start is None and end is None:
            return cls.__redis.get(key)
        else:
            return cls.__redis.getrange(key, start, end)

    @classmethod
    def get_set(cls, key, new_value):
        return cls.__redis.getset(key, new_value)

    @classmethod
    def get_bit(cls, key, index):
        return cls.__redis.getbit(key, index)

    @classmethod
    def set_bit(cls, key, index, bit):
        cls.__redis.setbit(key, index, bit)

    @classmethod
    def get_list(cls, keys):
        return cls.__redis.mget(keys)

