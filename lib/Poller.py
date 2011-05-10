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

import os, sys, glob, imp

import logging
import threading
import random
import time
import pprint

# setup pprint for debugging
pp = pprint.PrettyPrinter(indent=4)

# and setup the logger
logger = logging.getLogger("ogslb")

# The Poller class defines a thread that is used to monitor addresses.
# It loads up protocols from the proto dir, watches the queue and performs tests
class Poller(threading.Thread):
   def __init__(self, queue, Config, responderQueue, threadID):
      self.__queue = queue
      self.Config = Config
      self.responderQueue = responderQueue
      self.threadName = "poller-" + str(threadID)
      threading.Thread.__init__(self, name=self.threadName)

      # figure out where the protocol analizers live
      protoDir = ''
      try:
         protoDir = self.Config['protodir']
      except:
         protoDir = '/opt/ogslb/proto' # default to here if not configured in config.xml
      protoDir += '/*.py'
      logger.debug("protodir: %s" % protoDir)

      # and know load up all of the protocals
      fl = glob.glob(protoDir)
      self.adapters = {}
      for i in range(len(fl)):
          filename = fl[i]
          modpath = fl[i].split('/')
          fl[i] = modpath[len(modpath)  - 1]
          if fl[i] != '__init__.py': # don't try to load the __init__.py file
             fl[i] = fl[i][0:(len(fl[i])-3)]
             r = imp.load_source(fl[i], filename)
             self.adapters[fl[i]] = r

   def __del__(self):
      logger.debug("thread exiting")


   def run(self):
      while 1: # watch the queue forever
         item = self.__queue.get()
         if item is None:
            break # reached end of queue

         # now that we have something we picked up from the queue, parse it and get busy
         vip, data, passCount = item

         # based on the type of protocol, actually do the check
         try:
            r = self.adapters[ data['Type'] ].get(data, self.responderQueue, passCount, self.Config)
         except:
            logger.debug("error in get")





