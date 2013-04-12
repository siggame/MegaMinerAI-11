import random

from os import listdir
from os.path import isfile, join

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

class MapGenerator(object):
  def __init__(self, match):
    self.match = match
    self.load_tiles()

  def load_tiles(self):
    #TODO: Load tiles
    directory = join('config', 'mapTiles')
    files = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
    self.tiles = []
    for f in files:
      map = open(join(directory, f)).readlines()
      map = [[j  for j in i[:5]] for i in map]
      self.tiles.append(map)

  def lay_tiles(self):
    #super deep loop go!
    for i in range(4):
      for j in range(4):
        t = random.choice(self.tiles)
        if random.randint(0, 1):
          t = reversed(t)
        for k, row in enumerate(t):
          if random.randint(0, 1):
            row = reversed(row)
          for l, col in enumerate(row):
            x = i * 5 + k
            y = j * 5 + l
            tile = self.match.getTile(x, y)
            otherTile = self.match.getTile(self.match.mapWidth - x - 1, y)
            if col == ' ':
              tile.owner = otherTile.owner = 2
            else:
              tile.owner = otherTile.owner = 3

  def connect_map(self):
    while True:
      tiles = [i for i in self.match.objects.tiles if i.owner != 3]
      tile = random.choice(tiles)
      c = self._find_connected(tile)
      if len(c) == len(tiles):
        return
      walls = [i for i in self.match.objects.tiles if i.owner == 3]
      wall = random.choice(walls)
      otherWall = self.match.getTile(self.match.mapWidth - wall.x - 1, wall.y)
      wall.owner = otherWall.owner = 2

  def _find_connected(self, tile):
    open = [(tile.x, tile.y)]
    connected = set()
    while open:
      t = open.pop()
      if t in connected:
        continue
      connected.add(t)
      x, y = t
      for i, j in [ (x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if 0 <= i < self.match.mapWidth and 0 <= j < self.match.mapHeight:
          if self.match.getTile(i, j).owner == 3:
            continue
          if (i, j) not in connected:
            open.append((i, j))
    return connected

  def set_coves(self):
    tiles = [i for i in self.match.objects.tiles if i.x < 15 and i.owner == 3]
    tiles = random.sample(tiles, 10)
    for t in tiles:
      t.owner = 0
      x, y = t.x, t.y
      otherTile = self.match.getTile(self.match.mapWidth - x - 1, y)
      otherTile.owner = 1

def set_tiles(match):
  gen = MapGenerator(match)
  gen.lay_tiles()
  gen.set_coves()
  gen.connect_map()
