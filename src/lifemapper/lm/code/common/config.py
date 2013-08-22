"""
@summary: Location of local configuration options
@author: CJ Grady
@contact: cjgrady [at] ku [dot] edu
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
# ============================================================================
# =                            Contact Information                           =
# ============================================================================
INSTITUTION_NAME = "" # The name of your institution / organization
ADMIN_NAME = "" # We will contact this person if we have important information
ADMIN_EMAIL = "" #     such as version updates or troubleshooting
LOCAL_MACHINE_ID = "" # Identifier that is meaningful to you for this machine
                      #    if we need to contact you about a machine, we will 
                      #    use this
# ----------------------------------------------------------------------------

# ============================================================================
# =                         Environment Configuration                        =
# ============================================================================
# Location of plugins directory
PLUGINS_DIR = "/var/lm/code/plugins"

# Application directory
APP_PATH = "/var/lm/apps/"

# Place to store job input data
JOB_DATA_PATH = "/var/lm/data/"

# Where job output should be written
JOB_OUTPUT_PATH = "/var/lm/jobs/"

# User jobs, fill this in to only process a certain user's jobs
LM_USER_JOB = 'lm2'

# Job Types
def getJobTypes():
   """
   @summary: Uses introspection to determine what job types are available to 
                this system
   """
   import os
   pluginsDir = PLUGINS_DIR
   pluginsNS = 'plugins'
   jobTypes = {}
   jobImports = []
   for f in os.listdir(pluginsDir):
      try:
         m = __import__('{pluginsNS}.{plugin}'.format(pluginsNS=pluginsNS, 
                                             plugin=f), fromlist='jobTypes')
         jobImports.extend(m.jobTypes)
      except Exception, e: # Skip if not a valid plugin
         # print e # Uncomment if no plugins are showing up
         pass
   for jobTypeId, namespace, name in jobImports:
      jt = __import__('{pluginsNS}.{ns}'.format(pluginsNS=pluginsNS, 
                                                  ns=namespace), fromlist=name)
      jobTypes[jobTypeId] = {
                             'id': jobTypeId, 
                             'name': name, 
                             'constructor': jt.__getattribute__(name)
                            }
   return jobTypes
# ----------------------------------------------------------------------------

                      
JOB_TYPES = getJobTypes()
