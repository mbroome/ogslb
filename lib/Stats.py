
import redis
import pprint
pp = pprint.PrettyPrinter(indent=4)


class Stats:

   def __init__(self):
      self._db = redis.Redis('localhost')

   def sput(self, value):
      key = 'stats.hostlist'
      self._db.sadd(key, value)

   def sget(self, key='stats.hostlist'):
      data = []
      data = self._db.smembers(key);
      return data

   def sexpire(self, key='stats.hostlist'):
      r = self._db.delete(key)

   def sinset(self, value):
      key = 'stats.hostlist'
      r = self._db.sismember(key, value)
      return r

