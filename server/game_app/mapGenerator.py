import random

class MapGenerator(object):
  def __init__(self, match):
    self.match = match
    self.load_tiles()
  
  def load_tiles(self):
    #TODO: Load tiles
    self.tiles = [
        [ [ ' ', ' ', ' ', ' ', ' '],
          [ ' ', ' ', ' ', ' ', ' '],
          [ ' ', ' ', '#', ' ', ' '],
          [ ' ', '#', '#', ' ', ' '],
          [ ' ', ' ', ' ', ' ', ' ']]]

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
