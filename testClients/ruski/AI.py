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
  gridHistory = []

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
    self.replayGrid()
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
      if tile.hasEgg:
        self.charGrid[tile.x][tile.y] = 'E'
      #TRASH
      if tile.trashAmount > 0:
        self.charGrid[tile.x][tile.y] = 'T'

    #GET FISH
    for fish in self.fishes:
      self.charGrid[fish.x][fish.y] = 'F'

    return

  def replayGrid(self):
    wantReplay = True
    while wantReplay:
      for grid in self.gridHistory:
        time.sleep(0.25)
        self.printCharGrid(grid)
      print "Do you want to replay?: "
      usrinput = raw_input()
      if "y" in usrinput:
        wantReplay = True
      else:
        wantReplay = False
    return

  #PRINT CHARACTER GRID
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

  #VALID MOVE
  def validMove(self, x, y, tx, ty):
    self.getMyTrash()
    if tx < 0 or tx >= self.mapWidth:
      return False
    if ty < 0 or ty >= self.mapHeight:
      return False

    taxiDist = self.taxicabDist(x, y, tx, ty)
    #print "Taxi Dist: %i" % taxiDist
    if taxiDist > 1:
      return False
    for fish in self.fishes:
      if fish.x == tx and fish.y == ty:
        return False

    intoTile = self.tiles[ ty*self.mapWidth + tx ]
    #Cannot move onto trash
    if intoTile.trashAmount > 0:
      return False

    #Cannot move onto opponent cove
    if intoTile.owner == abs(self.playerID - 1):
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
    #Drop trash if ind enemy territory
    if fish.x > self.mapWidth/2 - self.boundLength:
      if fish.carryingWeight > 0:
        if self.validMove(fish.x, fish.y, fish.x, fish.y+1):
          fish.drop(fish.x, fish.y+1, fish.carryingWeight)

        elif self.validMove(fish.x, fish.y, fish.x, fish.y-1):
          fish.drop(fish.x, fish.y-1, fish.carryingWeight)

        elif self.validMove(fish.x, fish.y, fish.x+1, fish.y):
          fish.drop(fish.x+1, fish.y, fish.carryingWeight)

        elif self.validMove(fish.x, fish.y, fish.x-1, fish.y):
          fish.drop(fish.x-1, fish.y, fish.carryingWeight)

    return


  def handlePickUp(self, fish):
    for trash in self.myTrash:
      #If trash is nearby
      if self.taxicabDist(fish.x, fish.y, trash.x, trash.y) == 1:
        if fish.carryingWeight < 2*fish.carryCap/3:
          pickAmount = fish.carryCap - fish.carryingWeight
          if pickAmount > trash.trashAmount:
            pickAmount = trash.trashAmount
          fish.pickUp(trash.x, trash.y, pickAmount)

    return

  def handleEnemy(self, fish):
    for enemyF in self.enemyFish:
      if self.taxicabDist(fish.x, fish.y, enemyF.x, enemyF.y) == 1:
        fish.attack(enemyF)
    return

  def handleMovement(self, fish):
    for _ in range(fish.maxMovement):
      if self.validMove(fish.x, fish.y, fish.x+1, fish.y) == True:
        if not fish.move(fish.x+1, fish.y):
          print "Bad movement"

      elif self.validMove(fish.x, fish.y, fish.x, fish.y+1 == True):
        if not fish.move(fish.x, fish.y+1):
          print "Bad movement"

      elif self.validMove(fish.x, fish.y, fish.x, fish.y-1) == True:
        if not fish.move(fish.x, fish.y-1):
          print "Bad movement"

      elif self.validMove(fish.x, fish.y, fish.x-1, fish.y) == True:
        if not fish.move(fish.x-1, fish.y):
          print "Bad movement"

    return

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print "Starting Turn #%i P1: %i P2: %i" % (self.turnNumber, self.players[0].currentReefHealth, self.players[1].currentReefHealth)
    #GET LOCAL LISTS
    self.getMyFish()
    self.getEnemyFish()
    self.getMyTrash()

    #PRINT GRID
    self.getCharGrid()
    self.gridHistory.append(self.charGrid)

    self.actMyFish()

    #PRINT GRID
    self.getCharGrid()
    self.gridHistory.append(self.charGrid)

    for _ in range(10):
      for spec in self.species:
        cove = random.choice(self.coves)
        self.attemptSpawn(cove.x, cove.y, spec)


    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
