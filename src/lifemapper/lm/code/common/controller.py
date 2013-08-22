"""
@summary: Module containing classes for controlling job submission
@author: CJ Grady
@version: 1.0
@status: beta

@license: gpl2
@license: Copyright (C) 2013, University of Kansas Center for Research

          Lifemapper Project, lifemapper [at] ku [dot] edu, 
          Biodiversity Institute,
          1345 Jayhawk Boulevard, Lawrence, Kansas, 66045, USA
   
          This program is free software; you can redistribute it and/or modify 
          it under the terms of the GNU General Public License as published by 
          the Free Software Foundation; either version 2 of the License, or (at 
          your option) any later version.
  
          This program is distributed in the hope that it will be useful, but 
          WITHOUT ANY WARRANTY; without even the implied warranty of 
          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
          General Public License for more details.
  
          You should have received a copy of the GNU General Public License 
          along with this program; if not, write to the Free Software 
          Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
          02110-1301, USA.
"""
from config import JOB_TYPES, LM_USER_JOB
from lmConstants import JobStatus
from environment.localEnv import LocalEnv

class JobController(object):
   """
   @summary: Controls how jobs are ran in this environment.  
   """
   
   # ......................................
   def __init__(self, env, jobTypes=JOB_TYPES.keys(), numJobs=1):
      self.env = env
      self.jobTypes = jobTypes
      self.numJobs = numJobs
   
   #.......................................
   def run(self):
      for _ in range(self.numJobs):
         j = self.env.requestJob(validTypes=self.jobTypes, 
                                 parameters={'users' : LM_USER_JOB})
         print "Job:", j.jobId
         self.env.updateJob(j.jobType, j.jobId, JobStatus.PULL_COMPLETE, None)
         jr = JOB_TYPES[int(j.jobType)]['constructor'](j, self.env)
         jr.run()
         
# .............................................................................
if __name__ == "__main__":
   import sys
   
   try:
      numJobs = int(sys.argv[1])
   except:
      numJobs = 1
   
   env = LocalEnv()
   jc = JobController(env, numJobs=numJobs)
   jc.run()