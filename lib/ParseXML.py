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
def parseConfig(filename='poller.xml'):
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

