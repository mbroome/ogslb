#!/usr/bin/python
import os, sys, glob, imp

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))

# account for where we live
sys.path.append(scriptPath + '/..')
sys.path.append(scriptPath + '/../lib')
sys.path.append(scriptPath + '/../proto')

from time import time;
from TimeSeries import *
import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

t = TimeSeries()
value = {}
value['address'] = '1.2.3.4'
value['speed'] = 1234
value['when'] = time()

#t.zput('www.yahoo.com', value, value['when']);

r = t.zget('www.google.com')
pp.pprint(r)
#t.zexpire('www.yahoo.com')



priorities = {}
for a in r:
   try:
      priorities[a['address']] = int(priorities[a['address']]) + int(a['priority'])
   except:
      priorities[a['address']] = int(a['priority'])

#priorities['1.2.3.4'] = 70

pp.pprint(priorities)

high = 0
addresslist = {}
for k in priorities:
   if priorities[k] > high:
      high = priorities[k]

addresss = []
for k in priorities:
   if priorities[k] == high:
      addresss.append(k)


pp.pprint(addresss)

print random.choice(addresss)

