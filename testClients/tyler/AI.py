#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math
import random

SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH = range(12)

class AI(BaseAI):
  """The class implementing gameplay logic."""

  @staticmethod
  def username():
    return "Tyler"

  @staticmethod
  def password():
    return "yay"
  
  def getObject(self,x,y):
    return [self.grid[x][y][-1]]
    
  def getTile(self,x,y):
    return self.tiles[x*self.mapHeight+y]
    
  def getTrash(self):
    pass
    
  def getAdjacent(self, x, y):
    adj = []
    if x + 1 < self.mapWidth:
      adj.append(getTile[x+1,y])
    if x - 1 > 0:
      adj.append(getTile[x-1,y])
    if y + 1 < self.mapHeight:
      adj.append(getTile[x,y+1])
    if y - 1 > 0:
      adj.append(getTile[x,y-1])
    return adj
  
  def validMove(self, x, y):
    if x >= self.mapWidth or x < 0:
      return 0
    if y >= self.mapHeight or y < 0:
      return 0
    tile = getTile(x, y)
    if tile.owner != self.playerID or tile.hasEgg or tile.trashAmount > 0:
      return 0
    if isinstance(getObject(x,y), Fish):
      return 0
    return 1
    
  def manhatdist(self, x, y, destx, desty):
    return (abs(destx - x) + abs(desty - y))
    
  def pathfind(self, x, y, destx, desty):
    closed = set()
    path = []
    current = getTile(x, y)
    path.append(current)
    target = getTile(destx, desty)
    #closed.add(current)
    while target not in closed:
      open = []
      for tile in getAdjacent(current.x, current.y):
        if validMove(tile.x, tile.y) and tile not in closed:
          open.append(tile)
      min = manhatdist(open[0].x, open[0].y, destx, desty)
      mindex = 0
      for node in open:
        dist = manhatdist(node.x, node.y, destx, desty)
        if dist <= min:
          min = dist
          mindex = open.index(node)
      current = open[mindex]
      path.append(current)
      closed.add(current)
    return path
    
    
  
  
  ##This function is called once, before your first turn
  def init(self):
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    enemies = []
    friends = []
    for guy in self.fishes:
      if guy.owner == self.playerID:
        friends.append(guy)
      else:
        enemies.append(guy)
    
    
    
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
