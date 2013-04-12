from base import *
from matchUtils import *
from objects import *
import networking.config.config
import networking.sexpr.sexpr
import itertools
import scribe
import jsonLogger
import random
from operator import itemgetter
from mapGenerator import set_tiles

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

    self.turnNumber = -1
    self.playerID = -1
    self.maxReefHealth = self.maxReefHealth
    self.gameNumber = id
    self.initialFood = self.initialFood
    self.maxReefHealth = self.maxReefHealth
    self.mapWidth = self.mapWidth
    self.mapHeight = self.mapHeight
    self.trashAmount = self.trashAmount
    self.boundLength = random.choice(range(1, self.boundLength))
    self.currentSeason = random.choice(range(4))
    self.seasonLength = self.seasonLength
    self.healPercent = self.healPercent
    self.maxFood = self.maxFood
    self.count = 0
    self.minTrash = self.minTrash
    self.offset = [(1,0),(-1,0),(0,1),(0,-1)]

    #TODO UPDATE TRASH LIST WHEN EVER TRASH IS MOVED. IT WILL BE A dictionary. (x,y) key tied to a trash amount.
    self.trashDict = dict()


  def getAdjacent(self,node):
     adjacent = []
     for adj in self.offset:
        dx=node[0]+adj[0]; dy = node[1]+adj[1]
        if 0<=dx<self.mapWidth and 0<=dy<self.mapHeight:
          adjacent.append((dx,dy))
          if (dx,dy) not in self.adjDict:
            self.adjDict[(dx,dy)] = 1
          else:
            self.adjDict[(dx,dy)] +=1
     return adjacent

  def covePath(self,seed):
    self.adjDict = dict()
    closed = set()
    open = [seed]
    coves = self.coveLimit
    self.adjDict[seed[0],seed[1]] = 0
    while coves>0 and len(open)>0:
      current = random.choice(open)
      open.remove(current)
      coves-=1
      self.getTile(current[0],current[1]).owner=0
      self.getTile(self.mapWidth-1-current[0],current[1]).owner = 1
      closed.add(current)
      neighbors = self.getAdjacent(current)
      for node in open:
        if self.adjDict[(node[0],node[1])] > 1:
          open.remove(node)
      for neighbor in neighbors:
        if neighbor in closed:
          continue
        else:
          open.append(neighbor)
    return True

  #getTile RETURN TILE
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
        self.addObject(Player, [connection.screenName, self.startTime, self.maxReefHealth, self.initialFood])
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
    trashableTiles = list(self.objects.tiles)
    while self.trashAmount > 0:
      randTile = random.choice(trashableTiles)
      if randTile.owner==2:
        trashableTiles.remove(randTile)
      while randTile.owner!=2:
        randTile = random.choice(trashableTiles)
        trashableTiles.remove(randTile)
      oppTile = self.getTile(self.mapWidth-randTile.x-1, randTile.y)

      if randTile.owner == 2 and (randTile.x,randTile.y) not in self.trashDict:
         val = random.randint(1,min([self.minTrash, self.trashAmount]))
         randTile.trashAmount += val
         self.trashDict[(randTile.x, randTile.y)] = val
         oppTile.trashAmount += val
         self.trashDict[(oppTile.x, oppTile.y)] = val
         self.trashAmount -= val
   # print sum(self.trashDict.values())
    return True

  def findDamage(self,player):
    damage = 0
    if player == 0:
      min = 0; max = self.mapWidth/2 + self.boundLength; owner = 0
    elif player == 1:
      min = self.mapWidth/2-self.boundLength; max = self.mapWidth; owner = 1
    for key in self.trashDict:
      if min <= key[0] < max:
        damage+=self.trashDict[key]
    #TODO: Deal star damage to reefs - need a whiteboard to see what conditions there are
  #  print("star damage",sum([star.attackPower for star in self.objects.fishes if star.species == "SeaStar" and star.attacksLeft>0 and min<=star.x<max and star.owner != player ]))
  #  print "player = %i, damage = %i"%(self.playerID,damage)
    return damage


  def start(self):
    if len(self.players) < 2:
      return "Game is not full"
    if self.winner is not None or self.turn is not None:
      return "Game has already begun"

    print "Starting game"

    self.grid = [[[ self.addObject(Tile,[x, y, 0, 2, False, -1]) ] for y in range(self.mapHeight)] for x in range(self.mapWidth)]
    for tile in self.objects.tiles:
      if tile.x < self.mapWidth/2 - self.boundLength:
        tile.damages = 0
      elif tile.x >= self.mapWidth/2 + self.boundLength:
        tile.damages = 1
    self.statList = ["name","index","cost", "maxHealth", "maxMovement", "carryCap", "attackPower", "range", "maxAttacks", "season"]
    self.turn = self.players[-1]
    self.turnNumber = -1
    self.seed = (0,self.mapHeight-1)
    set_tiles(self)
    self.spawnTrash()

    species = cfgSpecies.values()
    species.sort(key=itemgetter('index'))
    for s in species:
      self.addObject(Species, [s[value] for value in self.statList])

    self.initSeasons()
    self.speciesDict = {species.index:species for species in self.objects.speciesList}
    self.speciesStrings = {species.index:species.name for species in self.objects.speciesList}
    self.nextTurn()
    return True

  def nextTurn(self):
    #print "Next turn: %i P0: %i P1 %i" % (self.turnNumber, self.objects.players[0].currentReefHealth, self.objects.players[1].currentReefHealth)
    self.turnNumber += 1
    if self.turn == self.players[0]:
      self.turn = self.players[1]
      self.playerID = 1

    elif self.turn == self.players[1]:
      self.turn = self.players[0]
      self.playerID = 0

    else:
      return "Game is over."

    #change seasons if applicable
    if self.turnNumber % self.seasonLength == 0:
      self.currentSeason = (self.currentSeason + 1) % 4 #Modded by 4 in case of multiple years

    for obj in self.objects.values():
      obj.nextTurn()

    if self.turn == self.players[0]:
      pass #self.objects.players[0].currentReefHealth -= self.findDamage(0)

    elif self.turn == self.players[1]:
     self.objects.players[0].currentReefHealth -= self.findDamage(0)
     self.objects.players[1].currentReefHealth -= self.findDamage(1)

    self.checkWinner()
    if self.winner is None:
      self.sendStatus([self.turn] +  self.spectators)
    else:
      self.sendStatus(self.spectators)

    if self.logJson:
      self.dictLog['turns'].append(
        dict(
          maxReefHealth = self.maxReefHealth,
          boundLength = self.boundLength,
          turnNumber = self.turnNumber,
          playerID = self.playerID,
          gameNumber = self.gameNumber,
          mapWidth = self.mapWidth,
          mapHeight = self.mapHeight,
          trashAmount = self.trashAmount,
          currentSeason = self.currentSeason,
          seasonLength = self.seasonLength,
          healPercent = self.healPercent,
          maxFood = self.maxFood,
          Mappables = [i.toJson() for i in self.objects.values() if i.__class__ is Mappable],
          Species = [i.toJson() for i in self.objects.values() if i.__class__ is Species],
          Tiles = [i.toJson() for i in self.objects.values() if i.__class__ is Tile],
          Fishes = [i.toJson() for i in self.objects.values() if i.__class__ is Fish],
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
        for fish in self.objects.fishes:
          fishValues[fish.owner] += self.speciesDict[fish.species].cost
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
          for fish in self.objects.fishes:
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
    #del self.grid
    self.winner=winner
    print "Player", self.getPlayerIndex(self.winner) + 1, "wins game", self.id

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

  @derefArgs(Species, Tile)
  def spawn(self, object, tile):
    return object.spawn(tile, )

  @derefArgs(Fish, None, None)
  def move(self, object, x, y):
    return object.move(x, y, )

  @derefArgs(Fish, Tile, None)
  def pickUp(self, object, tile, weight):
    return object.pickUp(tile, weight, )

  @derefArgs(Fish, Tile, None)
  def drop(self, object, tile, weight):
    return object.drop(tile, weight, )

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
      i.writeSExpr(self.status(i))
      i.writeSExpr(self.animations)
    return True

  def initSeasons(self):
    #random distribution of seasons, assigns each species a random season
    randSeason = range(len(cfgSpecies.keys()))
    random.shuffle(randSeason)
    count = 0
    while count < len(randSeason):
      randSeason[count] = randSeason[count] % 4
      count += 1

    for num in range (len(self.objects.speciesList)):
      self.objects.speciesList[num].season = randSeason[num]

#    print [species.season for species in self.objects.speciesList]
    return True

  def status(self, connection):
    msg = ["status"]

    msg.append(["game", self.maxReefHealth, self.boundLength, self.turnNumber, self.playerID, self.gameNumber, self.mapWidth, self.mapHeight, self.trashAmount, self.currentSeason, self.seasonLength, self.healPercent, self.maxFood])

    typeLists = []
    typeLists.append(["Mappable"] + [i.toList() for i in self.objects.values() if i.__class__ is Mappable])
    updated = [i for i in self.objects.values() if i.__class__ is Tile and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["Tile"] + [i.toList() for i in updated])
    updated = [i for i in self.objects.values() if i.__class__ is Species and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["Species"] + [i.toList() for i in updated])
    typeLists.append(["Fish"] + [i.toList() for i in self.objects.values() if i.__class__ is Fish and (i.isVisible is 1 or i.owner is self.playerID or connection.type != "player")])
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
