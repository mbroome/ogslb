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
from subprocess import *
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))

# account for where we live
sys.path.append(scriptPath + '/..')
sys.path.append(scriptPath + '/../lib')

import pprint
pp = pprint.PrettyPrinter(indent=4)

# this is a very basic program to test backend.py.  We effectivly emulate the
# PowerDNS protocol and talk to it on stdout and read back from stdin.
# Basically, just call this with a hostname as an argument
if __name__ == '__main__':
   host = ''
   try:
      host = sys.argv[1]
   except:
      print "need a hostname to lookup";
      sys.exit()

   try:
      scriptName = scriptPath + '/backend.py'
      p = Popen(scriptName, shell=True, bufsize=256, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True) 
#      p = Popen(scriptName, shell=True, bufsize=256, stdin=PIPE, stdout=PIPE, close_fds=True) 
      (child_stdin, child_stdout) = (p.stdin, p.stdout)

      child_stdin.write('HELO\t1\n');
      child_stdin.flush()
      l = child_stdout.readline()
      print l
      child_stdin.write('Q\t%s\tIN\tANY\t-1\t127.0.0.1\n' % host);
      child_stdin.flush()
      l = child_stdout.readline()
      print l

      p.close()
   except:
      ''' '''
