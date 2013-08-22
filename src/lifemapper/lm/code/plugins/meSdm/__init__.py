"""
@summary: This the Lifemapper Maximum Entropy Species Distribution Modeling 
             plugin
@author: CJ Grady
@contact: cjgrady [at] ku [dot] edu
@version: 1.0
@status: beta
@note: This was built for MaxEnt library 3.3.3e.  It may work with older or 
          newer versions.
"""

__version__ = "1.0"

jobTypes = [
            (3, 'meSdm.processRunner', 'MEModelRunner'), # MaxEnt model job runner
            (4, 'meSdm.processRunner', 'MEProjectionRunner') # MaxEnt projection job runner
           ]
