import socket
import time
import re
import pprint
import logging

l = logging.getLogger("gslb")

timeout = 10
socket.setdefaulttimeout(timeout)


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

