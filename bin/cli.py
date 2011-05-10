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

from time import *
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
#      print "%d: %s" % (c, y)
      print "%s: %s:\t%d %.4f" % (asctime( localtime( y['when'] )), y['address'], y['status'], y['speed'])
      c = c + 1
   print '\n'
