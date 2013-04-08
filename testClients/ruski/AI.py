#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import time
import math
import os

SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH = range(12)

class AI(BaseAI):
  """The class implementing gameplay logic."""

  ########## LOCAL LISTS ##########
  myCoves = []
  enemyCoves = []
  myFish = []
  enemyFish = []
  trash = []
  charGrid = [[]]
  gridHistory = []

  ########## USERNAME AND PASSWORD ##########
  @staticmethod
  def username():
    return "ruski"
  @staticmethod
  def password():
    return "password"

  ########## START AND END ##########
  def init(self):
    print "Init"
    self.getMyCoves()
    self.getEnemyCoves()
    return
  def end(self):
    print "The End"
    #self.replayGrid()
    return

  ########## LOCAL GETTERS ##########
  def getSpecies(self, index):
    for spec in self.species:
      if spec.index is index:
        return spec
    return "Invalid Index"
  def getMyCoves(self):
    self.myCoves = []
    for tile in self.tiles:
      if tile.owner is self.playerID:
        self.myCoves.append(tile)
    return
  def getEnemyCoves(self):
    self.enemyCoves = []
    for tile in self.tiles:
      if tile.owner is self.playerID^1:
        self.enemyCoves.append(tile)
    return
  def getMyFish(self):
    self.myFish = []
    for fish in self.fishes:
      if fish.owner is self.playerID:
        self.myFish.append(fish)
  def getEnemyFish(self):
    for fish in self.fishes:
      if fish.owner is self.playerID^1:
        self.enemyFish.append(fish)
  def getTrash(self):
    self.trash = []
    for tile in self.tiles:
      if tile.trashAmount > 0:
        self.trash.append(tile)


  ########## CHARACTER GRID ##########
  def getCharGrid(self):
    self.charGrid = [[' ' for _ in range(self.getMapHeight())] for _ in range(self.getMapWidth()) ]
    for tile in self.tiles:
      if tile.owner != 2:
        self.charGrid[tile.x][tile.y] = 'C'
      if tile.hasEgg:
        self.charGrid[tile.x][tile.y] = 'E'
      if tile.trashAmount > 0:
        self.charGrid[tile.x][tile.y] = 'T'
    for fish in self.fishes:
      if fish.isVisible is 1:
        self.charGrid[fish.x][fish.y] = 'F'
      else:
        self.charGrid[fish.x][fish.y] = 'f'
    return
  def replayGrid(self):
    wantReplay = True
    while wantReplay:
      for grid in self.gridHistory:
        time.sleep(0.25)
        self.printCharGrid(grid)
        print "--" * (self.mapWidth +2)
      print "Do you want to replay?: "
      usrinput = raw_input()
      if "y" in usrinput:
        wantReplay = True
      else:
        wantReplay = False
    return
  def printCharGrid(self, grid):
    for y in range(self.getMapHeight()):
      for x in range(self.getMapWidth()):
        if x == self.mapWidth/2 - self.boundLength:
          print "|",
        elif x == self.mapWidth/2 + self.boundLength:
          print "|",
        print grid[x][y],
      print
    return

  ########## DISTANCE FUNCTIONS ##########
  def euclDist(self, x1, y1, x2, y2):
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
  def taxiDist(self, x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)

  ########## FISH MOVE FUNCTIONS ##########
  def moveTo(self, fish, tx, ty):
    for _ in fish.maxMovement:
      #Move Right
      if fish.x < tx:
        if not self.attemptMove(fish, fish.x+1, fish.y):
          if not self.attemptMove(fish, fish.x, fish.y+1):
            self.attemptMove(fish, fish.x, fish.y-1)
      #Move Left
      elif fish.x > tx:
        if not self.attemptMove(fish, fish.x-1, fish.y):
          if not self.attemptMove(fish, fish.x, fish.y+1):
            self.attemptMove(fish, fish.x, fish.y-1)
      #Move Up
      elif fish.y < ty:
        self.attemptMove(fish, fish.x, fish.y+1)

      #Move Down
      elif fish.y > ty:
        self.attemptMove(fish, fish.x, fish.y-1)

    return

  def attemptMove(self, fish, tx, ty):
    if 0 <= tx < self.mapWidth:
      return False
    if 0 <= ty < self.mapHeight:
      return False

    T = self.tiles[ty*self.mapWidth + tx]
    print "Expected (%i, %i) Retrieved (%i, %i)" % (tx, ty, T.x, T.y)
    if T.trashAmount > 0:
      return False
    if T.owner is self.playerID or 2:
      return False
    if T.hasEgg:
      return False
    if self.taxiDist(fish.x, fish.y, tx, ty) is not 1:
      return False

    for otherfish in self.fishes:
      if otherfish.x == tx and otherfish.y == ty and otherfish.id != fish.id:
        return False
    return fish.move(tx, ty)

  ########## DECIDE WHAT TO SPAWN ##########
  def doSpawning(self):
    spec = self.getSpecies(JELLYFISH)
    me = self.players[self.playerID]
    for cove in self.myCoves:
      if me.spawnFood < spec.cost:
        return
      spec.spawn(cove.x, cove.y)
    return

  ########## RUN ##########
  def run(self):
    print "Starting Turn #%i P1: %i P2: %i" % (self.turnNumber, self.players[0].currentReefHealth, self.players[1].currentReefHealth)
    self.getMyFish()
    self.getEnemyFish()
    self.getTrash()

    self.getCharGrid()
    self.gridHistory.append(self.charGrid)

    self.doSpawning()

    self.getCharGrid()
    self.gridHistory.append(self.charGrid)

    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
