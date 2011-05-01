import socket
import time
import re
import pprint
import logging

l = logging.getLogger("gslb")

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

import smtplib

#pp = pprint.PrettyPrinter(indent=4)

def getSMTP(host, port):
   ret = 0
   reason = ''
   try:
      smtp = smtplib.SMTP(host, port, 'localhost')
      smtp.helo('localhost')
      smtp.quit()
      ret = 1
   except smtplib.SMTPConnectError, e:
      reason = e.code + ' ' + e.read()
   except:
      response = "error getting data: %s" % host
   return((ret, reason))

def get(data, queue, passCount, Config):
   try:
      port = data['port']
   except:
      port = 25

   reason = ''
   t1 = time.time()
   found, reason = getSMTP(data['ip'], port)
   t2 = time.time()
   speed = ((t2-t1)*1000.0)

   if speed >= 10000:
      reason = 'timeout'

#   queue.put((data['Type'], port, data['name'], data['ip'], found, speed, data['tag'], t1, passCount, reason, data['priority']))
   queue.put(data)

