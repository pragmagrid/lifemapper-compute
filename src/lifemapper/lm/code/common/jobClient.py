"""
@summary: Lifemapper computational job client library
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
import urllib
import urllib2

from config import JOB_TYPES, LOCAL_MACHINE_ID
from lmConstants import LM_JOB_SERVER
from lmXml import deserialize, fromstring

class RemoteKillException(Exception):
   """
   @summary: Signaled by Lifemapper job server to indicate that there is a 
                problem (server side, out of date client, other) and that the
                controlling code should stop until it is resolved
   """
   pass

class LmJobClient(object):
   """
   @summary: Communicates with the Lifemapper job server to retrieve, update,
                and post jobs
   """
   # .................................
   def __init__(self):
      self.id = LOCAL_MACHINE_ID
   
   # .................................
   def postJob(self, jobType, jobId, content, contentType, component):
      params = [
                ("request", "PostJob"),
                ("jobType", jobType),
                ("jobId", jobId),
                ("component", component)
               ]
      headers = {"Content-Type": contentType}
      body = content
      url = LM_JOB_SERVER
      ret = self.makeRequest(url, method="POST", parameters=params, body=body, 
                             headers=headers, objectify=False)
      return ret

   # .................................
   def requestJob(self, jobTypes=JOB_TYPES.keys(), parameters={}):
      params = [
                ("request", "GetJob"),
                ("jobTypes", ','.join([str(i) for i in jobTypes]))
               ]
      params.extend([(key, parameters[key]) for key in parameters.keys()])
      ret = self.makeRequest(LM_JOB_SERVER, parameters=params, objectify=True)
      return ret
   
   # .................................
   def requestPost(self, jobType, jobId, component):
      params = [
                ("request", "RequestPost"),
                ("jobType", jobType),
                ("jobId", jobId),
                ("component", component)
               ]
      resp = self.makeRequest(LM_JOB_SERVER, parameters=params)
      return bool(resp)
   
   # .................................
   def updateJob(self, jobType, jobId, status, progress):
      params = [
                ("request", "UpdateJob"),
                ("jobType", jobType),
                ("jobId", jobId),
                ("status", status),
                ("progress", progress)
               ]
      return self.makeRequest(LM_JOB_SERVER, method="POST", parameters=params)
   
   # .........................................
   def makeRequest(self, url, method="GET", parameters=[], body=None, 
                         headers={}, objectify=False):
      """
      @summary: Performs an HTTP request
      @param url: The url endpoint to make the request to
      @param method: (optional) The HTTP method to use for the request
      @param parameters: (optional) List of url parameters
      @param body: (optional) The payload of the request
      @param headers: (optional) Dictionary of HTTP headers
      @param objectify: (optional) Should the response be turned into an object
      @return: Response from the server
      """
      try:
         parameters = removeNonesFromTupleList(parameters)
         urlparams = urllib.urlencode(parameters)
         
         if body is None and len(parameters) > 0 and method.lower() == "post":
            body = urlparams
         else:
            url = "%s?%s" % (url, urlparams)
         req = urllib2.Request(url, data=body, headers=headers)
         ret = urllib2.urlopen(req)
         resp = ''.join(ret.readlines())
         if objectify:
            return self.objectify(resp)
         else:
            return resp
      except urllib2.HTTPError, e:
         print "Failed on url: %s" % url
         raise e
      
   # .........................................
   def objectify(self, xmlString):
      """
      @summary: Takes an XML string and processes it into a python object
      @param xmlString: The xml string to turn into an object
      @note: Uses LmAttList and LmAttObj
      @note: Object attributes are defined on the fly
      """
      return deserialize(fromstring(xmlString))   

# .............................................................................
def removeNonesFromTupleList(paramsList):
   """
   @summary: Removes parameter values that are None
   @param paramsList: List of parameters (name, value) [list of tuples]
   @return: List of parameters that are not None [list of tuples]
   """
   ret = []
   for param in paramsList:
      if param[1] is not None:
         ret.append(param)
   return ret

