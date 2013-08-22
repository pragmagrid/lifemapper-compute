"""
@summary: Module containing the job runners for Maximum Entropy models and 
             projections
@author: CJ Grady
@version: 1.0
@status: beta

@note: Commands are for maxent library version 3.3.3e
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

from config import JAVA_CMD, MDL_TOOL, ME_CMD, PRJ_TOOL
from constants import PARAMETERS
from common.layerManager import LayerManager
from jobRunners.base.applicationRunner import ApplicationRunner

# .............................................................................
class MEModelRunner(ApplicationRunner):
   """
   @summary: MaxEnt model job runner
   """
   # ...................................
   def _buildCommand(self):
      """
      @summary: Builds the command that will generate a model
      @return: A bash command to run
      
      @note: MaxEnt version 3.3.3e
      """
      baseCmd = "{0}{1} {0}{2} {3}".format(self.env.getApplicationPath(), 
                                                    JAVA_CMD, ME_CMD, MDL_TOOL)
      samples = "-s {0}".format(self.samplesFile)
      envParams = "-e {0}".format(self.jobLayerDir)
      outputParams = "-o {0}".format(self.jobOutputDir)
      algoOptions = getAlgorithmOptions(self.job.algorithm)
      options = "nowarnings autorun -z"
      # Application path, me command, model tool
      cmd = "{0} {1} {2} {3} {4} {5}".format(baseCmd, samples, envParams, 
                                            outputParams, algoOptions, options)
      return cmd
   
   # ...................................
   def _checkApplication(self):
      """
      @summary: Checks the openModeller output files to get the progress and 
                   status of the running model.
      """
      pass
   
   # ...................................
   def _checkOutput(self):
      """
      @summary: Checks the output of openModeller to see if any errors occurred
      """
      pass
   
   # ...................................
   def _cleanUp(self):
      """
      @summary: Cleans up after a job has completed.  This should deleting all
                   files created by the job that do not need to be kept on the
                   node.
      """
      try:
         import shutil
         shutil.rmtree(self.jobOutputDir)#, ignore_errors=True)
      except:
         pass

   # ...................................
   def _initializeJob(self):
      """
      @summary: Initializes a model to be ran by openModeller
      """
      self.dataDir = self.env.getJobDataPath()
      self.jobOutputDir = os.path.join(self.env.getJobOutputPath(), 
                                       "job-3-{0}".format(self.job.jobId))
      self.jobLayerDir = os.path.join(self.jobOutputDir, 'layers')
      self.samplesFile = os.path.join(self.jobOutputDir, 'samples.csv')
      self.lambdasFile = os.path.join(self.jobOutputDir, '{0}.lambdas'.format(self.job.points.displayName))
      
      if not os.path.exists(self.jobLayerDir):
         os.makedirs(self.jobLayerDir)
      
      # Layers
      handleLayers(self.job.layers, self.env, self.dataDir, self.jobLayerDir)
      # Points
      self._writePoints()
      
      # Logging?
      
   # .......................................
   def _push(self):
      """
      @summary: Pushes the results of the job to the job server
      """
      component = "model"
      contentType = "text/plain"
      content = open(self.lambdasFile).read()
      self._update()
      self.env.postJob(3, self.job.jobId, content, contentType, component)
   
   # ...................................
   def _writePoints(self):
      """
      @summary: Writes out the points of the job in a format MaxEnt can read
      """
      f = open(self.samplesFile, 'w')
      f.write("Species, X, Y\n")
      for pt in self.job.points:
         f.write("{0}, {1}, {2}\n".format(self.job.points.displayName, pt.x, pt.y))
      f.close()
      
# .............................................................................
class MEProjectionRunner(ApplicationRunner):
   """
   @summary: openModeller projection job runner
   """
   # .......................................
   def _buildCommand(self):
      """
      @summary: Builds the command that will generate a projection
      @note: MaxEnt version 3.3.3e
      @note: Usage: java -cp maxent.jar density.Project lambdaFile gridDir outFile [args]

