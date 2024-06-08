import redis

from api.exceptions.KeyNotFound import KeyNotFound


class RedisService:
    def __init__(self, host, port):
        self.redis = redis.Redis(host=host, port=port, db=0)

    def set(self, key):
        self.redis.set(key, "SUPPORTED")

    def checkIfKeyExist(self, key):
        value = self.redis.get(key)

        if value is None:
            raise KeyNotFound()
