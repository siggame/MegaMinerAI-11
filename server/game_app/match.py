from base import *
from matchUtils import *
from objects import *
import networking.config.config
import networking.sexpr.sexpr
import itertools
import scribe
import jsonLogger
import random

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
    if self.logJson:
      self.jsonLogger = jsonLogger.JsonLogger(self.logPath())
      self.jsonAnimations = []
      self.dictLog = dict(gameName = "Reef", turns = [])
    self.addPlayer(self.scribe, "spectator")

    #TODO: INITIALIZE THESE!
    self.turnNumber = -1
    self.playerID = -1
    self.gameNumber = id 
    self.initialFood = self.initialFood
    self.spawnFoodPerTurn = self.spawnFoodPerTurn
    self.maxReefHealth = self.maxReefHealth
    self.trashDamage = self.trashDamage
    self.mapWidth = self.mapWidth
    self.mapHeight = self.mapHeight
    self.trashAmount = self.trashAmount
    self.boundLength = self.boundLength
    self.currentSeason = self.currentSeason
    self.seasonLength = self.seasonLength

    #Make grid
    self.grid = [[[self.addObject(Tile,[x, y, 0, self.getTileOwner(x,y)])] for y in range(self.mapHeight)] for x in range(self.mapWidth)]
    
    #TODO UPDATE TRASH LIST WHEN EVER TRASH IS MOVED. IT WILL BE A dictionary. (x,y) key tied to a trash amount. 
    self.trashDict = []

  # Helper function
  #since ownership only matter on cove tiles, we're making an owned tile a cove. 
  def getTileOwner(self,x,y):
    if x < 3 and y<3:
      return 1
    elif x>self.mapWidth-3 and y<3:
      return 2
    else:
      return 3
    
  #getTile RETURN [TILE]
  def getTile(self, x, y):
    return  self.grid[x][y][0] 
  
  #getFish RETURN LIST OF FISH
  def getFish(self, x, y):
    return self.grid[x][y][1:]

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
        #Add Player and Player attributes  
        self.addObject(Player, [connection.screenName, self.startTime, self.initialFood, self.maxReefHealth ])
      except TypeError:
        raise TypeError("Someone forgot to add the extra attributes to the Player object initialization")
    elif type == "spectator":
      self.spectators.append(connection)
      #If the game has already started, send them the ident message
      if self.turn is not None:
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
    print("START spawnTrash(self)")
    #RANDOM ALGORITHM
    #Loop trashAmount number of times
    print "START RANDOM TRASH GENERATION"
    trashCur = 0 #Current number of trash created
    #self.trashAmount Total amount of trash
    trashMax = self.trashAmount
    while(self.trashAmount>0):
      #Create random X and random Y
      print ("CREATE RANDOM X AND Y")
      randX = random.randint(0, (self.mapWidth/2)//2)
      randY = random.randint(0, (self.mapHeight)//2)

      #Find tile at random X and random Y position
      randTile = self.getTile(randX, randY)
      oppTile = self.getTile(self.mapWidth-randX-1, randY)
      
      if isinstance(randTile,Tile) and randTile.owner==3:
          print "Trash was spawned"
          val=random.randint(1,self.trashAmount)
          randTile.trashAmount+=val
          oppTile.trashAmount+=val
          self.trashAmount-=val
           #TODO UPDATE TRASH DICT
          print 'val = %i , and self.trashAmount = %i '%(val,self.trashAmount)
      
    print("END RANDOM TRASH GENERATION")
    return True
     
  def start(self):
    print("GAME STARTED")
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

  def getTrashLeft(self):
    totalTrash = 0
    #is this right? --- This works. But it runs at O(w*h), and can be done more efficiently. I'll bring this up or make an issue, for now this works.  
    for x in range(0,self.mapWidth/2-self.boundLength):
      for y in range(0,self.mapHeight):
        totalTrash += self.getTile(x,y).trashAmount
    return totalTrash
    
  def getTrashShared(self):
    totalTrash = 0
    #I think these bounds are right?
    for x in range(self.mapWidth/2-self.boundLength,self.mapWidth/2+self.boundLength):
      for y in range(0,self.mapHeight):
        totalTrash += self.getTile(x,y).trashAmount
    return totalTrash
    
  def getTrashRight(self):
    totalTrash = 0
    #Comment to remind who so ever changes this to change all of the bounds
    for x in range(self.mapWidth/2+self.boundLength,self.mapWidth):
      for y in range(0,self.mapHeight):
        totalTrash += self.getTile(x,y).trashAmount
    return totalTrash

  def nextTurn(self):
    print "TURN NUMBER: %i"% self.turnNumber
    print self.playerID
    self.turnNumber += 1
    print "---------------------------"
    print self.objects.players
    print "-------------------------"
    if self.turn == self.players[0]:
      #deal damage to the left-side player
      self.objects.players[0].currentReefHealth -= (self.getTrashLeft() + self.getTrashShared()) * self.trashDamage

      self.turn = self.players[1]
      self.playerID = 1
    elif self.turn == self.players[1]:
      #deal damage to the left-side player
      self.objects.players[1].currentReefHealth -= (self.getTrashRight() + self.getTrashShared()) * self.trashDamage

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
    
    if self.logJson:
      self.dictLog['turns'].append(
        dict(
          boundLength = self.boundLength,
          turnNumber = self.turnNumber,
          playerID = self.playerID,
          gameNumber = self.gameNumber,
          trashDamage = self.trashDamage,
          mapWidth = self.mapWidth,
          mapHeight = self.mapHeight,
          trashAmount = self.trashAmount,
          currentSeason = self.currentSeason,
          seasonLength = self.seasonLength,
          Mappables = [i.toJson() for i in self.objects.values() if i.__class__ is Mappable],
          Speciess = [i.toJson() for i in self.objects.values() if i.__class__ is Species],
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
    print "----------------------------"
    print self.objects.players
    print "----------------------"
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
    
    if self.logJson:
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

  @derefArgs(Species, None, None)
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

  @derefArgs(Fish, Fish)
  def attack(self, object, target):
    return object.attack(target, )

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

    msg.append(["game", self.boundLength, self.turnNumber, self.playerID, self.gameNumber, self.trashDamage, self.mapWidth, self.mapHeight, self.trashAmount, self.currentSeason, self.seasonLength])

    typeLists = []
    typeLists.append(["Mappable"] + [i.toList() for i in self.objects.values() if i.__class__ is Mappable])
    typeLists.append(["Species"] + [i.toList() for i in self.objects.values() if i.__class__ is Species])
    typeLists.append(["Tile"] + [i.toList() for i in self.objects.values() if i.__class__ is Tile])
    typeLists.append(["Fish"] + [i.toList() for i in self.objects.values() if i.__class__ is Fish])
    typeLists.append(["Player"] + [i.toList() for i in self.objects.values() if i.__class__ is Player])

    msg.extend(typeLists)

    return msg

  def addAnimation(self, anim):
    # generate the sexp
    self.animations.append(anim.toList())
    # generate the json
    if self.logJson:
      self.jsonAnimations.append(anim.toJson())
  


loadClassDefaults()
