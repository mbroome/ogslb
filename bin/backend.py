#!/usr/bin/python
import sys, os
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

def DNSLookup(query):
   """parse DNS query and produce lookup result.

   query: a sequence containing the DNS query as per PowerDNS manual appendix A:
   http://downloads.powerdns.com/documentation/html/backends-detail.html#PIPEBACKEND-PROTOCOL
   """
   (_type, qname, qclass, qtype, _id, ip) = query

   logger.debug("doing a lookup")

   results = ''
   # we only deal with a few of the query types
   if(qtype == 'A' or qtype == 'ANY' or qtype == 'CNAME'):

      qname_lower = qname.lower()

      selectedAddres = ''
      recordType = ''
      try:
         r = redis.zget(qname_lower)

         addressData = {}
         priorities = {}
         for a in r:
            try:
               priorities[a['address']] = int(priorities[a['address']]) + int(a['priority'])
            except:
               priorities[a['address']] = int(a['priority'])
            addressData[a['address']] = a


         high = 0
         addresslist = {}
         for k in priorities:
            if priorities[k] > high:
               high = priorities[k]

         addresss = []
         for k in priorities:
            if priorities[k] == high:
               addresss.append(k)


         logger.debug(addresss)

         selectedAddres = random.choice(addresss)

         try:
            if addressData[selectedAddres]['recordtype']:
               recordType = addressData[selectedAddres]['recordtype']
         except:
            recordType = 'A'

         logger.debug(selectedAddres)
         logger.debug(recordType)

         results = 'DATA\t%s\t%s\t%s\t%d\t-1\t%s' % (qname, qclass, recordType, 60, selectedAddres)

         return(results)
      except:
         logger.debug("no record")
         return(results)
   else:
      return(results)


def fprint(message):
   """Print the given message with newline and flushing."""
   sys.stdout.write(message + '\n')
   sys.stdout.flush()
   logger.debug('sent to pdns:%s' % message)


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

   logger.info('startup')

   first_time = True
   while 1:
       rawline = sys.stdin.readline()
       if rawline == '':
          logger.debug('EOF')
          return  # EOF detected
       line = rawline.rstrip()

       logger.debug('received from pdns:%s' % line)
            
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
       else:
          query = line.split('\t')
          if len(query) != 6:
             fprint('LOG\tPowerDNS sent unparseable line')
             fprint('FAIL')
          else:
             logger.debug('Performing DNSLookup(%s)' % repr(query))
             lookup = ''
             lookup = DNSLookup(query)
             if lookup != '':
                logger.debug(lookup)
                fprint(lookup)
             fprint('END')



if __name__ == '__main__':
   main()

