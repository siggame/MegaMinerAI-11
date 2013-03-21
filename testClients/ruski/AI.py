#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random

class AI(BaseAI):
  """The class implementing gameplay logic."""

  myCoves = []
  myFish = []


  @staticmethod
  def username():
    return "ruski"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    print "Init"
    self.getMyCoves()
    return

  ##This function is called once, after your last turn
  def end(self):
    self.printMyFish()
    print "The End"
    return

  def getMyFish(self):
    self.myFish = []
    for fish in self.fishes:
      if fish.owner is self.playerID:
        self.myFish.append(fish)
    return
  '''
  def getFish(self, x, y):
    for fish in self.fish:

  def getTile(self, x, y):
    for tile in self.tiles:
      if tile.x is x and tile.y is y:
        return tile

    return None
    '''
  def attemptSpawn(self, x, y, species):
    me = self.players[self.playerID]
    if x < 0 or x > self.mapWidth:
      return False
    if y < 0 or y > self.mapHeight:
      return False

    if self.getCurrentSeason() is not species.season:
      return False

    print "Spawn Food: %i    Species Cost: %i" % (me.spawnFood, species.cost)
    if me.spawnFood < species.cost:
      return False

    species.spawn(x, y)
    return True

  def getMyCoves(self):
    print "Find coves."
    self.myCoves = []
    for tile in self.tiles:
      if tile.owner is self.getPlayerID():
        self.myCoves.append(tile)
    return

  def printMyCoves(self):
    for cove in self.myCoves:
      print "(%i, %i)" % (cove.x, cove.y)
    return

  def printMyFish(self):
    for fish in self.myFish:
      print fish
    return

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print "Starting Turn #%i" % self.turnNumber
    self.getMyFish()
    self.printMyFish()

    for spec in self.species:
      for cove in self.myCoves:
        self.attemptSpawn(cove.x, cove.y, spec)

    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
