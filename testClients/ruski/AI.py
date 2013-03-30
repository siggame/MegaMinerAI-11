#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import time
import math
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
    return

  ##This function is called once, after your last turn
  def end(self):
    print "The End"
    self.replayGrid()
    return

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
      self.charGrid[fish.x][fish.y] = 'F'
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

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print "Width: %i Height %i" % (self.mapWidth, self.mapHeight)
    print "Starting Turn #%i P1: %i P2: %i" % (self.turnNumber, self.players[0].currentReefHealth, self.players[1].currentReefHealth)

    #PRINT GRID
    self.getCharGrid()
    self.gridHistory.append(self.charGrid)

    #PRINT GRID
    self.getCharGrid()
    self.gridHistory.append(self.charGrid)

    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
