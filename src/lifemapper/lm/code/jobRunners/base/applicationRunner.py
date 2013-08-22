"""
@summary: Module containing the application job runner class
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
from subprocess import Popen
from time import sleep

from jobRunner import JobRunner

from common.lmConstants import JobStatus
from common.lmObj import LmException

# Other
# ............................
WAIT_SECONDS = 30 # The number of seconds to wait, by default, between polling

# .............................................................................
class ApplicationRunner(JobRunner):
   """
   @summary: This class is a job runner that spawns off a 3rd party application
                to work on a job.
   """
   # ...................................
   def __init__(self, job, env):
      """
      @summary: Constructor
      @param jobType: The type of job to be run
      @param jobId: The id of the job to run
      @param env: The environment to run in
      """
      if self.__class__ == ApplicationRunner:
         raise Exception("Abstract class ApplicationRunner should not be instantiated.")
      JobRunner.__init__(self, job, env)
      self.status = JobStatus.PULL_COMPLETE
      self.progress = 0
   
   # ...................................
   def run(self):
      """
      @summary: Runs the application and periodically checks it
      """
      try:
         self._initializeJob()
         self._update()
         cmd = self._buildCommand()
         self._startApplication(cmd)
         self.status = JobStatus.RUNNING
         while not self._poll():
            self._checkApplication()
            self._update()
            self._wait()
         self._checkApplication()
         self._checkOutput()
         self._update()
         self._push()
         self._cleanUp()
      except LmException, lme:
         self.status = lme.code
         self._update()
      except Exception, e:
         print str(e)
         self.status = JobStatus.GENERAL_ERROR
         self._update()

   # ...................................
   def _buildCommand(self):
      """
      @summary: Builds a command to be ran for the job
      """
      return ""
   
   # ...................................
   def _checkApplication(self):
      """
      @summary: Checks a running application to get an updated progress and 
                   status
      """
      return True
   
   # ...................................
   def _checkOutput(self):
      """
      @summary: Checks the output of an application to see if any unexpected
                   errors occurred.
      """
      pass
   
   # ...................................
   def _cleanUp(self):
      """
      @summary: Cleans up after a job has completed.  This should deleting all
                   files created by the job that do not need to be kept on the
                   node.
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
   def _poll(self):
      """
      @summary: Polls the active subprocess running the application
      """
      if self.subprocess.poll() is not None:
         return True
      else:
         return False
   
   # ...................................
   def _push(self):
      """
      @summary: Posts the results of the job back to the server
      """
      pass
   
   # ...................................
   def _startApplication(self, cmd):
      """
      @summary: This method takes a bash command and starts up an application.
      """
      self.subprocess = Popen(cmd, shell=True)
      sleep(WAIT_SECONDS)
   
   # ...................................
   def _update(self):
      """
      @summary: Updates the job object in storage
      """
      print self.env.updateJob(self.job.jobType, self.job.jobId, self.status, self.progress)
      
   # ...................................
   def _wait(self):
      """
      @summary: Waits some amount of time so that the job runner isn't 
                   constantly polling the application and updating files.
      """
      sleep(WAIT_SECONDS)
         