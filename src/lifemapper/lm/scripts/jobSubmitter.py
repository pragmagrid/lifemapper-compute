"""
@summary: Simple script that submits jobs to a cluster via SGE's qsub
@author: CJ Grady
@version: 1.0
@status: alpha
"""
import os
from time import sleep

# =============================================================================
# =                           Configuration Options                           =
# =============================================================================
KILL_FILE = "submitter.die"
QSTAT_CMD = "qstat"
QSUB_CMD = "qsub -S /bin/bash -v PYTHONPATH=/var/lm/code -j y -o /dev/null runLmJob.sh"
#QSUB_CMD = "qsub -S /bin/bash -v PYTHONPATH=/var/lm/code -j y -o output/ runLmJob.sh"

DEFAULT_QUEUE_SIZE = 20
SLEEP_TIME = 30 # Number of seconds to sleep between polls

# .............................................................................
def numQstatProcesses():
   """
   @summary: Determines the number of processes running via qstat
   """
   res = os.popen(QSTAT_CMD)
   numLines = res.readlines()
   numProc = len(numLines)-2 if len(numLines) > 2 else 0
   res.close()
   return numProc

# .............................................................................
def run(queueSize=DEFAULT_QUEUE_SIZE):
   """
   @summary: Runs the job submitter
   @param queueSize: The number of processes to keep in the queue
   @param jobsPerProcess: The number of jobs to run per process
   """
   if os.path.exists(KILL_FILE):
      os.remove(KILL_FILE)
      
   while not os.path.exists(KILL_FILE):
      numToSubmit = queueSize - numQstatProcesses()
      print "Need to submit {0} processes".format(numToSubmit)
      if numToSubmit < 0:
         numToSubmit = 0
      for i in range(numToSubmit):
         print "Submitting job"
         res = os.popen(QSUB_CMD)
         res.close()
      # Sleep
      print "Sleep"
      sleep(SLEEP_TIME)

   print "Done"
   
# .............................................................................
if __name__ == "__main__":
   import sys
   try:
      queueSize = int(sys.argv[1])
   except:
      queueSize = DEFAULT_QUEUE_SIZE
   
   run(queueSize=queueSize)
   
