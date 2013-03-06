#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  def findCoves(self):
    coves = []
    for tile in self.tiles:
      if tile.owner!=2:
        coves.append(tile)
    return coves
  
  def findFish(self,myDude, confusion = False):
    dis = 400
    nearest = 1
    for fish in self.fishes:
      if self.distance(myDude,fish)<dis:
        if not confusion and fish.id!=myDude.id:
          nearest = fish
        else:
          nearest = fish
    return nearest
  
  def distance(self,source,target):
    return math.sqrt((source.x-target.x)**2+(source.y-target.y)**2)

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    for species in self.species:
      for cove in self.findCoves():
        species.spawn(cove.x,cove.y)
    for fish in self.fishes:
      fish.move(fish.x+1,fish.y)
      fish.pickUp(fish.x,fish.y+1,1)
      fish.pickUp(fish.x,fish.y-1,1)
      fish.drop(fish.x-1,fish.y,1)
      fish.attack(self.findFish(fish))
      fish.attack(self.findFish(fish,True))
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
