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

