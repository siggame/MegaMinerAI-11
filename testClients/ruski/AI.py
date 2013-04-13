#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import math

SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH = range(12)

class AI(BaseAI):
  """The class implementing gameplay logic."""

  myCoves = []
  myFish = []
  trash = []

  @staticmethod
  def username():
    return "ruski"

  @staticmethod
  def password():
    return "password"

########## GET LOCAL LISTS ##########
  def getMyCoves(self):
    print "Get My Coves"
    for tile in self.tiles:
      if tile.trashAmount > 0:
        self.trash.append(tile)
    return
  def getMyFish(self):
    print "Get My Fish"
    for fish in self.fishes:
      if fish.owner == self.playerID:
        self.myFish.append(fish)
    return

########## FISH FUNCTIONS ##########
  def spawnFish(self):
    print "Spawn Fish"
    for cove in self.myCoves:
      if cove.hasEgg == 0 and self.getFish(cove.x, cove.y) == None:
        for species in self.speciesList:
          if species.season == self.currentSeason and self.players[self.playerID].spawnFood >= species.cost:
            species.spawn(cove)
            break
    return

  def actFish(self):
    for fish in self.myFish:

    return

########## DISTANCE FUNCTIONS ##########
  def euclDist(self, x1, y1, x2, y2):
    return math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
  def taxiDist(self, x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

########## INIT AND END ##########
  def init(self):
    print "Init"
    self.getMyCoves()
    return

  def end(self):
    print "End"
    return

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print "Starting Turn %i" % self.turnNumber
    self.spawnFish()

    self.actFish()

    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)

