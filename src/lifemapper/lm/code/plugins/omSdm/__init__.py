"""
@summary: This the Lifemapper openModeller Species Distribution Modeling plugin
@author: CJ Grady
@contact: cjgrady [at] ku [dot] edu
@version: 2.0
@status: beta
@note: This was built for openModeller library 1.3.0.  It may work with older
          or newer versions.
"""

__version__ = "2.0"

jobTypes = [
            (1, 'omSdm.processRunner', 'OMModelRunner'), # openModeller model job runner
            (2, 'omSdm.processRunner', 'OMProjectionRunner') # openModeller projection job runner
           ]
