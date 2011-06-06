#!/usr/bin/python
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


import sqlite3
import logging
import ast
from time import time
import pprint

BackendType = "sqlite"

# setup pprint for debugging
pp = pprint.PrettyPrinter(indent=4)

# and setup the logger
logger = logging.getLogger("ogslb")


# the TimeSeries class is used to abstract how we deal with data
# collected from responses to tests.  TimeSeries stores data
# using a redis set with scores.  In redis, a score is just a number
# so we use the timestamp of the response as the score so we keep
# everything in order allowing us to query for a name based on a
# window of time
class TimeSeries:

   def __init__(self, Config):
      self._config = Config
      self._db = sqlite3.connect('/var/tmp/ogslb-timeseries.db', check_same_thread = False)
      try:
         self._setupDB()
      except:
         """ """

   def _setupDB(self):
      cursor = self._db.cursor()
      if(cursor):
         sql = """create table timeseries (
                     id TEXT not null,
                     status INT not null,
                     last INT not null,
                     value TEXT,
                     primary key(id, last)
                  )
               """
         cursor.execute(sql)
         self._db.commit()

   def zput(self, key, value, when):
      valuehash = (key,value['status'],when,str(value))
      sql = "insert into timeseries (id, status, last, value) values (?,?,?,?)"
      cursor = self._db.cursor()
      if(cursor):
         try:
            cursor.execute(sql, valuehash)
            self._db.commit()
         except:
            print "error puting value";

   # when we get the data for a given name, we pull the last 2 minutes
   # (120sec) of data
   def zget(self, key):
      dataArray = []
      data = []
      when = time()

      valuehash = (key, (when - 120))
      sql = "select value from timeseries where id = ? and status = 1 and last >= ?"

      cursor = self._db.cursor()
      if(cursor):
            cursor.execute(sql, valuehash)
            data = cursor.fetchall()
            for r in data:
                  d = ast.literal_eval(r[0]);
                  dataArray.append(d);
            return dataArray

   # and we expire data older than 2 minutes
   def zexpire(self, key):
      when = int(time()) - 121
      valuehash = (key, when)
      sql = "delete from timeseries where id = ? and last < ?"

      cursor = self._db.cursor()
      if(cursor):
         try:
            cursor.execute(sql, valuehash)
            self._db.commit()
         except:
            print "error expiring record"



