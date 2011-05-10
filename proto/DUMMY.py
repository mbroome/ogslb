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


import time
import logging

logger = logging.getLogger("ogslb")

# this is a basic stub that lets you fake a successful check
# to aid in balancing traffic with priorities across diverse systems
def get(data, queue, passCount, Config):

   data['port'] = 0
   data['found'] = 1
   data['speed'] = 1
   data['when'] = time.time()
   data['pass'] = passCount
   data['reason'] = 'dummy'

   queue.put(data)

