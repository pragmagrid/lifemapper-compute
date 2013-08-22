"""
@summary: Module containing the python job runner base class
@author: CJ Grady
@version: 2.0
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
from jobRunner import JobRunner
from common.lmConstants import JobStatus
from common.lmObj import LmException

class PythonRunner(JobRunner):
   """
   @summary: This is the base class for Job Runners that run python code to 
                work on a job.
   """
   def __init__(self, job, env):
      self.job = job
      self.env = env()
      
   def run(self):
      try:
         self._initializeJob()
         self.status = JobStatus.INITIALIZE
         self._update()
         self._doWork()
         self.status = JobStatus.COMPUTED
         self._update()
         self._push()
         self._cleanUp()
      except LmException, lme:
         self.status = lme.code
         self._update()
         self.log.error(str(lme))
      except Exception, e:
         self.status = JobStatus.GENERAL_ERROR
         self._update()
         self.log.error(str(e))
   
   # ...................................
   def _doWork(self):
      """
      @summary: Does the work for the process
      """
      pass
   
   # ...................................
   def _cleanUp(self):
      """
      @summary: Cleans up after a job has completed.  This should deleting all
                   files created by the job that do not need to be kept.
      """
      pass
   
   # ...................................
   def _initializeJob(self):
      """
      @summary: This method initializes a job.  This may include writing out 
                   parameter files to the file system or other initialization
                   tasks.
      """
      pass
   
   # ...................................
   def _push(self):
      """
      @summary: Pushes the results of the job to the job server
      """
      pass
   
   # ...................................
   def _update(self):
      """
      @summary: Updates the job object in storage
      """
      if self.env.updateJob(self.job.jobType, self.job.id, self.status, self.progress):
         print "Successfully update status"
      
