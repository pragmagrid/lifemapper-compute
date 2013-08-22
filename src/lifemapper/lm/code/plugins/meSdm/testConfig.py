"""
@summary: Test's the Lifemapper MaxEnt configuration
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
import os
import subprocess

from config import ME_CMD, MDL_TOOL, PRJ_TOOL
from environment.localEnv import LocalEnv
from plugins.meSdm.processRunner import MEModelRunner, MEProjectionRunner

## -----------------------------------------------------------------------------
#def testOmModel(env):
#   """
#   @summary: Tests that the openModeller model generation binary can be called
#   @param env: An environment class to test
#   """
#   appBase = env.getApplicationPath()
#   cmd = "%s%s --version" % (appBase, OM_MODEL_CMD)
#   retCode = subprocess.call(cmd, shell=True)
#   if retCode != 0:
#      raise Exception ("Call to: %s returned exit code: %s, expected 0" % \
#                               (cmd, retCode))
#
## -----------------------------------------------------------------------------
#def testOmProject(env):
#   """
#   @summary: Tests that the openModeller projection generation binary can be 
#                called
#   @param env: An environment class to test
#   """
#   appBase = env.getApplicationPath()
#   cmd = "%s%s --version" % (appBase, OM_PROJECT_CMD)
#   retCode = subprocess.call(cmd, shell=True)
#   if retCode != 0:
#      raise Exception ("Call to: %s returned exit code: %s, expected 0" % \
#                               (cmd, retCode))
#
## -----------------------------------------------------------------------------
#def testInputDirectory(env):
#   """
#   @summary: Tests that the job input directories can be written to
#   @param env: An environment class to test
#   """
#   oDir = env.getJobDataPath()
#   fn = "%s%s" % (oDir, 'write_test.txt')
#   f = open(fn, 'w')
#   f.write('test')
#   f.close()
#   os.remove(fn)
#
## -----------------------------------------------------------------------------
#def testOutputDirectory(env):
#   """
#   @summary: Tests that the job output directories can be written to
#   @param env: An environment class to test
#   """
#   oDir = env.getJobOutputPath()
#   fn = "%slayers/%s" % (oDir, 'write_test.txt')
#   f = open(fn, 'w')
#   f.write('test')
#   f.close()
#   os.remove(fn)

# -----------------------------------------------------------------------------
def testRunModelJob(env):
   """
   @summary: Attempts to run a model job
   @param env: An environemnt class to test
   """
   j = env.requestJob(validTypes=[3], parameters={'users': 'lm2'})
   jr = MEModelRunner(j, env)
   jr.run()

# -----------------------------------------------------------------------------
def testRunProjectionJob(env):
   """
   @summary: Attempts to run a projection job
   @param env: An environemnt class to test
   """
   j = env.requestJob(validTypes=[4], parameters={'users': 'lm2'})
   jr = MEProjectionRunner(j, env)
   jr.run()

# -----------------------------------------------------------------------------
def runTests(env=None):
   """
   @summary: Runs the tests associated with the Lifemapper openModeller plugin
   @param env: (optional) The environment to test in
   """
   if env is None:
      env = LocalEnv()
#   testOmModel(env)
#   testOmProject(env)
#   testInputDirectory(env)
#   testOutputDirectory(env)
   testRunModelJob(env)
   testRunProjectionJob(env)

# ============================================================================
if __name__ == '__main__':
   runTests()
   