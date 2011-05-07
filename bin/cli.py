#!/usr/bin/python
import os, sys, glob, imp

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))

# account for where we live
sys.path.append(scriptPath + '/..')
sys.path.append(scriptPath + '/../lib')
sys.path.append(scriptPath + '/../proto')

from time import time;
from TimeSeries import *
from Stats import *
import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

t = TimeSeries()
s = Stats()

#r = t.zget('www.google.com')

r = s.sget()

for i in r:
   print "Hostname: %s" % i
   x = t.zget(i)
#   print x
#   pp.pprint(x)
   c = 1
   for y in x:
      print "%d: %s" % (c, y)
      c = c + 1
   print '\n'
