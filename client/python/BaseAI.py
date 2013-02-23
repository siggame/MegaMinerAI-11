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
  fishSpeciess = []
  tiles = []
  fishs = []
  players = []
  #\cond
  def startTurn(self):
    from GameObject import Mappable
    from GameObject import FishSpecies
    from GameObject import Tile
    from GameObject import Fish
    from GameObject import Player

    BaseAI.mappables = [Mappable(library.getMappable(self.connection, i)) for i in xrange(library.getMappableCount(self.connection))]
    BaseAI.fishSpeciess = [FishSpecies(library.getFishSpecies(self.connection, i)) for i in xrange(library.getFishSpeciesCount(self.connection))]
    BaseAI.tiles = [Tile(library.getTile(self.connection, i)) for i in xrange(library.getTileCount(self.connection))]
    BaseAI.fishs = [Fish(library.getFish(self.connection, i)) for i in xrange(library.getFishCount(self.connection))]
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
  def getSpawnFoodPerTurn(self):
    return library.getSpawnFoodPerTurn(self.connection)
  #\endcond
  spawnFoodPerTurn = property(getSpawnFoodPerTurn)
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
  def getTurnsTillSpawn(self):
    return library.getTurnsTillSpawn(self.connection)
  #\endcond
  turnsTillSpawn = property(getTurnsTillSpawn)
  #\cond
  def getMaxReefHealth(self):
    return library.getMaxReefHealth(self.connection)
  #\endcond
  maxReefHealth = property(getMaxReefHealth)
  #\cond
  def getTrashDamage(self):
    return library.getTrashDamage(self.connection)
  #\endcond
  trashDamage = property(getTrashDamage)
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
  def __init__(self, connection):
    self.connection = connection
