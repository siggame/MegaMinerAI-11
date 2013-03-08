import objects

class ObjectHolder(dict):
  def __init__(self, *args, **kwargs):
    dict.__init__(self, *args, **kwargs)
% for model in models:
    self.${lowercase(model.plural)} = []
% endfor

  def __setitem__(self, key, value):
    if key in self:
      self.__delitem__(key)
    dict.__setitem__(self, key, value)
% for model in models:
    if isinstance(value, objects.${model.name}):
      self.${lowercase(model.plural)}.append(value)
% endfor

  def __delitem__(self, key):
    value = self[key]
    dict.__delitem__(self, key)
% for model in models:
    if value in self.${lowercase(model.plural)}:
      self.${lowercase(model.plural)}.remove(value)
% endfor

  def clear(self):
    for i in self.keys():
      del self[i]
