#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import math
import time

SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH = range(12)

class AI(BaseAI):
  """The class implementing gameplay logic."""

  myCoves = []
  myFish = []
  trash = []

  gridHistory = []

  @staticmethod
  def username():
    return "ruski"

  @staticmethod
  def password():
    return "password"

########## DO GRID STUFF ##########
  def saveGrid(self):
    tempGrid = [[' ' for _ in range(self.mapWidth) ] for _ in range(self.mapHeight) ]
    for tile in self.tiles:
      if tile.owner == 0 or tile.owner == 1:
        tempGrid[tile.y][tile.x] = 'C'
      if tile.owner == 3:
        tempGrid[tile.y][tile.x] = 'W'
      if tile.trashAmount > 0:
        tempGrid[tile.y][tile.x] = 'T'
      if tile.hasEgg == 1:
        tempGrid[tile.y][tile.x] = 'e'

    for fish in self.fishes:
      if fish.owner == self.playerID:
        tempGrid[fish.y][fish.x] = 'F'
      else:
        tempGrid[fish.y][fish.x] = 'f'

    self.gridHistory.append(tempGrid)
    return

  def replayHistory(self):
    for grid in self.gridHistory:
      self.printGrid(grid)
      time.sleep(.1)
    return

  def printGrid(self, grid):
    print "--" * self.mapWidth
    for columns in grid:
      for data in columns:
        print data,
      print
    return


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
  def generatePath(self, sourceX, sourceY, targetX, targetY):

    return

  def actFish(self):
    #for fish in self.myFish:

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

    print "Replaying Grid in ..."
    time.sleep(1)
    print "3 ..."
    time.sleep(1)
    print "2 ..."
    time.sleep(1)
    print "1 ..."
    time.sleep(1)
    self.replayHistory()

    return

  def run(self):
    print "Turn %i P1: %i P2 %i" % (self.turnNumber, self.players[0].currentReefHealth, self.players[1].currentReefHealth)
    self.saveGrid()

    self.spawnFish()
    self.actFish()

    self.saveGrid()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)

