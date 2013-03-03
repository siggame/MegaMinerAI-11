# -*- coding: iso-8859-1 -*-
from copy import copy
#from odict import OrderedDict

class Model(object):
  data = []
  functions = []
  properties = []
  name = ''
  plural = ''
  doc = ''
  type = ''
  parent = None
  def __init__(self, name, **kwargs):
    self.data = [ Variable('id', int, 'Unique Identifier') ]
    self.functions = []
    self.properties = []
    self.name = name
    self.plural = name + 's'
    self.type = 'Model'
    self.permanent = False

    if 'parent' in kwargs:
      self.parent = kwargs['parent']
      self.data = copy(self.parent.data)
      self.functions = copy(self.parent.functions)
      self.properties = copy(self.parent.properties)
    if 'data' in kwargs:
      data = kwargs['data']
      self.data.extend(data)
    if 'functions' in kwargs:
      functions = kwargs['functions']
      self.functions.extend(functions)
    if 'properties' in kwargs:
      properties = kwargs['properties']
      self.properties.extend(properties)
    if 'doc' in kwargs:
      self.doc = kwargs['doc']
    if 'type' in kwargs:
      self.type = kwargs['type']
    if 'plural' in kwargs:
      self.plural = kwargs['plural']
    if 'permanent' in kwargs:
      self.permanent = kwargs['permanent']

  def addData(self, data):
    self.data.extend(data)

  def addFunctions(self, functions):
    self.functions.extend(functions)

  def addProperties(self, properties):
    self.properties.extend(properties)

class Variable(object):
  name = ''
  type = None
  doc = ''

  def __init__(self, name, type, doc=''):
    self.name = name
    self.type = type
    self.doc = doc

class Animation(object):
  name = ''
  data = []

  def __init__(self, name, **kwargs):
    self.data = []
    self.name = name
    if 'data' in kwargs:
      data = kwargs['data']
      self.data.extend(data)


class Function(object):
  name = ''
  arguments = []
  result = None
  doc = ''

  def __init__(self, name, arguments=[], result=None, doc=''):
    self.name = name
    self.arguments = arguments
    self.result = result
    self.doc = doc
