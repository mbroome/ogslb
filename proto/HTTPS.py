import socket
import time
import re
import pprint
import logging
import string 
from random import Random

l = logging.getLogger("ogslb")

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

import urllib2

pp = pprint.PrettyPrinter(indent=4)

# do the actual http get and return headers
def getUrl(url, headers):
   rheaders = {}
   ret = None
   code = 0
   req = urllib2.Request(url,None,headers)
   try:
      response = urllib2.urlopen(req)
      code = response.code
      rheaders = response.info()
   except urllib2.HTTPError, e:
      code = e.code
      rheaders = e.info()
      ret = e.read()
   except IOError, e:
      if hasattr(e, 'reason'):
         reason = e.reason
      elif hasattr(e, 'code'):
         code = e.code
         rheaders = e.info()
      else:
         pp.pprint(e)
         pp.pprint(e.reason)

   try:
      ret = response.read()
   except:
      # response error
      pass
   return((ret,code,rheaders))

      
# deal with preparing to get the content and handling it's response
def get(data, queue, passCount, Config):
   reason = ''
   headers = {'Host': data['name']}
   
   try: # if there was a response defined to look for, make a regex
      prog = re.compile(data['response']);
      checkResponse = 1
   except: # otherwise disable the content match and just look at status codes
      checkResponse = 0

   # format the url
   try:
      url = 'https://' + data['ip'] + ":" + data['port'] + data['url']
   except:
      url = 'https://' + data['ip'] + data['url']
      data['port'] = 80

   # do the get and time it
   t1 = time.time()
   r, code, rheaders = getUrl(url, headers)
   t2 = time.time()

   # if we are doing a content match, get busy
   if checkResponse == 1:
      try:
         if code >= 400:
            found = 0
         elif prog.search(r):
            found = 1
         else:
            found = 0
      except:
         found = 0
   else: # otherwise, handle the return code
      if code >= 400:
         found = 0
      else:
         found = 1
   data['speed'] = ((t2-t1)*1000.0)

   # If the get wasn't sucessful, figure out why
   if found == 0:
      errorID = ''.join( Random().sample(string.letters+string.digits, 12) )
      if data['speed'] >= 10000: # too slow
         reason = 'timeout'
      elif code >= 400: # got a status code over 400
         reason = "status: \"" + str(code) + "\" saved error: " + data['Type'] + '-' + str(data['port']) + '/' + data['name'] + '/' + errorID

      elif r != None: # got content but it didn't match
         reason = "content match: \"" + data['response'] + "\" saved error: " + data['Type'] + '-' + str(data['port']) + '/' + data['name'] + '/' + errorID
      elif (code == 0) and (data['speed'] < 10000):
         reason = "funk: code=0 and speed: " + str(data['speed'])
      else: # what the heck happened...
         reason = "content match error" + " saved error: " + data['Type'] + '-' + str(data['port']) + '/' + data['name'] + '/' + errorID


   data['status'] = found
   data['when'] = t1
   data['pass'] = passCount
   data['reason'] = reason

   # throw the collected data in the queue to be jammed into the database
   queue.put(data)

