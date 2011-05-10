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

