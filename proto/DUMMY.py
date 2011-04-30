import time
import logging

l = logging.getLogger("gslb")

# this is a basic stub that lets you fake a successful check
# to aid in balancing traffic with priorities across diverse systems
def get(data, queue, passCount, dbConfig):

   data['port'] = 0
   data['found'] = 1
   data['speed'] = 1
   data['when'] = time.time()
   data['pass'] = passCount
   data['reason'] = 'dummy'

#   queue.put((data['Type'], 0, data['name'], data['ip'], 1, 1, data['tag'], time.time(), passCount, reason, data['priority']))

   queue.put(data)

