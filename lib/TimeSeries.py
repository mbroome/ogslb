
import redis
import ast
from time import time
import pprint
pp = pprint.PrettyPrinter(indent=4)


class TimeSeries:

   def __init__(self):
      self._db = redis.Redis('localhost')

   def zput(self, key, value, when):
#      when = int(when)
      self._db.zadd(key, value, when)

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

   def zexpire(self, key):
      when = int(time()) - 121
      r = self._db.zremrangebyscore(key, 0, when)

