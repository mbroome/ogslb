import threading
import Queue
import socket
import time
import logging
from TimeSeries import *
import pprint

pp = pprint.PrettyPrinter(indent=4)

l = logging.getLogger("ogslb")

class Responder(threading.Thread):
    def __init__(self, queue, Config, threadID):
        self.__queue = queue
        self.Config = Config
        self.threadName = "responder-" + str(threadID)
        threading.Thread.__init__(self, name=self.threadName)

#        myIP = socket.gethostbyname(socket.gethostname())

        self._db = TimeSeries()


    def run(self):
        while 1:
            item = self.__queue.get()
            if item is None:
                break # reached end of queue

            # store the info in redis
            self._db.zput(item['name'], item, item['when']);

            # and cleanup any old data about this name
            self._db.zexpire(item['name']);


