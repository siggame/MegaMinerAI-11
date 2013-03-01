from base import *
from matchUtils import *
from objects import *
import networking.config.config
from collections import defaultdict
from networking.sexpr.sexpr import *
import os
import itertools
import scribe
import jsonLogger
import random
import math

Scribe = scribe.Scribe

def loadClassDefaults(cfgFile = "config/defaults.cfg"):
  cfg = networking.config.config.readConfig(cfgFile)
  for className in cfg.keys():
    for attr in cfg[className]:
      setattr(eval(className), attr, cfg[className][attr])

class Match(DefaultGameWorld):
  def __init__(self, id, controller):
    self.id = int(id)
    self.controller = controller
    DefaultGameWorld.__init__(self)
    self.scribe = Scribe(self.logPath())
    if( self.logJson ):
      self.jsonLogger = jsonLogger.JsonLogger(self.logPath())
      self.jsonAnimations = []
      self.dictLog = dict(gameName = "Reef", turns = [])
    self.addPlayer(self.scribe, "spectator")

    #TODO: INITIALIZE THESE!
    self.turnNumber = -1
    self.playerID = -1
    self.gameNumber = id
    
    self.initialFood = self.initialFood
    self.sharedLowerBound = self.sharedLowerBound
    self.sharedUpperBound = self.sharedUpperBound
    self.spawnFoodPerTurn = self.spawnFoodPerTurn
    self.turnsTillSpawn = self.turnsTillSpawn
    self.maxReefHealth = self.maxReefHealth
    self.trashDamage = self.trashDamage
    self.mapWidth = self.mapWidth
    self.mapHeight = self.mapHeight
    self.trashAmount = self.trashAmount
    self.coveX = self.coveX
    self.coveY = self.coveY

    # Helper function
    def getTileOwner(x):
      if x < self.sharedLowerBound:
        return 1
      elif x > self.sharedUpperBound:
        return 2
      else:
        return 3
    #Make grid		
    self.grid = [[[self.addObject(Tile, x, y, 0, getTileOwner(x), False)] for y in range(self.mapHeight)] for x in range(self.mapWidth)]
    
  #getTile RETURN [TILE]
  def getTile(self, x, y):
    return [ self.grid[x][y][0] ]
  
  #getFish RETURN LIST OF FISH
  def getFish(self, x, y):
    return self.grid[x][y][1:]

  #def getObject(self, x, y):
  #  if len(self.grid[x][y]) > 1:
  #    return self.grid[x][y][1]
  #  else:
  #    return None

  #this is here to be wrapped
  def __del__(self):
    pass

  def addPlayer(self, connection, type="player"):
    connection.type = type
    if len(self.players) >= 2 and type == "player":
      return "Game is full"
    if type == "player":
      self.players.append(connection)
      try:
        #500 and 0 are place holder values for default initial reef health and initial reef food
        self.addObject(Player, [connection.screenName, self.startTime, 500, 0 ])
      except TypeError:
        raise TypeError("Someone forgot to add the extra attributes to the Player object initialization")
    elif type == "spectator":
      self.spectators.append(connection)
      #If the game has already started, send them the ident message
      if (self.turn is not None):
        self.sendIdent([connection])
    return True

  def removePlayer(self, connection):
    if connection in self.players:
      if self.turn is not None:
        winner = self.players[1 - self.getPlayerIndex(connection)]
        self.declareWinner(winner, 'Opponent Disconnected')
      self.players.remove(connection)
    else:
      self.spectators.remove(connection)

  def spawnTrash(self):
    #Set coves on left side
    for tile in self.objects.tiles:
      if tile.x < self.coveX and tile.y > self.mapHeight- self.coveY:
        tile.isCove = True
    #Set coves on right side
    for tile in self.objects.tiles:
      if tile.x > self.mapWidth-self.coveX and tile.y > self.mapHeight-self.coveY:
        tile.isCove = True

    #RANDOM ALGORITHM
    #Loop trashAmount number of times
    trashCur = 0
    trashMax = 500
    while(trashCur < self.trashAmount):
      #Create random X and random Y
      randX = random.randint(0, (self.mapWidth)//2)
      randY = random.randint(0, (self.mapWidth)//2)

      #Find tile at random X and random Y position
      randTile = None
      for tile in self.objects.tiles:
        if isinstance(tile, Tile):
          randTile = tile
      
      if randTile is None:
        return "Error in getting randTile"    
      
      #If tile isCove
      if randTile.isCove is True:
        #Rerun loop (subtract/add one to index)
        continue
      #Else if tile trashAmount >= trashMax
      elif randTile.trashAmount >= trashMax:
        #Rerun loop (subtract/add one to index)
        continue
      #Else
      else:
        #Increment trashAmount by 1
        randTile.trashAmount += 1
        trashCur += 1

    return True
    
  def start(self):
    if len(self.players) < 2:
      return "Game is not full"
    if self.winner is not None or self.turn is not None:
      return "Game has already begun"

    #TODO: START STUFF
    self.turn = self.players[-1]
    self.turnNumber = -1
    self.spawnTrash()

    self.nextTurn()
    return True


  def nextTurn(self):
    self.turnNumber += 1
    if self.turn == self.players[0]:
      self.turn = self.players[1]
      self.playerID = 1
    elif self.turn == self.players[1]:
      self.turn = self.players[0]
      self.playerID = 0

    else:
      return "Game is over."

    for obj in self.objects.values():
      obj.nextTurn()

    self.checkWinner()
    if self.winner is None:
      self.sendStatus([self.turn] +  self.spectators)
    else:
      self.sendStatus(self.spectators)
    
    if( self.logJson ):
      self.dictLog['turns'].append(
        dict(
          initialFood = self.initialFood,
          sharedLowerBound = self.sharedLowerBound,
          sharedUpperBound = self.sharedUpperBound,
          spawnFoodPerTurn = self.spawnFoodPerTurn,
          turnNumber = self.turnNumber,
          playerID = self.playerID,
          gameNumber = self.gameNumber,
          turnsTillSpawn = self.turnsTillSpawn,
          maxReefHealth = self.maxReefHealth,
          trashDamage = self.trashDamage,
          mapWidth = self.mapWidth,
          mapHeight = self.mapHeight,
          trashAmount = self.trashAmount,
          coveX = self.coveX,
          coveY = self.coveY,
          Mappables = [i.toJson() for i in self.objects.values() if i.__class__ is Mappable],
          FishSpeciess = [i.toJson() for i in self.objects.values() if i.__class__ is FishSpecies],
          Tiles = [i.toJson() for i in self.objects.values() if i.__class__ is Tile],
          Fishs = [i.toJson() for i in self.objects.values() if i.__class__ is Fish],
          Players = [i.toJson() for i in self.objects.values() if i.__class__ is Player],
          animations = self.jsonAnimations
        )
      )
      self.jsonAnimations = []

    self.animations = ["animations"]
    return True

  def checkWinner(self):
    # Get the players
    player1 = self.objects.players[0]
    player2 = self.objects.players[1]
    # Get the current reef healths
    p1h = player1.currentReefHealth
    p2h = player2.currentReefHealth
    # The game should end if any of these conditions are met
    if p1h <= 0 or p2h <= 0 or self.turnNumber >= self.turnLimit:
      # Player 2 wins if Player 1's health is lower
      if p1h < p2h:
        self.declareWinner(self.players[1], "Player 2 wins through reef survival")
      # Player 1 wins if Player 2's health is lower
      elif p2h < p1h:
        self.declareWinner(self.players[0], "Player 1 wins through reef survival")
      # The game must end, but both players have the same reef health.  Resort to secondary criteria
      else:
        # Start by computing the total value of all fish for each player
        fishValues = [0, 0]
        for fish in self.objects.fishs:
          fishValues[fish.owner] += cfgSpecies[fish.species]["cost"]
        # Now compare!
        # Player 1 wins if they have the higher value school of fish
        if fishValues[0] > fishValues[1]:
          self.declareWinner(self.players[0], "Player 1 wins by total fish value")
        # Player 2 wins if they have the higher value school of fish
        elif fishValues[1] > fishValues[0]:
          self.declareWinner(self.players[1], "Player 2 wins by total fish value")
        # Otherwise, both players have the same value of fish
        else:
          # Start by computing the total health of all fish for each player
          fishHealths = [0, 0]
          for fish in self.objects.fishs:
            fishHealths[fish.owner] += fish.currentHealth
          # Now compare!
          # Player 1 wins if they have the school of fish with more health
          if fishHealths[0] > fishHealths[1]:
            self.declareWinner(self.players[0], "Player 1 wins by total fish health")
          # Player 2 wins if they have the school of fish with more health
          elif fishHealths[1] > fishHealths[0]:
            self.declareWinner(self.players[1], "Player 2 wins by total fish health")
          # Otherwise, both players have the same fish health
          else:
            # At this point, we consider the AIs identical and it doesn't matter who we pick to win
            self.declareWinner(self.players[0], "Player 1 wins because they connected first")

  def declareWinner(self, winner, reason=''):
    #DELETE GRID
    del self.grid
    print "Player", self.getPlayerIndex(self.winner), "wins game", self.id
    self.winner = winner

    msg = ["game-winner", self.id, self.winner.user, self.getPlayerIndex(self.winner), reason]
    
    if( self.logJson ):
      self.dictLog["winnerID"] =  self.getPlayerIndex(self.winner)
      self.dictLog["winReason"] = reason
      self.jsonLogger.writeLog( self.dictLog )
    
    self.scribe.writeSExpr(msg)
    self.scribe.finalize()
    self.removePlayer(self.scribe)

    for p in self.players + self.spectators:
      p.writeSExpr(msg)
    
    self.sendStatus([self.turn])
    self.playerID ^= 1
    self.sendStatus([self.players[self.playerID]])
    self.playerID ^= 1
    self.turn = None
    self.objects.clear()

  def logPath(self):
    return "logs/" + str(self.id)

  @derefArgs(FishSpecies, None, None)
  def spawn(self, object, x, y):
    return object.spawn(x, y, )

  @derefArgs(Fish, None, None)
  def move(self, object, x, y):
    return object.move(x, y, )

  @derefArgs(Fish, None, None, None)
  def pickUp(self, object, x, y, weight):
    return object.pickUp(x, y, weight, )

  @derefArgs(Fish, None, None, None)
  def drop(self, object, x, y, weight):
    return object.drop(x, y, weight, )

  @derefArgs(Fish, None, None)
  def attack(self, object, x, y):
    return object.attack(x, y, )

  @derefArgs(Player, None)
  def talk(self, object, message):
    return object.talk(message, )


  def sendIdent(self, players):
    if len(self.players) < 2:
      return False
    list = []
    for i in itertools.chain(self.players, self.spectators):
      list += [[self.getPlayerIndex(i), i.user, i.screenName, i.type]]
    for i in players:
      i.writeSExpr(['ident', list, self.id, self.getPlayerIndex(i)])

  def getPlayerIndex(self, player):
    try:
      playerIndex = self.players.index(player)
    except ValueError:
      playerIndex = -1
    return playerIndex

  def sendStatus(self, players):
    for i in players:
      i.writeSExpr(self.status())
      i.writeSExpr(self.animations)
    return True


  def status(self):
    msg = ["status"]

    msg.append(["game", self.initialFood, self.sharedLowerBound, self.sharedUpperBound, self.spawnFoodPerTurn, self.turnNumber, self.playerID, self.gameNumber, self.turnsTillSpawn, self.maxReefHealth, self.trashDamage, self.mapWidth, self.mapHeight, self.trashAmount, self.coveX, self.coveY])

    typeLists = []
    typeLists.append(["Mappable"] + [i.toList() for i in self.objects.values() if i.__class__ is Mappable])
    typeLists.append(["FishSpecies"] + [i.toList() for i in self.objects.values() if i.__class__ is FishSpecies])
    typeLists.append(["Tile"] + [i.toList() for i in self.objects.values() if i.__class__ is Tile])
    typeLists.append(["Fish"] + [i.toList() for i in self.objects.values() if i.__class__ is Fish])
    typeLists.append(["Player"] + [i.toList() for i in self.objects.values() if i.__class__ is Player])

    msg.extend(typeLists)

    return msg

  def addAnimation(self, anim):
    # generate the sexp
    self.animations.append(anim.toList())
    # generate the json
    if( self.logJson ):
      self.jsonAnimations.append(anim.toJson())
  


loadClassDefaults()

