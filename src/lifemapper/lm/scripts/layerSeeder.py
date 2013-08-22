"""
@summary: This script is used to seed layers into the layers database for a 
             compute resource so that they are not downloaded unnecessarily
@author: CJ Grady
@version: 1.0
@status: alpha
"""
import sys

from common.layerManager import LayerManager

DATA_DIR = "/var/lm/data/"

def processFile(fn):
   f = open(fn)
   lyrs = [tuple(line.split(', ')) for line in f.readlines()]
   f.close()
   return lyrs

# .............................................................................
if __name__ == "__main__":
   if len(sys.argv) < 2:
      print "Usage: python layerSeeder.py file"
      print "   File should be pairs of url, local file path separated by line feeds"
   else:
      lyrFile = sys.argv[1]
   lm = LayerManager(DATA_DIR)
   
   for url, fn in processFile(lyrFile):
      lm.seedLayer(url.strip(), fn.strip())
   
   lm.close()
   
