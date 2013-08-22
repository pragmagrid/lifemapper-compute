"""
@summary: Module containing compute environment layer management code
@author: CJ Grady
@status: beta
@version: 1.0
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
from hashlib import md5
import os
from osgeo import gdal, gdalconst
import sqlite3
from time import sleep
import urllib2

from lmConstants import JobStatus
from lmObj import LmException

TIMEOUT = 600
WAIT_SECONDS = 30

# .............................................................................
class LayerManager(object):
   """
   @summary: Manages the storage of layers on the file system through sqlite
   """
   # .................................
   def __init__(self, dataDir):
      dbFile = os.path.join(dataDir, "layers", "layers.db")
      self.lyrBasePath = os.path.join(dataDir, "layers")
      createDb = False
      if not os.path.exists(dbFile):
         createDb = True
      self.con = sqlite3.connect(dbFile, isolation_level=None)
      if createDb:
         self._createLayerDb()
   
   # .................................
   def close(self):
      self.con.close()
      
   # .................................
   def getLayerFilename(self, layerUrl):
      """
      @summary: Gets the path to the file created when storing the layer found
                   at the web address specified by layerUrl.  This layer is
                   downloaded and information is stored in the database.
      """
      #print "%s: %s" % (logId, lyr)
      host, key = self._getLayerUrlParts(layerUrl)
      
      fn = os.path.join(self.lyrBasePath, host, key)
      
      # Gets the status of the layer on the node (
      #     0: exists and writing by another process, 
      #     1: exists and stored, 
      #     2: new)
      insertStatus = self._getOrInsertLayer(host, key)
      
      if insertStatus == 1:
         # Layer exists and is stored
         pass
      elif insertStatus == 0:
         # Layer exists but has not been stored
         waitTime = 0
         while self._getOrInsertLayer(host, key) != 1 and waitTime < TIMEOUT:
            sleep(WAIT_SECONDS)
            waitTime = waitTime + WAIT_SECONDS
         if waitTime >= TIMEOUT:
            raise LmException(JobStatus.IO_WAIT_ERROR, "Layer took too long write: {0}, {1}".format(layerUrl, fn))
      elif insertStatus == 2:
         # Write file
         if self._writeLayer(layerUrl, fn):
            self._updateLayerAsStored(host, key)
         else:
            #TODO: delete layer if failed to write
            self._deleteLayer(layerUrl)
            raise LmException(JobStatus.IO_WRITE_ERROR, "Failed to write layer: {0}".format(layerUrl))
      else:
         raise LmException(JobStatus.DB_READ_ERROR, "Unknown insertion status: {0}".format(insertStatus))
      return fn
   
   # .................................
   def seedLayer(self, layerUrl, localFile):
      """
      @summary: Seeds the layer database with a layer file that is already 
                   stored on the local system.  This prevents extra downloads
                   of data when it is already present
      @param layerUrl: The url to be used for the database
      @param localFile: The local file location of this layer
      @note: To remain consistent with the rest of the layers, a symbolic link
                will be created for the layer rather than storing a location
                in the database
      """
      host, key = self._getLayerUrlParts(layerUrl)
      
      fn = os.path.join(self.lyrBasePath, host, key)
   
      # Gets the status of the layer on the node (
      #     0: exists and writing by another process, 
      #     1: exists and stored, 
      #     2: new)
      insertStatus = self._getOrInsertLayer(host, key)
      
      if insertStatus == 1:
         # Layer exists and is stored
         pass
      elif insertStatus == 0:
         # Layer exists but has not been stored
         waitTime = 0
         while self._getOrInsertLayer(host, key) != 1 and waitTime < TIMEOUT:
            sleep(WAIT_SECONDS)
            waitTime = waitTime + WAIT_SECONDS
         if waitTime >= TIMEOUT:
            raise LmException(JobStatus.IO_WAIT_ERROR, "Layer took too long write: {0}, {1}".format(layerUrl, fn))
      elif insertStatus == 2:
         # Write file
         fDir = os.path.dirname(fn)
         if not os.path.exists(fDir):
            os.mkdir(fDir)
         os.symlink(localFile, fn)
         self._updateLayerAsStored(host, key)
      else:
         raise LmException(JobStatus.DB_READ_ERROR, "Unknown insertion status: {0}".format(insertStatus))
      return fn

   # .................................
   def _createLayerDb(self):
      """
      @summary: Attempts to create a layers database table
      """
      try:
         self.con.execute("CREATE TABLE layers(host TEXT, paramhash TEXT, stored INT, PRIMARY KEY (host, paramhash))")
      except:
         pass

   # .................................
   def _deleteLayer(self, hostname, key):
      """
      @summary: Deletes a layer from the database
      @param hostname: The name of the layer host
      @param key: The key for the layer
      @note: This could be useful if the layer failed to store
      """
      with self.con:
         cur = self.con.cursor()
         cur.execute("DELETE FROM layers WHERE host='{host}' AND paramhash='{key}'".format(host=hostname, key=key))
      
   # .................................
   def _getLayerUrlParts(self, layerUrl):
      """
      @summary: Breaks a url into host name and parameters and then returns the 
                   hash of the set of url parameters (ensures a unique key for any 
                   given set of url parameters even in a different order)
      """
      parts = layerUrl.split("?")
      # remove trailing slash and leading http:// if present
      host = parts[0].strip('/').replace('http://', '').replace('/', '_')
      params = set([tuple(param.split('=')) for param in parts[1].split('&')])
      key = md5(str(params)).hexdigest()
      
      return host, key 

   # .................................
   def _getOrInsertLayer(self, hostname, key):
      """
      @summary: Inserts a layer into the database.
      @return: Returns, 0: inserted by another process and not stored
                        1: inserted and stored on file system
                        2: new
      """
      try:
         with self.con:
            # check to see if layer exists
            cur = self.con.cursor()
            cur.execute("SELECT stored FROM layers WHERE host = '{host}' AND paramhash = '{key}'".format(host=hostname, key=key))
            rows = cur.fetchall()
            if len(rows) == 0:
               # New insert
               cur.execute("INSERT into layers VALUES ('{host}', '{key}', 0)".format(host=hostname, key=key))
               ret = 2
            else:
               ret = rows[0][0] # 0 if not stored, 1 if stored
      except sqlite3.IntegrityError: # Item was inserted between statements
         ret = 0
      return ret

   # .................................
   def _updateLayerAsStored(self, hostname, key):
      """
      @summary: Marks the layer as stored on the file system
      """
      with self.con:
         cur = self.con.cursor()
         cur.execute("UPDATE layers SET stored = 1 WHERE host='{host}' AND paramhash='{key}'".format(host=hostname, key=key))

   # .................................
   def _writeLayer(self, layerUrl, filename):
      """
      @summary: Writes a layer to the file system.
      @return: Boolean value indicating success
      """
      try:
         fDir = os.path.dirname(filename)
         if not os.path.exists(fDir):
            os.mkdir(fDir)
            
         content = urllib2.urlopen(layerUrl).readlines()
         if layerUrl.find('aaigrid') >= 0:
            f = open(filename, 'w')
            f.writelines(content[:5])
            f.write("NODATA_value   -9999\n")
            f.writelines(content[5:])
            f.close()
         else:
            f = open(filename, 'w')
            f.write(''.join(content))
            f.close()
            
            ds = gdal.Open(filename, gdalconst.GA_Update)
            band = ds.GetRasterBand(1)
            if band.GetNoDataValue() is None:
               valMin, _ = band.ComputeRasterMinMax(1)
               if valMin < -9000:
                  band.SetNoDataValue(valMin)
            ds = None
         
         return True
      except Exception, e:
         print str(e)
         return False
