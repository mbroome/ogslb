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

import getopt

from time import *
from TimeSeries import *
from Stats import *
import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

def getData(fields):
   t = TimeSeries()
   s = Stats()

   r = s.sget("stats.hostlist")

   for i in r:
      print "Hostname: %s" % i
      line = "when\t\t\t\t"
      for f in fields:
         if f != 'when':
            line += f +"\t" 
      print "%s" % line

      x = t.zget(i)
      for y in x:
         line = "%s" % asctime( localtime( y['when'] )) 
         line += "\t"
         for f in fields:
            if f != 'when':
               try:
                  if type(y[f]) == 'int':
                     line += y[f] + "\t"
                  elif type(y[f]) == 'float':
                     line += "%.2f" % y[f]
                     line += "\t"
                  else:
                     line += str(y[f]) + "\t"
               except:
                  line += "-\t"
         print "%s" % line
      print '\n'


def usage():
   print """cli.py: command line client for ogslb
Mitchell Broome (mitchell.broome@gmail.com)

cli.py [-f=field1,field2] [-h]

-f      Comma separated list of fields to display (default: status,address,speed)
	Field names come from attributes defined in poller.xml for each poller
-h      Print help

"""



def main(argv):

   # parse the command line arguments
   try:
      opts, args = getopt.getopt(argv, "hf:n:", ['help', 'fields=', 'name'])
   except getopt.GetoptError:
      sys.exit(2)

   field = 'status,address,speed'
   name = ''
   # override defaults based on command line arguments
   for opt, arg in opts:
      if opt in ('-h', '--help'):
         usage()
         sys.exit()
      elif opt == '-f':
         field = arg
      elif opt == '-n':
         name = arg

   fields = field.split(',');
   getData(fields)


if __name__ == "__main__":
   main(sys.argv[1:])


