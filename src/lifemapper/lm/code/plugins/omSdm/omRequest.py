"""
@summary: Module used to create openModeller requests
@author: CJ Grady
@contact: cjgrady@ku.edu
@version: 2.0
@status: beta
@note: For openModeller version 1.3.0
@note: Possibly backwards compatible

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
from types import ListType

from common.layerManager import LayerManager

DEFAULT_FILE_TYPE = "GreyTiff"
DEFAULT_LOG_LEVEL = "debug" # debug, warn, info, error

FILE_TYPES = ["FloatingHFA", "FloatingTiff", "GreyTiff"]

# .............................................................................
class OmRequest(object):
   """
   @summary: Base class for openModeller requests
   """
   # .................................
   def __init__(self):
      if self.__class__ == OmRequest:
         raise Exception, "OmRequest base class should not be used directly."
      
   # .................................
   def generate(self):
      raise Exception, "generate method must be overridden by a subclass"

# .............................................................................
class OmModelRequest(OmRequest):
   """
   @summary: Class for generating openModeller model requests
   """
   
   # .................................
   def __init__(self, model, dataDir):
      """
      @summary: openModeller model request constructor
      @param model: The model object to use
      @param dataDir: The directory to store layers in
      @todo: Take options and statistic options as inputs
      """
      self.options = [
                  #("OccurrencesFilter", "SpatiallyUnique"), # Ignore duplicate points (same coordinates)
                  #("OccurrencesFilter", "EnvironmentallyUnique") # Ignore duplicate points (same environment values)
                ]
      self.statOpts = {
                    "ConfusionMatrix" : {
                                           "Threshold" : "0.5"
                                        },
                    "RocCurve" :        {
                                           "Resolution" : "15",
                                           "BackgroundPoints" : "10000",
                                           "MaxOmission" : "1.0"
                                        }
                 }

      self.lyrs = []
      
      lyrMgr = LayerManager(dataDir)
      for lyrUrl in model.layers:
         self.lyrs.append(lyrMgr.getLayerFilename(lyrUrl))
      lyrMgr.close()

      if len(self.lyrs) > 0:
         self.mask = self.lyrs[0]
      else:
         self.mask = ""
      self.model = model
      
      if model.algorithm.parameter is not None:
         if isinstance(model.algorithm.parameter, ListType):
            self.algoParams = model.algorithm.parameter
         else:
            self.algoParams = [model.algorithm.parameter]
      else:
         self.algoParams = []
      
   # .................................
   def generate(self):
      """
      @summary: Generates a model request string
      """
      lyrs = '\n'.join(['         <Map Id="{lyr}" IsCategorical="0" />'.format(lyr=lyr) for lyr in self.lyrs])
      pts = '\n'.join(['         <Point Id="{id}" X="{x}" Y="{y}" />'.format(id=pt.id, x=pt.x, y=pt.y) for pt in self.model.points.point])
      algPrms = '\n'.join(['         <Parameter Id="{id}" Value="{val}" />'.format(id=param.id, val=param.value) for param in self.algoParams])
      opts = '\n'.join(['      <{name}>{value}</{name}>'.format(name=name, value=value) for name, value in self.options])
      ret = """<ModelParameters>
   <Sampler>
      <Environment NumLayers="{numLayers}">
{lyrSection}
         <Mask Id="{mask}" />
      </Environment>
      <Presence Label="{displayName}">
         <CoordinateSystem>
            {wkt}
         </CoordinateSystem>
{pts}
      </Presence>
   </Sampler>
   <Algorithm Id="{algoCode}">
      <Parameters>
{algPrms}
      </Parameters>
   </Algorithm>
   <Options>
{opts}
   </Options>
   <Statistics>
      <ConfusionMatrix Threshold="{confMatThreshold}" />
      <RocCurve Resolution="{rocResolution}" BackgroundPoints="{bkPnts}" MaxOmission="{maxOmission}" />
   </Statistics>
</ModelParameters>""".format(
            numLayers=len(self.lyrs), 
            lyrSection=lyrs,
            mask=self.mask,
            displayName=self.model.points.displayName,
            wkt=self.model.points.wkt,
            pts=pts,
            algoCode=self.model.algorithm.code,
            algPrms=algPrms,
            opts=opts,
            confMatThreshold=self.statOpts['ConfusionMatrix']['Threshold'],
            rocResolution=self.statOpts['RocCurve']['Resolution'],
            bkPnts=self.statOpts['RocCurve']['BackgroundPoints'],
            maxOmission=self.statOpts['RocCurve']['MaxOmission'])
      return ret

# .............................................................................
class OmProjectionRequest(OmRequest):
   """
   @summary: Class for generating openModeller projection requests
   """
   
   # .................................
   def __init__(self, projection, dataDir):
      """
      @summary: Constructor for OmProjectionRequest class
      @param projection: The projection object to use
      @param dataDir: The directory to store layers in
      """
      lyrs = []
      
      lyrMgr = LayerManager(dataDir)
      for lyrUrl in projection.layers:
         lyrs.append(lyrMgr.getLayerFilename(lyrUrl))
      lyrMgr.close()

      if len(lyrs) > 0:
         mask = lyrs[0]
      else:
         mask = ""
      
      self.algorithmSection = projection.algorithm
      self.layers = lyrs
      self.mask = mask
      self.fileType = DEFAULT_FILE_TYPE
      self.templateLayer = mask
      
   # .................................
   def generate(self):
      """
      @summary: Generates a model request string
      """
      lyrs = '\n'.join(['         <Map Id="{lyr}" IsCategorical="0" />'.format(lyr=lyr) for lyr in self.layers])
      ret = """<ProjectionParameters>
{algorithmSection}
   <Environment NumLayers="{numLayers}">
{lyrSection}
      <Mask Id="{mask}" />
   </Environment>
   <OutputParameters FileType="{fileType}">
      <TemplateLayer Id="{templateLayer}" />
   </OutputParameters>
</ProjectionParameters>""".format(algorithmSection=self.algorithmSection,
                                  numLayers=len(self.layers), 
                                  lyrSection=lyrs,
                                  mask=self.mask,
                                  fileType=self.fileType,
                                  templateLayer=self.templateLayer)
      return ret

