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

import threading
import Queue
import socket
import time
import logging
from TimeSeries import *
import pprint

# setup pprint for debugging
pp = pprint.PrettyPrinter(indent=4)

# and fire up the logger
logger = logging.getLogger("ogslb")

# the Responder class watches for responses from each test and inserts them into redis
class Responder(threading.Thread):
    def __init__(self, queue, Config, threadID):
        self.__queue = queue
        self.Config = Config
        self.threadName = "responder-" + str(threadID)
        threading.Thread.__init__(self, name=self.threadName)

        # setup the time series connection
        self._db = TimeSeries()


    def run(self):
        while 1: # watch the queue forever
            item = self.__queue.get()
            if item is None:
                break # reached end of queue

            # store the info in redis
            self._db.zput(item['name'], item, item['when']);

            # and cleanup any old data about this name
            self._db.zexpire(item['name']);


