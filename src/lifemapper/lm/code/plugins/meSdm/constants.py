"""
@summary: Module containing MaxEnt constants

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

PARAMETERS = {
   'addallsamplestobackground': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'addsamplestobackground': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'adjustsampleradius': {
      'default' : '0',
      'process' : lambda x: str(int(x))
   },
   'appendtoresultsfile': {
      'default' : 'false',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'autofeature': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'beta_categorical': {
      'default' : '-1.0',
      'process' : lambda x: str(float(x))
   },
   'beta_hinge': {
      'default' : '-1.0',
      'process' : lambda x: str(float(x))
   },
   'beta_lqp': {
      'default' : '-1.0',
      'process' : lambda x: str(float(x))
   },
   'beta_threshold': {
      'default' : '-1.0',
      'process' : lambda x: str(float(x))
   },
   'betamultiplier': {
      'default' : '1.0',
      'process' : lambda x: str(float(x))
   },
   'convergencethreshold': {
      'default' : '0.00001',
      'process' : lambda x: str(float(x))
   },
   'defaultprevalence': {
      'default' : '0.5',
      'process' : lambda x: str(float(x))
   },
   'doclamp': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'extrapolate': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'fadebyclamping': {
      'default' : 'false',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'hinge': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'hingethreshold': {
      'default' : '15',
      'process' : lambda x: str(int(x))
   },
   'jackknife': {
      'default' : 'false',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'linear': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'logscale': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'lq2lqptthreshold': {
      'default' : '80',
      'process' : lambda x: str(int(x))
   },
   'l2lqthreshold': {
      'default' : '10',
      'process' : lambda x: str(int(x))
   },
   'maximumbackground': {
      'default' : '10000',
      'process' : lambda x: str(int(x))
   },
   'maximumiterations': {
      'default' : '',
      'process' : lambda x: str(int(x))
   },
   'outputformat': {
      'default' : 'logistic',
      'options' : {
                   '0' : 'raw',
                   '1' : 'logistic',
                   '2' : 'cumulative'
                  },
      'process' : lambda x: x
   },
   'outputgrids': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'perspeciesresults': {
      'default' : 'false',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'pictures': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'plots': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'product': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'quadratic': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'randomseed': {
      'default' : 'false',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'randomtestpoints': {
      'default' : '0',
      'process' : lambda x: str(int(x))
   },
   'removeduplicates': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'replicates': {
      'default' : '1',
      'process' : lambda x: str(int(x))
   },
   'replicatetype': {
      'default' : 'crossvalidate',
      'options' : {
                   '0' : 'crossvalidate',
                   '1' : 'bootstrap',
                   '2' : 'subsample'
                  },
      'process' : lambda x: x
   },
   'responsecurves': {
      'default' : 'true',
      'process': lambda x: str(bool(int(x))).lower()
   },
   'responsecurvesexponent': {
      'default' : 'false',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'threshold': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'writebackgroundpredictions': {
      'default' : 'false',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'writeclampgrid': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'writemess': {
      'default' : 'true',
      'process' : lambda x: str(bool(int(x))).lower()
   },
   'writeplotdata': {
      'default' : 'false',
      'process' : lambda x: str(bool(int(x))).lower()
   },
}
