# Open Global Server Load Balancer (ogslb)
# Copyright (C) 2010 Mitchell Broome
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import redis
import ast
from time import time
import pprint

BackendType = "redis"

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

