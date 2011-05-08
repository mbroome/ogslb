import socket
import time
import re
import pprint
import logging

# fire up the logger
logger = logging.getLogger("ogslb")

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

import smtplib

# and setup pprint for debugging
#pp = pprint.PrettyPrinter(indent=4)

# The SMTP test makes sure we can do a very basic smtp test.  Basically,
# we just connect to a mail server and issue a helo

# actually do the smtp test
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
   found, reason = getSMTP(data['address'], port)
   t2 = time.time()
   speed = ((t2-t1)*1000.0)

   if speed >= 10000:
      reason = 'timeout'

   queue.put(data)

