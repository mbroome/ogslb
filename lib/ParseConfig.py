import xml.dom.minidom
import logging
import pprint

pp = pprint.PrettyPrinter(indent=4)
l = logging.getLogger("ogslb")

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def parseConfig(filename='config.xml'):
   dom = xml.dom.minidom.parse(filename);
   config = {}
   try:
      dbc = dom.getElementsByTagName('CONFIG')[0]
      for a in dbc.attributes.keys():
         config[a] = dbc.attributes[a].value
   except:
      l.debug("error getting config")


   return(config)

