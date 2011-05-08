
import redis
import ast
from time import time
import pprint

# setup pprint for debugging
pp = pprint.PrettyPrinter(indent=4)


# the TimeSeries class is used to abstract how we deal with data
# collected from responses to tests.  TimeSeries stores data
# using a redis set with scores.  In redis, a score is just a number
# so we use the timestamp of the response as the score so we keep
# everything in order allowing us to query for a name based on a
# window of time
class TimeSeries:

   def __init__(self):
      self._db = redis.Redis('localhost')

   def zput(self, key, value, when):
      self._db.zadd(key, value, when)

   # when we get the data for a given name, we pull the last 2 minutes
   # (120sec) of data
   def zget(self, key):
      dataArray = []
      data = []
      when = time()
      data = self._db.zrangebyscore(key, (when - 120), when);
      for r in data:
         try:
            d = ast.literal_eval(r);
            dataArray.append(d);
         except:
            ''' '''
      return dataArray

   # and we expire data older than 2 minutes
   def zexpire(self, key):
      when = int(time()) - 121
      r = self._db.zremrangebyscore(key, 0, when)

