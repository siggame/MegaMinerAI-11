# -*- python -*-

from library import library

class BaseAI:
  """@brief A basic AI interface.

  This class implements most the code an AI would need to interface with the lower-level game code.
  AIs should extend this class to get a lot of builer-plate code out of the way
  The provided AI class does just that.
  """
  #\cond
  initialized = False
  iteration = 0
  runGenerator = None
  connection = None
  #\endcond
  mappables = []
  tiles = []
  speciesList = []
  fishes = []
  players = []
  #\cond
  def startTurn(self):
    from GameObject import Mappable
    from GameObject import Tile
    from GameObject import Species
    from GameObject import Fish
    from GameObject import Player

    BaseAI.mappables = [Mappable(library.getMappable(self.connection, i)) for i in xrange(library.getMappableCount(self.connection))]
    BaseAI.tiles = [Tile(library.getTile(self.connection, i)) for i in xrange(library.getTileCount(self.connection))]
    BaseAI.speciesList = [Species(library.getSpecies(self.connection, i)) for i in xrange(library.getSpeciesCount(self.connection))]
    BaseAI.fishes = [Fish(library.getFish(self.connection, i)) for i in xrange(library.getFishCount(self.connection))]
    BaseAI.players = [Player(library.getPlayer(self.connection, i)) for i in xrange(library.getPlayerCount(self.connection))]

    if not self.initialized:
      self.initialized = True
      self.init()
    BaseAI.iteration += 1;
    if self.runGenerator:
      try:
        return self.runGenerator.next()
      except StopIteration:
        self.runGenerator = None
    r = self.run()
    if hasattr(r, '__iter__'):
      self.runGenerator = r
      return r.next()
    return r
  #\endcond
  #\cond
  def getMaxReefHealth(self):
    return library.getMaxReefHealth(self.connection)
  #\endcond
  maxReefHealth = property(getMaxReefHealth)
  #\cond
  def getBoundLength(self):
    return library.getBoundLength(self.connection)
  #\endcond
  boundLength = property(getBoundLength)
  #\cond
  def getTurnNumber(self):
    return library.getTurnNumber(self.connection)
  #\endcond
  turnNumber = property(getTurnNumber)
  #\cond
  def getPlayerID(self):
    return library.getPlayerID(self.connection)
  #\endcond
  playerID = property(getPlayerID)
  #\cond
  def getGameNumber(self):
    return library.getGameNumber(self.connection)
  #\endcond
  gameNumber = property(getGameNumber)
  #\cond
  def getMapWidth(self):
    return library.getMapWidth(self.connection)
  #\endcond
  mapWidth = property(getMapWidth)
  #\cond
  def getMapHeight(self):
    return library.getMapHeight(self.connection)
  #\endcond
  mapHeight = property(getMapHeight)
  #\cond
  def getTrashAmount(self):
    return library.getTrashAmount(self.connection)
  #\endcond
  trashAmount = property(getTrashAmount)
  #\cond
  def getCurrentSeason(self):
    return library.getCurrentSeason(self.connection)
  #\endcond
  currentSeason = property(getCurrentSeason)
  #\cond
  def getSeasonLength(self):
    return library.getSeasonLength(self.connection)
  #\endcond
  seasonLength = property(getSeasonLength)
  #\cond
  def getHealPercent(self):
    return library.getHealPercent(self.connection)
  #\endcond
  healPercent = property(getHealPercent)
  #\cond
  def getMaxFood(self):
    return library.getMaxFood(self.connection)
  #\endcond
  maxFood = property(getMaxFood)
  def __init__(self, connection):
    self.connection = connection

  #Returns index of fish at X, Y in self.fishes list
  #Returns -1 if a fish is not found
  def getFishIndex(self, x, y):
    index = -1
    for fish in self.fishes:
      index += 1
      if fish.x is x and fish.y is y:
        return index
    return -1

  #Returns the tile based of off x and y
  def getTile(self, x, y):
    return self.tiles[x * self.mapHeight + y]
