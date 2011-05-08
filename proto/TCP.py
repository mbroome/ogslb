import socket
import time
import re
import pprint
import logging

# fire up the logger
logger = logging.getLogger("ogslb")

timeout = 10
socket.setdefaulttimeout(timeout)

# The TCP test is the most basic test that actually talks to a server.
# we basically just connect to a tcp port and if something was listening,
# then we assume the service is alive

def getTCP(host, port):
   status = 0
   reason = ''
   try:
      s = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
      s.connect((host, int(port)))
      s.shutdown(1)
      s.close()
      status = 1
   except socket.error, e:
      reason = "error connecting %s" % host
   return((status, reason))

def get(data, queue, passCount, Config):
   t1 = time.time()
   found, reason = getTCP(data['address'], data['port'])
   t2 = time.time()
   speed = ((t2-t1)*1000.0)

   if speed >= 10000:
      reason = 'timeout'

   queue.put(data)

