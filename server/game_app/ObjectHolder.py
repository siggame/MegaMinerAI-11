import objects

class ObjectHolder(dict):
  def __init__(self, *args, **kwargs):
    dict.__init__(self, *args, **kwargs)
    self.mappables = []
    self.tiles = []
    self.species = []
    self.fishes = []
    self.players = []

  def __setitem__(self, key, value):
    if key in self:
      self.__delitem__(key)
    dict.__setitem__(self, key, value)
    if isinstance(value, objects.Mappable):
      self.mappables.append(value)
    if isinstance(value, objects.Tile):
      self.tiles.append(value)
    if isinstance(value, objects.Species):
      self.species.append(value)
    if isinstance(value, objects.Fish):
      self.fishes.append(value)
    if isinstance(value, objects.Player):
      self.players.append(value)

  def __delitem__(self, key):
    value = self[key]
    dict.__delitem__(self, key)
    if value in self.mappables:
      self.mappables.remove(value)
    if value in self.tiles:
      self.tiles.remove(value)
    if value in self.species:
      self.species.remove(value)
    if value in self.fishes:
      self.fishes.remove(value)
    if value in self.players:
      self.players.remove(value)

  def clear(self):
    for i in self.keys():
      del self[i]
