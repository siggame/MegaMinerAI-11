#TODO: Account for invisible fish

class Tile(object):
  def __init__(self, x, y):
    self.item = None
    self.source = None
    self.tile = None
    self.distance = 10000
    self.x = x
    self.y = y

class Pathfinder(object):
  def __init__(self, ai):
    self.ai = ai
    self.tiles = [
        [Tile(i, j) for j in xrange(ai.mapHeight)]
        for i in xrange(ai.mapWidth)]
    for i in self.ai.tiles:
      tile = self.tiles[i.x][i.y]
      tile.tile = i


  def populate(self):
    for i in self.tiles:
      for j in i:
        j.distance = 10000
        j.source = None
        j.item = None

    for i in self.ai.fishes:
      tile = self.tiles[i.x][i.y]
      if not tile.item:
        tile.item = i

  def path(self, fish, max=200):
    start = self.tiles[fish.x][fish.y]
    start.distance = 0
    open = [start]
    closed = []
    while open:
      i = open.pop(0)
      closed.append(i)
      if i.distance >= max:
        continue
      adjacent = self.adjacentTiles(i)
      for j in adjacent:
        if j.distance > i.distance + 1:
          j.distance = i.distance+1
          j.source = i
          if not self.blocked(fish, j):
            open.append(j)

    return closed

  def blocked(self, fish, tile):
    if tile.tile.owner == fish.owner^1:
        return True
    if tile.tile.trashAmount:
      return True
    if not tile.item:
      return False
    return True


  def adjacentTiles(self, tile):
    x = tile.x
    y = tile.y
    locations = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    tiles = []
    for i, j in locations:
      if i < 0 or i >= self.ai.mapWidth or j < 0 or j >= self.ai.mapHeight:
        continue
      tiles.append(self.tiles[i][j])

    return tiles

