"""
@summary: Module containing the job runners for openModeller models and 
             projections
@author: CJ Grady
@version: 2.0
@status: beta

@note: Commands are for openModeller library version 1.3.0
@note: Commands may be backwards compatible

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
import os

from jobRunners.base.applicationRunner import ApplicationRunner
from config import DEFAULT_LOG_LEVEL, OM_MODEL_CMD, OM_PROJECT_CMD
from constants import JobStatus
from omRequest import OmModelRequest, OmProjectionRequest


# .............................................................................
class OMModelRunner(ApplicationRunner):
   """
   @summary: openModeller model job runner
   """
   # ...................................
   def _buildCommand(self):
      """
      @summary: Builds the command that will generate a model
      @return: A bash command to run
      
      @note: om_model version 1.3.0
      @note: Usage - om_model [options [args]]
         --help,       -h          Displays this information
         --version,    -v          Display version info
         --xml-req,    -r <args>   Model creation request file in XML
         --model-file, -m <args>   File to store the generated model
         --log-level <args>        Set the log level (debug, warn, info, error)
         --log-file <args>         Log file
         --prog-file <args>        File to store model creation progress
      """
      cmd = "%s%s -r %s -m %s --log-level %s --log-file %s --prog-file %s" % \
               (self.env.getApplicationPath(), OM_MODEL_CMD, 
                self.modelRequestFile, self.modelResultFile,
                self.modelLogLevel, self.modelLogFile, self.modelProgressFile)
      return cmd
   
   # ...................................
   def _checkApplication(self):
      """
      @summary: Checks the openModeller output files to get the progress and 
                   status of the running model.
      """
      f = open(self.modelProgressFile)
      self.progress = int(''.join(f.readlines()))
      f.close()
   
   # ...................................
   def _checkOutput(self):
      """
      @summary: Checks the output of openModeller to see if any errors occurred
      """
      if self.progress == -2:
         self.status = self._getModelErrorStatus()
      elif self.progress == 100:
         self.status = JobStatus.COMPUTED
      else:
         # Probably a seg fault or killed by signal
         self.status = self._getModelErrorStatus()
         
   # ...................................
   def _cleanUp(self):
      """
      @summary: Cleans up after a job has completed.  This should deleting all
                   files created by the job that do not need to be kept on the
                   node.
      """
      try:
         import shutil
         shutil.rmtree(self.outputPath)#, ignore_errors=True)
      except:
         pass
   
   # ...................................
   def _initializeJob(self):
      """
      @summary: Initializes a model to be ran by openModeller
      """
      self.outputPath = os.path.join(self.env.getJobOutputPath(), 
                                     'job-1-%s' % self.job.jobId)
      
      if not os.path.exists(self.outputPath):
         os.makedirs(self.outputPath)

      self.modelLogFile = "%s/modLog-%s.log" % (self.outputPath, self.job.jobId)
      self.modelProgressFile = "%s/modProg-%s.txt" % (self.outputPath, self.job.jobId)
      self.modelRequestFile = "%s/modReq-%s.xml" % (self.outputPath, self.job.jobId)
      self.modelResultFile = "%s/mod-%s.xml" % (self.outputPath, self.job.jobId)

      self.modelLogLevel = DEFAULT_LOG_LEVEL
      
      # Generate a model request file and write it to the file system
      req = OmModelRequest(self.job, self.env.getJobDataPath())
      reqFile = open(self.modelRequestFile, "w")
      reqFile.write(req.generate())
      reqFile.close()
      self.status = JobStatus.COMPUTE_INITIALIZED
   
   # .......................................
   def _getModelErrorStatus(self):
      """
      @summary: Checks the model log file to determine what error occurred. 
      """
      f = open(self.modelLogFile)
      omLog = ''.join(f.readlines())
      f.close()
      
      status = JobStatus.UNKNOWN_ERROR
      
      if omLog.find("[Error] No presence points available") >= 0:
         status = JobStatus.OM_MOD_REQ_POINTS_MISSING_ERROR
      elif omLog.find(
          "[Error] Cannot use zero presence points for sampling") >= 0:
         status = JobStatus.OM_MOD_REQ_POINTS_MISSING_ERROR
      elif omLog.find(
          "[Error] Cannot create model without any presence or absence point."
          ) >= 0:
         status = JobStatus.OM_MOD_REQ_POINTS_OUT_OF_RANGE_ERROR
      elif omLog.find("[Error] XML Parser fatal error: not well-formed") >= 0:
         status = JobStatus.OM_MOD_REQ_ERROR
      elif omLog.find("[Error] Unable to open file") >= 0:
         status = JobStatus.OM_MOD_REQ_LAYER_ERROR
      elif omLog.find("[Error] Algorithm %s not found" % \
                                            self.job.algoCode) >= 0:
         status = JobStatus.OM_MOD_REQ_ALGO_INVALID_ERROR
      elif omLog.find("[Error] Parameter") >= 0:
         if omLog.find("not set properly.\n", 
                                         omLog.find("[Error] Parameter")) >= 0:
            status = JobStatus.OM_MOD_REQ_ALGOPARAM_MISSING_ERROR
      return status
   
   # .......................................
   def _push(self):
      """
      @summary: Pushes the results of the job to the job server
      """
      if self.status < JobStatus.GENERAL_ERROR:
         self.status = JobStatus.PUSH_REQUESTED
         component = "model"
         contentType = "application/xml"
         content = open(self.modelResultFile).read()
         self._update()
         self.env.postJob(1, self.job.jobId, content, contentType, component)
      else:
         component = "error"
         content = None
   
# .............................................................................
class OMProjectionRunner(ApplicationRunner):
   """
   @summary: openModeller projection job runner
   """
   # .......................................
   def _buildCommand(self):
      """
      @summary: Builds the command that will generate a projection
      @note: om_project version 1.3.0
      @note: Usage: om_project [options [args]]
        --help,      -h          Displays this information
        --version,   -v          Display version info
        --xml-req,   -r <args>   Projection request file in XML
        --model,     -o <args>   File with serialized model (native projection)
        --template,  -t <args>   Raster template for the distribution map 
                                    (native projection)
        --format,    -f <args>   File format for the distribution map 
                                    (native projection)
        --dist-map,  -m <args>   File to store the generated model
        --log-level <args>       Set the log level (debug, warn, info, error)
        --log-file <args>        Log file
        --prog-file <args>       File to store projection progress
        --stat-file <args>       File to store projection statistics
      """
      cmd = "%s%s -r %s -m %s --log-level %s --log-file %s --prog-file %s --stat-file %s" % \
            (self.env.getApplicationPath(), OM_PROJECT_CMD, 
             self.projRequestFile, self.projResultFile,
             self.projLogLevel, self.projLogFile, self.projProgressFile,
             self.projStatFile)
      return cmd
   
   # .......................................
   def _checkApplication(self):
      """
      @summary: Checks the openModeller output files to get the progress and 
                   status of the running projection.
      """
      f = open(self.projProgressFile)
      self.progress = int(''.join(f.readlines()))
      f.close()
      
   # .......................................
   def _checkOutput(self):
      """
      @summary: Checks the output of openModeller to see if any errors occurred
      """
      if self.progress == -2:
         self.status = self._getProjectionErrorStatus()
      elif self.progress == 100:
         self.status = JobStatus.COMPUTED
      else:
         # Probably a seg fault or killed by signal
         self.status = self._getProjectionErrorStatus()
   
   # .......................................
   def _getProjectionErrorStatus(self):
      """
      @summary: Checks the projection log file to determine what error occurred
      @todo: Look for errors in log file
      """
      #f = open(self.projLogFile)
      #omLog = ''.join(f.readlines())
      #f.close()
      
      # Need to look for specific projection errors
      status = JobStatus.OM_PROJECTION_ERROR
      
      return status
   
   # .......................................
   def _initializeJob(self):
      """
      @summary: Initializes a projection for generation
      """
      self.outputPath = os.path.join(self.env.getJobOutputPath(), 
                                     'job-2-%s' % self.job.jobId)
      
      if not os.path.exists(self.outputPath):
         os.makedirs(self.outputPath)

      self.projLogFile = "%s/projLog-%s.log" % (self.outputPath, self.job.jobId)
      self.projLogLevel = DEFAULT_LOG_LEVEL
      self.projProgressFile = "%s/projProg-%s.txt" % (self.outputPath, self.job.jobId)
      self.projRequestFile = "%s/projReq-%s.xml" % (self.outputPath, self.job.jobId)
      self.projResultFile = "%s/proj-%s.tif" % (self.outputPath, self.job.jobId)
      self.projStatFile = "%s/projStats-%s.txt" % (self.outputPath, self.job.jobId)
      
      # Generate a projection request file and write it to the file system
      req = OmProjectionRequest(self.job, self.env.getJobDataPath())
      reqFile = open(self.projRequestFile, "w")
      reqFile.write(req.generate())
      reqFile.close()
      self.status = JobStatus.COMPUTE_INITIALIZED

   # ...................................
   def _cleanUp(self):
      """
      @summary: Cleans up after a job has completed.  This should deleting all
                   files created by the job that do not need to be kept on the
                   node.
      """
      try:
         import shutil
         shutil.rmtree(self.outputPath)#, ignore_errors=True)
      except:
         pass

   # .......................................
   def _push(self):
      """
      @summary: Pushes the results of the job to the job server
      """
      if self.status < JobStatus.GENERAL_ERROR:
         self.status = JobStatus.PUSH_REQUESTED
         component = "projection"
         contentType = "image/tiff"
         content = open(self.projResultFile).read()
         self._update()
         self.env.postJob(2, self.job.jobId, content, contentType, component)
      else:
         component = "error"
         content = None
