# -*- python -*-

from library import library

class BaseAI:
  """@brief A basic AI interface.

  This class implements most the code an AI would need to interface with the lower-level game code.
  AIs should extend this class to get a lot of builer-plate code out of the way
  The provided AI class does just that.
  """
  #\cond
  initialized = False
  iteration = 0
  runGenerator = None
  connection = None
  #\endcond
% for model in models:
%   if model.type == 'Model':
  ${lowercase(model.plural)} = []
%   endif
% endfor
  #\cond
  def startTurn(self):
% for model in models:
%   if model.type == 'Model':
    from GameObject import ${model.name}
%   endif
% endfor

% for model in models:
%   if model.type == 'Model':
    BaseAI.${lowercase(model.plural)} = [${model.name}(library.get${model.name}(self.connection, i)) for i in xrange(library.get${model.name}Count(self.connection))]
%   endif
% endfor

    if not self.initialized:
      self.initialized = True
      self.init()
    BaseAI.iteration += 1;
    if self.runGenerator:
      try:
        return self.runGenerator.next()
      except StopIteration:
        self.runGenerator = None
    r = self.run()
    if hasattr(r, '__iter__'):
      self.runGenerator = r
      return r.next()
    return r
  #\endcond
% for datum in globals:
  #\cond
  def get${capitalize(datum.name)}(self):
    return library.get${capitalize(datum.name)}(self.connection)
  #\endcond
  ##${datum.doc}
  ${datum.name} = property(get${capitalize(datum.name)})
% endfor
  def __init__(self, connection):
    self.connection = connection
