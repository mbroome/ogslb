#!/usr/bin/python
import sys, os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))

# account for where we live
sys.path.append(scriptPath + '/..')
sys.path.append(scriptPath + '/../lib')

from TimeSeries import *
import time
import random
import pprint
pp = pprint.PrettyPrinter(indent=4)


class DNSLookup(object):
    """Handle PowerDNS pipe-backend domain name lookups."""
    ttl = 1
    
    def __init__(self, query):
        """parse DNS query and produce lookup result.

        query: a sequence containing the DNS query as per PowerDNS manual appendix A:
        http://downloads.powerdns.com/documentation/html/backends-detail.html#PIPEBACKEND-PROTOCOL
        """
        (_type, qname, qclass, qtype, _id, ip) = query
        self.has_result = False  # has a DNS query response

        # we only deal with a few of the query types
        if(qtype == 'A' or qtype == 'ANY' or qtype == 'CNAME'):

           qname_lower = qname.lower()

           self.results = []
           selectedAddres = ''
           recordType = ''
           try:
              t = TimeSeries()
              r = t.zget(qname_lower)

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


              debug_log("########## address list");
              debug_log(addresss)

              debug_log("########## pick an address");
              selectedAddres = random.choice(addresss)

              try:
                 if addressData[selectedAddres]['recordtype']:
                    recordType = addressData[selectedAddres]['recordtype']
              except:
                 recordType = 'A'

              debug_log("##############  here");
              debug_log(selectedAddres)
              debug_log(recordType)

              self.results.append('DATA\t%s\t%s\t%s\t%d\t-1\t%s' % (qname, qclass, recordType, DNSLookup.ttl, selectedAddres))
              self.has_result = True

           except:
              debug_log("no record")

        

    def str_result(self):
        """return string result suitable for pipe-backend output to PowerDNS."""
        if self.has_result:
            return '\n'.join(self.results)
        else:
            return ''

class Logger(object):
    def __init__(self):
        pid = os.getpid()
        self.logfile = '/tmp/backend-%d.log' % pid

    def write(self, msg):
        logline = '%s|%s\n' % (time.asctime(), msg)
        f = file(self.logfile, 'a')
        f.write(logline)
        f.close()

def debug_log(msg):
    logger.write(msg)

class PowerDNSbackend(object):
    """The main PowerDNS pipe backend process."""
    
    def __init__(self, filein, fileout):
        """initialise and run PowerDNS pipe backend process."""
        self.filein = filein
        self.fileout = fileout
        
        self._process_requests()   # main program loop

    def _process_requests(self):
        """THE main program loop."""
        first_time = True
        while 1:
            rawline = self.filein.readline()
            if rawline == '':
                debug_log('EOF')
                return  # EOF detected
            line = rawline.rstrip()

            debug_log('received from pdns:%s' % line)
            
            if first_time:
                if line == 'HELO\t1':
                    self._fprint('OK\tPython backend firing up')
                else:
                    self._fprint('FAIL')
                    debug_log('HELO input not received - execution aborted')
                    rawline = self.filein.readline()  # as per docs - read another line before aborting
                    debug_log('calling sys.exit()')
                    sys.exit(1)
                first_time = False
            else:
                query = line.split('\t')
                if len(query) != 6:
                    self._fprint('LOG\tPowerDNS sent unparseable line')
                    self._fprint('FAIL')
                else:
                    debug_log('Performing DNSLookup(%s)' % repr(query))
                    lookup = DNSLookup(query)
                    if lookup.has_result:
                        self._fprint(lookup.str_result())
                    self._fprint('END')

    def _fprint(self, message):
        """Print the given message with newline and flushing."""
        self.fileout.write(message + '\n')
        self.fileout.flush()
        debug_log('sent to pdns:%s' % message)

if __name__ == '__main__':
    logger = Logger()
    infile = sys.stdin
    outfile = sys.stdout
    try:
        PowerDNSbackend(infile, outfile)
    except:
        debug_log('execution failure:' + str(sys.exc_info()[0]))
        raise