Here lambdaFile is a .lambdas file describing a Maxent model, and gridDir is a 
directory containing grids for all the predictor variables described in the 
.lambdas file.  As an alternative, gridDir could be an swd format file.  The 
optional args can contain any flags understood by Maxent -- for example, a 
"grd" flag would make the output grid of density.Project be in .grd format.
      """
      baseCmd = "{0}{1} {0}{2} {3}".format(self.env.getApplicationPath(), 
                                                    JAVA_CMD, ME_CMD, PRJ_TOOL)
      outFile = os.path.join(self.jobOutputDir, 'output.asc')
      args = "autorun -z"
      #cmd = "{baseCmd} {lambdaFile} {gridDir} {outFile} {args}".format(
      #            baseCmd=baseCmd, gridDir=gridDir, outFile=outFile, args=args)
      cmd = "{0} {1} {2} {3} {4}".format(baseCmd, self.lambdasFile, 
                                               self.jobLayerDir, outFile, args)
      return cmd
   
   # .......................................
   def _checkApplication(self):
      """
      @summary: Checks the openModeller output files to get the progress and 
                   status of the running projection.
      """
      pass
      
   # .......................................
   def _checkOutput(self):
      """
      @summary: Checks the output of openModeller to see if any errors occurred
      """
      pass
   
   # ...................................
   def _cleanUp(self):
      """
      @summary: Cleans up after a job has completed.  This should deleting all
                   files created by the job that do not need to be kept on the
                   node.
      """
      try:
         import shutil
         shutil.rmtree(self.jobOutputDir)#, ignore_errors=True)
      except:
         pass

   # .......................................
   def _initializeJob(self):
      """
      @summary: Initializes a projection for generation
      """
      self.dataDir = self.env.getJobDataPath()
      self.jobOutputDir = os.path.join(self.env.getJobOutputPath(), 
                                       "job-4-{0}".format(self.job.jobId))
      self.jobLayerDir = os.path.join(self.jobOutputDir, 'layers')
      self.lambdasFile = os.path.join(self.jobOutputDir, 'input.lambdas')
      self.outputFile = os.path.join(self.jobOutputDir, 'output.asc')

      if not os.path.exists(self.jobLayerDir):
         os.makedirs(self.jobLayerDir)

      handleLayers(self.job.layers, self.env, self.dataDir, self.jobLayerDir)
      
      f = open(self.lambdasFile, 'w')
      f.write(self.job.lambdas)
      f.close()
      
      # Determine directories
      # Write lambdas file
      # Logging?
      # Statisitcs?
      # Output file
      

   # .......................................
   def _push(self):
      """
      @summary: Pushes the results of the job to the job server
      """
      component = "projection"
      contentType = "image/x-aaigrid"
      content = open(self.outputFile).read()
      self._update()
      self.env.postJob(4, self.job.jobId, content, contentType, component)




# .................................
def getAlgorithmOptions(algo):
   """
   @summary: Processes the algorithm parameters provided to generate 
                command-line options
   """
   params = []
   if algo.parameter is not None:
      for param in algo.parameter:
         p = processParameter(param.id, param.value)
         if p is not None:
            params.append(p)
   return ' '.join(params)
         
# .................................
def processParameter(param, value):
   """
   @summary: Processes an individual parameter and value
   """
   p = PARAMETERS[param]
   v = p['process'](value)
   if p.has_key('options'):
      v = p['options'][v]
   if v != p['default']:
      return "--{parameter}={value}".format(parameter=param, value=v)
   else:
      return None

# .................................
def handleLayers(layerUrls, env, dataDir, jobLayerDir):
   """
   @summary: Iterates through the list of layer urls and stores them on the 
                file system if they are not there yet.  Then creates links
                in the job layer directory so that the layers may be stored
                long term on the machine but still used per job.
   @param layerUrls: List of layer urls
   @param env: The environment to operate in
   @param dataDir: Directory to store layers
   @param jobLayerDir: The layer directory of the job
   """
   lyrs = []
   lyrMgr = LayerManager(dataDir)
   for lyrUrl in layerUrls:
      lyrs.append(lyrMgr.getLayerFilename(lyrUrl))
   lyrMgr.close()
   for i in range(len(lyrs)):
      env.createLink("{0}/layer{1}.asc".format(jobLayerDir, i), lyrs[i])

