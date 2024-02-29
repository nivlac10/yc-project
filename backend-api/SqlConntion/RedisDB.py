import redis

from app import constant

host = '127.0.0.1'


class Redis:
    def __init__(self):
        self.connection_pool = redis.ConnectionPool(host=constant.DBCONFIG[constant.DBINDEX]['redis_db'], port=6379,
                                                    db=0, decode_responses=True)
        self.client = redis.Redis(connection_pool=self.connection_pool)

    def set(self, key, value):
        return self.client.set(key, value)

    def hset(self, key, mkey, value):
        return self.client.hset(key, mkey, value)

    def get(self, key):
        return self.client.get(key)

    def hget(self, key, mkey):
        return self.client.hget(key, mkey)

    def rpush(self, key, mkey):
        return self.client.rpush(key, mkey)

    def delete(self, key):
        return self.client.delete(key)

    def keys(self, pattern='*'):
        return self.client.keys(pattern)

    def close(self):
        self.connection_pool.disconnect()

    def hincrby(self, key, mkey, value):
        return self.client.hincrby(key, mkey, value)

    def expire(self, key, ex):
        return self.client.expire(key, ex)
