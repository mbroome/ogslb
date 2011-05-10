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

import sys, os

# figure out where the script is so we can setup paths relative to it
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))

# account for where we live
sys.path.append(scriptPath + '/..')
sys.path.append(scriptPath + '/../lib')

from TimeSeries import *
import time
import logging
import logging.handlers
import random
import pprint
pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger("ogslb")
redis = TimeSeries()

# backend.py is the python backend that is called by PowerDNS and talks to redis.
# We listen to stdin and talk on stdout which effectivly attaches us to PowerDNS.

# Here, we actually talk to redis and do our prioritizing of healthy services
def DNSLookup(query):
   """parse DNS query and produce lookup result."""

   (_type, qname, qclass, qtype, _id, ip) = query

   logger.debug("doing a lookup")

   results = ''
   # we only deal with a few of the query types
   if(qtype == 'A' or qtype == 'ANY' or qtype == 'CNAME'):

      # we deal with everything in lowercase
      qname_lower = qname.lower()

      selectedAddres = ''
      recordType = ''
      try:
         # see if we can find a matching hostname in redis
         r = redis.zget(qname_lower)

         addressData = {}
         priorities = {}
         for a in r: # build up a list of priorities for each of the addresses returned from redis
            try:
               priorities[a['address']] = int(priorities[a['address']]) + int(a['priority'])
            except:
               priorities[a['address']] = int(a['priority'])
            addressData[a['address']] = a


         high = 0
         addresslist = {}
         for k in priorities: # find the highest total priority from the responses
            if priorities[k] > high:
               high = priorities[k]

         addresss = []
         for k in priorities: # and now find the list of addresses that matched the high priority
            if priorities[k] == high:
               addresss.append(k)


         logger.debug(addresss)

         # pick a random address from the list of addresses matching the high priority
         selectedAddres = random.choice(addresss)

         # if there is an address type (such as CNAME)  set, use it.  Otherwise, assume it's an 'A' record
         try:
            if addressData[selectedAddres]['recordtype']:
               recordType = addressData[selectedAddres]['recordtype']
         except:
            recordType = 'A'

         logger.debug(selectedAddres)
         logger.debug(recordType)

         # build up the response to hand back
         results = 'DATA\t%s\t%s\t%s\t%d\t-1\t%s' % (qname, qclass, recordType, 60, selectedAddres)

         return(results)
      except:
         logger.debug("no record")
         return(results)
   else:
      return(results)

# print the message to PowerDNS with a newline and flush it
def fprint(message):
   sys.stdout.write(message + '\n')
   sys.stdout.flush()
   logger.debug('sent to pdns:%s' % message)


# the main program 
def main():
   pid = os.getpid()
   logFile = '/tmp/backend-%d.log' % pid
   debug = 0

   # setup the logger
   if(debug):
      logger.setLevel(logging.DEBUG)
   else:
      logger.setLevel(logging.INFO)

   ch = logging.handlers.RotatingFileHandler(logFile, maxBytes=25000000, backupCount=5)

   if(debug):
      ch.setLevel(logging.DEBUG)
   else:
      ch.setLevel(logging.INFO)

   formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
   ch.setFormatter(formatter)
   logger.addHandler(ch)

   # and fire up the logger
   logger.info('startup')

   first_time = True

   # here, we have to deal with how to talk to PowerDNS.
   while 1: # loop forever reading from PowerDNS
       rawline = sys.stdin.readline()
       if rawline == '':
          logger.debug('EOF')
          return  # EOF detected
       line = rawline.rstrip()

       logger.debug('received from pdns:%s' % line)

       # If this is the first pass reading from PowerDNS, look for a HELO
       if first_time:
          if line == 'HELO\t1':
             fprint('OK\togslb backend firing up')
          else:
             fprint('FAIL')
             logger.debug('HELO input not received - execution aborted')
             rawline = sys.stdin.readline()  # as per docs - read another line before aborting
             logger.debug('calling sys.exit()')
             sys.exit(1)
          first_time = False
       else: # now we actually get busy
          query = line.split('\t')
          if len(query) != 6:
             fprint('LOG\tPowerDNS sent unparseable line')
             fprint('FAIL')
          else:
             logger.debug('Performing DNSLookup(%s)' % repr(query))
             lookup = ''
             # Here, we actually to the real work.  Lookup a hostname in redis and prioritize it
             lookup = DNSLookup(query)
             if lookup != '':
                logger.debug(lookup)
                fprint(lookup)
             fprint('END')


# the main program
if __name__ == '__main__':
   main()

