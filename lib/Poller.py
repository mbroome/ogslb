import os, sys, glob, imp

import logging
import threading
import random
import time
import pprint

pp = pprint.PrettyPrinter(indent=4)
l = logging.getLogger("ogslb")


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
         protoDir = Config['protodir']
      except:
         protoDir = '/opt/ogslb/proto'
      protoDir += '/*.py'
      l.debug("protodir: %s" % protoDir)

      # and know load up all of the protocals
      fl = glob.glob(protoDir)
      self.adapters = {}
      for i in range(len(fl)):
          file = fl[i]
          fl[i] = fl[i].split('/')[4]
          if fl[i] != '__init__.py': # don't try to load the __init__.py file
             fl[i] = fl[i][0:(len(fl[i])-3)]
             r = imp.load_source(fl[i], file)
             self.adapters[fl[i]] = r

   def __del__(self):
      l.debug("thread exiting")


   def run(self):
      while 1: # watch the queue forever
         item = self.__queue.get()
         if item is None:
            break # reached end of queue

         vip, data, passCount = item

         # based on the type of protocol, actually do the check
         try:
            r = self.adapters[ data['Type'] ].get(data, self.responderQueue, passCount, self.Config)
         except:
            l.debug("error in get")





