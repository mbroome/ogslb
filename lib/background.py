import os
import sys

def createDaemon():
   UMASK = 0
   WORKDIR = "/"
#   MAXFD = 1024
#
#   if (hasattr(os, "devnull")):
#      REDIRECT_TO = os.devnull
#   else:
#      REDIRECT_TO = "/dev/null"


   try:
      pid = os.fork()
   except OSError, e:
      raise Exception, "%s [%d]" % (e.strerror, e.errno)

   if (pid == 0):	# The first child.
      os.setsid()

      try:
         pid = os.fork()	# Fork a second child.
      except OSError, e:
         raise Exception, "%s [%d]" % (e.strerror, e.errno)

      if (pid == 0):	# The second child.
         os.chdir(WORKDIR)
         os.umask(UMASK)
      else:
         os._exit(0)	# Exit parent (the first child) of the second child.
   else:
      os._exit(0)	# Exit parent of the first child.

#   import resource		# Resource usage information.
#   maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
#   if (maxfd == resource.RLIM_INFINITY):
#      maxfd = MAXFD
  
   # Iterate through and close all file descriptors.
   for fd in range(0, 2):
      try:
         os.close(fd)
      except OSError:	# ERROR, fd wasn't open to begin with (ignored)
         pass

#   os.open(REDIRECT_TO, os.O_RDWR)	# standard input (0)

#   os.dup2(0, 1)			# standard output (1)
#   os.dup2(0, 2)			# standard error (2)

   return(0)


