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

import xml.dom.minidom
import logging
import pprint

# setup pprint for debugging
pp = pprint.PrettyPrinter(indent=4)

# and fire up the logger
logger = logging.getLogger("ogslb")

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

# parse the xml for pollers
def parseXML(filename='poller.xml'):
   dom = xml.dom.minidom.parse(filename);
   vips = {}

   logger.debug("parsing poller config: %s" % filename)
   try:
      vipsData = dom.getElementsByTagName("VIP")

      for vip in vipsData:
         v = {}
         i = []
         v['data'] = []
         if vip.hasAttributes():
            vname = vip.attributes['name'].value;
         poll = vip.getElementsByTagName("Poll");
         for p in poll:
            if p.hasAttributes():
               pollData = {}
               for k in p.attributes.keys():
                  pollData[k] = p.attributes[k].value
               pollData['name'] = vname
               try:
                  if pollData['tag'] == None:
                     pollData['tag'] = ''
               except:
                     pollData['tag'] = ''
               v['data'].append(pollData);
            vips[vname] = v
   except:
      logger.info("error finding vip configs")

   return(vips)

