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
#import redis
import pprint
from time import time

BackendType = "sqlite"

# setup pprint for debugging
pp = pprint.PrettyPrinter(indent=4)


# the Stats class abstracts away how we deal with statistics collected.
# these statistics are at a more global level that what is managed in
# TimeSeries which is collected from responses to tests.  Stats is used
# for things such as collecting info about how ogslb it's self is doing
class Stats:
   def __init__(self, Config):
      self._config = Config
      self._db = sqlite3.connect('/var/tmp/ogslb-stats.db')
      try:
         self._setupDB()
      except:
         """ """

   def _setupDB(self):
      cursor = self._db.cursor()
      if(cursor):
         sql = """create table stats (
                     id TEXT not null,
                     last INT,
                     value TEXT not null,
                     primary key(id, value)
                  )
               """
         cursor.execute(sql)
         self._db.commit()


   def sput(self, key, value):
      valuehash = (key, time(), value)
      sql = "insert into stats (id, last, value) values (?,?,?)"

      cursor = self._db.cursor()
      if(cursor):
         try:
            cursor.execute(sql, valuehash)
            self._db.commit()
         except:
            """ """


   def sget(self, key):
      dataArray = []
      data = []
      valuehash = (key,)
      sql = "select value from stats where id=?"

      cursor = self._db.cursor()
      if(cursor):
         try:
            cursor.execute(sql, valuehash)
            data = cursor.fetchall()
            for r in data:
               dataArray.append(r[0])
         except:
            """ """

      return dataArray

   # this needs to get smarter
   def sexpire(self, key):
      valuehash = (key,)
      sql = "delete from stats where id=?"

      cursor = self._db.cursor()
      if(cursor):
         try:
            cursor.execute(sql, valuehash)
            self._db.commit()
         except:
            """ """


   def sinset(self, key, value):
      valuehash = (key, value)
      sql = "select value from stats where key=? and value=?"

      cursor = self._db.cursor()
      if(cursor):
         try:
            cursor.execute(sql, valuehash)
            if cursor.rowcount:
               return True
         except:
            """ """

      return False


