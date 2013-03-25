#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import time
import os


class AI(BaseAI):
  """The class implementing gameplay logic."""

  coves = []
  myFish = []
  enemyFish = []
  myTrash = []
  charGrid = [[]]

  @staticmethod
  def username():
    return "ruski"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    print "Init"
    #Coves will never change. Only needs to be done once.
    self.getCoves()
    return

  ##This function is called once, after your last turn
  def end(self):
    print "The End"
    return

  #GET COVES
  def getCoves(self):
    print "Find coves."
    self.coves = []
    for tile in self.tiles:
      if tile.owner is self.getPlayerID():
        self.coves.append(tile)
    return

  #GET MY FISH
  def getMyFish(self):
    self.myFish = []
    for fish in self.fishes:
      if fish.owner is self.playerID:
        self.myFish.append(fish)
    return

  #GET ENEMY FISH
  def getEnemyFish(self):
    self.enemyFish = []
    for fish in self.fishes:
      if fish.owner is abs(self.playerID - 1):
        self.enemyFish.append(fish)
    return

  #GET TRASH TILES
  def getMyTrash(self):
    self.myTrash = []
    for tile in self.tiles:
      if tile.trashAmount > 0:
        self.myTrash.append(tile)
    return

  #GET CHARACTER GRID
  def getCharGrid(self):
    #RESET GRID
    self.charGrid = [[' ' for _ in range(self.getMapHeight())] for _ in range(self.getMapWidth()) ]

    #GET TILES AND TRASH
    for tile in self.tiles:
      #COVE
      if tile.owner != 2:
        self.charGrid[tile.x][tile.y] = 'C'
      #TRASH
      if tile.trashAmount > 0:
        self.charGrid[tile.x][tile.y] = 'T'

    #GET FISH
    for fish in self.fishes:
      self.charGrid[fish.x][fish.y] = 'F'

    return

  #PRINT CHARACTER GRID
  def printCharGrid(self):
    for y in range(self.getMapHeight()):
      for x in range(self.getMapWidth()):
        print self.charGrid[x][y],
      print
    return

  #VALID MOVE
  def validMove(self, x, y):
    if x < 0 or x >= self.mapWidth:
      return False
    if y < 0 or y >= self.mapHeight:
      return False
    for fish in self.fishes:
      if fish.x == x and fish.y == y:
        return False
    for trash in self.myTrash:
      if trash.x == x and trash.y == y:
        return False
    for cove in self.coves:
      if cove.x == x and cove.y == y and cove.owner != self.playerID:
        return False

    return True

  #ATTEMPT SPAWN
  def attemptSpawn(self, x, y, species):
    me = self.players[self.playerID]
    if x < 0 or x > self.mapWidth:
      return False
    if y < 0 or y > self.mapHeight:
      return False

    if self.getCurrentSeason() is not species.season:
      return False

    if me.spawnFood < species.cost:
      return False

    for fish in self.fishes:
      if fish.x == x and fish.y == y:
        return False

    if self.tiles[ self.mapHeight*y + x ].hasEgg:
      return False

    species.spawn(x, y)
    print "Spawning %s at (%i, %i)" % (species.name, x, y)
    return True

  def taxicabDist(self, x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)

  #ACT MY FISH
  def actMyFish(self):
    for fish in self.myFish:

      #HANDLE PICKUP
      self.handlePickUp(fish)

      #HANDLE DROP
      self.handleDrop(fish)

      #HANDLE ENEMY
      self.handleEnemy(fish)

      #HANDLE MOVEMENT
      self.handleMovement(fish)

    return

  def handleDrop(self, fish):
    self.getMyTrash()
    #Drop trash if ind enemy territory
    if fish.x > self.mapWidth/2 - self.boundLength:
      if fish.carryingWeight > 0:
        if self.validMove(fish.x, fish.y+1):
          fish.drop(fish.x, fish.y+1, fish.carryingWeight)
        elif self.validMove(fish.x, fish.y-1):
          fish.drop(fish.x, fish.y-1, fish.carryingWeight)
        elif self.validMove(fish.x+1, fish.y):
          fish.drop(fish.x+1, fish.y, fish.carryingWeight)
        elif self.validMove(fish.x-1, fish.y):
          fish.drop(fish.x-1, fish.y, fish.carryingWeight)
    return


  def handlePickUp(self, fish):
    self.getMyTrash()
    for trash in self.myTrash:
      #If trash is nearby
      if self.taxicabDist(fish.x, fish.y, trash.x, trash.y) == 1:
        if fish.carryingWeight < fish.carryCap:
          pickAmount = fish.carryCap - fish.carryingWeight
          if pickAmount > trash.trashAmount:
            pickAmount = trash.trashAmount
          fish.pickUp(trash.x, trash.y, pickAmount)

    return

  def handleEnemy(self, fish):
    self.getEnemyFish()
    for enemyF in self.enemyFish:
      if self.taxicabDist(fish.x, fish.y, enemyF.x, enemyF.y) == 1:
        fish.attack(enemyF)
    return

  def handleMovement(self, fish):
    self.getMyTrash()
    for _ in range(fish.maxMovement):
      if self.validMove(fish.x+1, fish.y):
        fish.move(fish.x+1, fish.y)
      elif self.validMove(fish.x, fish.y+1):
        fish.move(fish.x, fish.y+1)
      elif self.validMove(fish.x, fish.y-1):
        fish.move(fish.x, fish.y-1)
    return

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print "Starting Turn #%i P1: %i P2: %i" % (self.turnNumber, self.players[0].currentReefHealth, self.players[1].currentReefHealth)
    #GET LOCAL LISTS
    self.getMyFish()
    self.getMyTrash()

    #PRINT GRID
    self.getCharGrid()
    self.printCharGrid()

    self.actMyFish()

    for spec in self.species:
      for cove in self.coves:
        self.attemptSpawn(cove.x, cove.y, spec)


    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
