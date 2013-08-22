"""
@summary: Module containing Lifemapper XML utilities
@note: Mainly wraps elementTree functionality to fit Lifemapper needs
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
from types import BuiltinFunctionType, BuiltinMethodType, IntType, FloatType, \
                  FunctionType, LambdaType, ListType, MethodType, NoneType, \
                  StringType, TypeType, DictType
import xml.etree.ElementTree as ET

from lmConstants import ENCODING, LM_NAMESPACE
from lmObj import LmAttList, LmAttObj

# Functions / Classes directly mapped to the Element Tree versions
# ..............................................................................
Comment = ET.Comment
dump = ET.dump
ElementTree = ET.ElementTree
fromstring = ET.fromstring
iselement = ET.iselement
iterparse = ET.iterparse
parse = ET.parse
PI = ET.PI
ProcessingInstruction = ET.ProcessingInstruction
QName = ET.QName
TreeBuilder = ET.TreeBuilder
VERSION = ET.VERSION
XML = ET.XML
XMLParser = ET.XMLParser
XMLTreeBuilder = ET.XMLTreeBuilder
# ..............................................................................

# Functions modified to serve Lifemapper purposes
# ..............................................................................
# Redefinition of _serialize_xml to handle CDATA
ET._original_serialize_xml = ET._serialize_xml
def _serialize_xml(write, elem, encoding, qnames, namespaces):
   if elem.tag == '![CDATA[':
      write("\n<%s%s]]>\n" % (elem.tag, elem.text))
      return
   return ET._original_serialize_xml(write, elem, encoding, qnames, namespaces)
ET._serialize_xml = ET._serialize['xml'] = _serialize_xml

# ..............................................................................
def Element(name, value=None, namespace=LM_NAMESPACE, attribs=[]):
   """
   @summary: Wrapper for the ElementTree Element function
   @param name: The name of the element created
   @param value: (optional) The value of the .text property for the element
   @param attribs: (optional) A list of name / value attribute pairs to attach
                   to the element.
   @return: The element created
   """
   if namespace is not None:
      elmname = "{%s}%s" % (namespace, name)
   else:
      elmname = name
      
   newElement = ET.Element(unicode(elmname, ENCODING))
   if value is not None:
      value = str(value)
      newElement.text = unicode(str(value), ENCODING)
   
   for att in attribs:
      try:
         newElement.attrib[unicode(att[0], ENCODING)] = \
                                                   unicode(att[1], ENCODING)
      except Exception:
         pass
   return newElement

# ..............................................................................
def SubElement(parent, name, value=None, namespace=LM_NAMESPACE, attribs=[]):
   """
   @summary: Wrapper for the ElementTree SubElement function
   @param parent: The element to use as the parent for this element
   @param name: The name of the element created
   @param value: (optional) The value of the .text property for the element
   @param attribs: (optional) A list of name / value attribute pairs to attach
                   to the element.
   @return: The element created
   """
   if namespace is not None:
      elmname = "{%s}%s" % (namespace, name)
   else:
      elmname = name
      
   newElement = ET.SubElement(parent, unicode(elmname, ENCODING))
   if value is not None:
      value = str(value)
      newElement.text = unicode(str(value), ENCODING)
   
   for att in attribs:
      try:
         newElement.attrib[unicode(att[0], ENCODING)] = \
                                                   unicode(att[1], ENCODING)
      except Exception:
         pass
   return newElement

# ..............................................................................
def tostring(elem, encoding=ENCODING):
   """
   @summary: Converts an ElementTree to a formatted string
   @param elem: The element tree element to convert to a string
   @param encoding: (optional) The encoding to use [ex. UTF-8]
   """
   _prettyFormat(elem)
   return ET.tostring(elem, encoding=encoding)

# ..............................................................................
def _prettyFormat(elem, level=0):
   """
   @summary: Formats ElementTree element so that it prints pretty (recursive)
   @param elem: ElementTree element to be pretty formatted
   @param level: How many levels deep to indent for
   """
   tab = "   "

   i = "\n" + level*tab
   if len(elem):
      if not elem.text or not elem.text.strip():
         elem.text = i + tab
      for e in elem:
         _prettyFormat(e, level+1)
         if not e.tail or not e.tail.strip():
            e.tail = i + tab
      if not e.tail or not e.tail.strip():
         e.tail = i
   else:
      if level and (not elem.tail or not elem.tail.strip()):
         elem.tail = i
 
# ..............................................................................
def setNamespacePrefix(namespace, prefix):
   """
   @summary: Sets the prefix for a namespace.  Without this function, the 
             namespace prefix will be assigned by ElementTree.
   @param namespace: The namespace url
   @param prefix: The desired namespace prefix
   """
   ET._namespace_map[namespace] = prefix

# .............................................................................
def deserialize(element, removeNS=True):
   """
   @summary: Deserializes an ElementTree (Sub)Element into an object
   @param element: The element to deserialize
   @param removeNS: (optional) If true, removes the namespaces from the tags
   @return: A new object
   """
   # If removeNS is set to true, look for namespaces in the tag and remove them
   #    They are enclosed in curly braces {namespace}tag
   if removeNS:
      processTag = lambda s: s.split("}")[1] if s.find("}") >= 0 else s
   else:
      processTag = lambda s: s
   
   # If the element has no children, just get the text   
   if len(list(element)) == 0 and len(element.attrib.keys()) == 0:
      try:
         val = element.text.strip()
         if len(val) > 0:
            return val
         else:
            return None
      except:
         return None
   else:
      attribs = dict([(processTag(key), element.attrib[key]) for key in element.attrib.keys()])
      obj = LmAttObj(attribs=attribs, name=processTag(element.tag))

      try:
         val = element.text.strip()
         if len(val) > 0:
            obj.value = val
      except:
         pass
      
      # Get a list of all of the element's children's tags
      # If they are all the same type and match the parent, make one list
      tags = [child.tag for child in list(element)]
      reducedTags = list(set(tags))
      
      if len(reducedTags) == 1 and reducedTags[0] == element.tag[:-1]: # or len(tags) > 1):
         obj = LmAttList([], attribs=attribs, name=processTag(element.tag))
         for child in list(element):
            obj.append(deserialize(child, removeNS))
      else:
         # Process the children
         for child in list(element):
            if hasattr(obj, processTag(child.tag)):
               tmp = obj.__getattribute__(processTag(child.tag))
               if isinstance(tmp, ListType):
                  tmp.append(deserialize(child, removeNS))
               else:
                  tmp = LmAttList([tmp, deserialize(child, removeNS)], name=processTag(child.tag)+'s')
               setattr(obj, processTag(child.tag), tmp)
            else:
               setattr(obj, processTag(child.tag), deserialize(child, removeNS))
      return obj

# .............................................................................
def serialize(obj, parent=None):
   """
   @summary: This function serializes an object into xml
   @note: Recursive
   @param parent: (optional) A parent element to attach this one to
   @return: An ElementTree element representing the object
   @rtype: ElementTree (Sub)Element
   """
   value = None
   attribs = []
   if hasattr(obj, 'value'):
      value = obj.value
   elif isinstance(obj, StringType):
      value = obj
      
   fltr = lambda x: not x.startswith('_') and not x == "attribs" and not x == "value"
   objAttribs = [attrib for attrib in dir(obj) if fltr(attrib)]

   if hasattr(obj, 'attribs'):
      attribs = [(key, obj.attribs[key]) for key in obj.attribs.keys()]
   try:
      atts = obj.getAttributes()
      for key in atts.keys():
         if isinstance(atts[key], (IntType, StringType, FloatType)):
            attribs.append((key, str(atts[key])))
         elif isinstance(atts[key], (NoneType)):
            pass
         else:
            objAttribs.append(key)
   except Exception:
      pass

   if isinstance(obj, TypeType):
      elName = obj.__name__
   elif isinstance(obj, LmAttObj):
      elName = obj.__name__
   else:
      elName = obj.__class__.__name__

   if parent is None:
      el = Element(elName, value=value, namespace=None, attribs=attribs)
   else:
      el = SubElement(parent, elName, value=value, namespace=None, attribs=attribs)

   for attrib in objAttribs:
      subObj = getattr(obj, attrib)
      if isinstance(subObj, ListType):
         for i in subObj:
            serialize(i, el)
      elif isinstance(subObj, (MethodType, FunctionType, LambdaType, BuiltinMethodType, BuiltinFunctionType)):
         pass
      elif isinstance(subObj, (StringType, IntType, FloatType)):
         SubElement(el, attrib, subObj, namespace=None)
      elif isinstance(subObj, DictType):
         sEl = SubElement(el, attrib, namespace=None)
         for key in subObj.keys():
            if isinstance(subObj[key], (StringType, IntType, FloatType)):
               SubElement(sEl, key, subObj[key], namespace=None)
            elif isinstance(subObj[key], NoneType):
               pass
            else:
               serialize(subObj[key], sEl)
      else:
         serialize(getattr(obj, attrib), el)
   if isinstance(obj, ListType):
      for i in obj:
         serialize(i, el)
   return el
