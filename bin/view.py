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


addressData = {}
priorities = {}
for a in r:
   try:
      priorities[a['address']] = int(priorities[a['address']]) + int(a['priority'])
   except:
      priorities[a['address']] = int(a['priority'])
   addressData[a['address']] = a

#priorities['1.2.3.4'] = 70
pp.pprint(addressData)

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

