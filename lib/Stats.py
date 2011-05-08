
import redis
import pprint

# setup pprint for debugging
pp = pprint.PrettyPrinter(indent=4)


# the Stats class abstracts away how we deal with statistics collected.
# these statistics are at a more global level that what is managed in
# TimeSeries which is collected from responses to tests.  Stats is used
# for things such as collecting info about how ogslb it's self is doing
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

