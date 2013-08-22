"""
@summary: Module containing the constants set by Lifemapper
@author: CJ Grady
@version: 2.0
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
# =                             Client Constants                             =
# ============================================================================
CLIENT_VERSION = "1.0"
LM_JOB_SERVER = "http://lifemapper.org/jobs"

# ----------------------------------------------------------------------------

ENCODING = 'utf8'
LM_NAMESPACE = "http://lifemapper.org"
LM_NS_PREFIX = "lm"


class JobStatus:
   GENERAL = 0
   INITIALIZE = 1
   PULL_REQUESTED = 90
   PULL_COMPLETE = 100
   COMPUTE_INITIALIZED = 110
   RUNNING = 120
   COMPUTED = 130
   PUSH_REQUESTED = 140
   PUSHED = 150
   PUSH_COMPLETE = 200
   COMPLETE = 300
   
   GENERAL_ERROR = 1000
   UNKNOWN_ERROR = 1001
   PUSH_FAILED = 1100

   # ==========================================================================
   # =                              Common Errors                             =
   # ==========================================================================
   # Database
   # ------------
   DB_CREATE_ERROR = 1201
   DB_DELETE_ERROR = 1202
   DB_INSERT_ERROR = 1203
   DB_READ_ERROR = 1204
   DB_UPDATE_ERROR = 1205
   
   # I/O
   # -----------
   IO_READ_ERROR = 1301
   IO_WRITE_ERROR = 1302
   IO_WAIT_ERROR = 1303

   # ==========================================================================   
   # =                               HTTP Errors                              =
   # ==========================================================================
   # Last 3 digits are the http error code, only 400 and 500 levels listed
   HTTP_GENERAL_ERROR = 4000
      
   # Client error
   # ............................................
   HTTP_CLIENT_BAD_REQUEST = 4400
   HTTP_CLIENT_UNAUTHORIZED = 4401
   HTTP_CLIENT_FORBIDDEN = 4403
   HTTP_CLIENT_NOT_FOUND = 4404
   HTTP_CLIENT_METHOD_NOT_ALLOWED = 4405
   HTTP_CLIENT_NOT_ACCEPTABLE = 4406
   HTTP_CLIENT_PROXY_AUTHENTICATION_REQUIRED = 4407
   HTTP_CLIENT_REQUEST_TIMEOUT = 4408
   HTTP_CLIENT_CONFLICT = 4409
   HTTP_CLIENT_GONE = 4410
   HTTP_CLIENT_LENGTH_REQUIRED = 4411
   HTTP_CLIENT_PRECONDITION_FAILED = 4412
   HTTP_CLIENT_REQUEST_ENTITY_TOO_LARGE = 4413
   HTTP_CLIENT_REQUEST_URI_TOO_LONG = 4414
   HTTP_CLIENT_UNSUPPORTED_MEDIA_TYPE = 4415
   HTTP_CLIENT_REQUEST_RANGE_NOT_SATISFIABLE = 4416
   HTTP_CLIENT_EXPECTATION_FAILED = 4417

   # Server error
   # ............................................
   HTTP_SERVER_INTERNAL_SERVER_ERROR = 4500
   HTTP_SERVER_NOT_IMPLEMENTED = 4501
   HTTP_SERVER_BAD_GATEWAY = 4502
   HTTP_SERVER_SERVICE_UNAVAILABLE = 4503
   HTTP_SERVER_GATEWAY_TIMEOUT = 4504
   HTTP_SERVER_HTTP_VERSION_NOT_SUPPORTED = 4505
   
