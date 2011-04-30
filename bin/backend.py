#!/usr/bin/python
import sys, os
#scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))

# account for where we live
#sys.path.append(scriptPath + '/..')
#sys.path.append(scriptPath + '/../lib')
sys.path.append('/opt/ogslb/lib')

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
        if(qtype == 'A' or qtype == 'ANY' or qtype == 'CNAME'):

           qname_lower = qname.lower()

           self.results = []
           try:
              t = TimeSeries()
              r = t.zget(qname_lower)

              priorities = {}
              for a in r:
                 try:
                    priorities[a['ip']] = int(priorities[a['ip']]) + int(a['priority'])
                 except:
                    priorities[a['ip']] = int(a['priority'])

#              priorities['1.2.3.4'] = 70


              high = 0
              iplist = {}
              for k in priorities:
                 if priorities[k] > high:
                    high = priorities[k]

              ips = []
              for k in priorities:
                 if priorities[k] == high:
                    ips.append(k)


              debug_log(ips)

#              debug_log( random.choice(ips) )

              self.results.append('DATA\t%s\t%s\tA\t%d\t-1\t%s' % (qname, qclass, DNSLookup.ttl, random.choice(ips)))
              self.has_result = True

           except:
              debug_log("no record")

        
#        if (qtype == 'A' or qtype == 'ANY') and qname_lower == 'webserver.example.com':
#            self.results.append('DATA\t%s\t%s\tA\t%d\t-1\t1.2.3.4' %
#                                (qname, qclass, DNSLookup.ttl))
#            self.results.append('DATA\t%s\t%s\tA\t%d\t-1\t1.2.3.5' %
#                                (qname, qclass, DNSLookup.ttl))
#            self.results.append('DATA\t%s\t%s\tA\t%d\t-1\t1.2.3.6' %
#                                (qname, qclass, DNSLookup.ttl))
#            self.has_result = True
#        elif (qtype == 'CNAME' or qtype == 'ANY') and qname_lower == 'www.example.com':
#            self.results.append('DATA\t%s\t%s\tCNAME\t%d\t-1\twebserver.example.com' %
#                                (qname, qclass, DNSLookup.ttl))
#            self.has_result = True

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
    #sys.stdout.close()
    #outfile = os.fdopen(1, 'w', 1)
    outfile = sys.stdout
    try:
        PowerDNSbackend(infile, outfile)
    except:
        debug_log('execution failure:' + str(sys.exc_info()[0]))
        raise


