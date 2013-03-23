# -*- python -*-

from library import library

from ExistentialError import ExistentialError

class GameObject(object):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration


##A mappable object!
class Mappable(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.mappableGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.mappables:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  #\cond
  def getId(self):
    self.validify()
    return library.mappableGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.mappableGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.mappableGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    return ret

##Represents a single tile on the map, can contain some amount of trash or be a cove (spawn point).
class Tile(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.tileGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.tiles:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  #\cond
  def getId(self):
    self.validify()
    return library.tileGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.tileGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.tileGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)

  #\cond
  def getTrashAmount(self):
    self.validify()
    return library.tileGetTrashAmount(self._ptr)
  #\endcond
  ##The amount of trash on this tile
  trashAmount = property(getTrashAmount)

  #\cond
  def getOwner(self):
    self.validify()
    return library.tileGetOwner(self._ptr)
  #\endcond
  ##The owner of the tile if it is part of a cove
  owner = property(getOwner)

  #\cond
  def getHasEgg(self):
    self.validify()
    return library.tileGetHasEgg(self._ptr)
  #\endcond
  ##Determines of a fish is set to spawn on this cove
  hasEgg = property(getHasEgg)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "trashAmount: %s\n" % self.getTrashAmount()
    ret += "owner: %s\n" % self.getOwner()
    ret += "hasEgg: %s\n" % self.getHasEgg()
    return ret

##This class describes the characteristics for each type of fish. A groundbased fish is damaged each time it ends a turn above the groundBound Y value. Also, a species will only be available For so long, and new species will become available as a match progreses. 
class Species(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.speciesGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.species:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Have a new fish spawn and join the fight!
  def spawn(self, x, y):
    self.validify()
    return library.speciesSpawn(self._ptr, x, y)

  #\cond
  def getId(self):
    self.validify()
    return library.speciesGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getName(self):
    self.validify()
    return library.speciesGetName(self._ptr)
  #\endcond
  ##The name of this species
  name = property(getName)

  #\cond
  def getIndex(self):
    self.validify()
    return library.speciesGetIndex(self._ptr)
  #\endcond
  ##The species index of the species.
  index = property(getIndex)

  #\cond
  def getCost(self):
    self.validify()
    return library.speciesGetCost(self._ptr)
  #\endcond
  ##The amount of food it takes to raise this fish
  cost = property(getCost)

  #\cond
  def getMaxHealth(self):
    self.validify()
    return library.speciesGetMaxHealth(self._ptr)
  #\endcond
  ##The maximum health of this fish
  maxHealth = property(getMaxHealth)

  #\cond
  def getMaxMovement(self):
    self.validify()
    return library.speciesGetMaxMovement(self._ptr)
  #\endcond
  ##The maximum number of movements in a turn
  maxMovement = property(getMaxMovement)

  #\cond
  def getCarryCap(self):
    self.validify()
    return library.speciesGetCarryCap(self._ptr)
  #\endcond
  ##The total weight the fish can carry
  carryCap = property(getCarryCap)

  #\cond
  def getAttackPower(self):
    self.validify()
    return library.speciesGetAttackPower(self._ptr)
  #\endcond
  ##The power of the fish's attack
  attackPower = property(getAttackPower)

  #\cond
  def getRange(self):
    self.validify()
    return library.speciesGetRange(self._ptr)
  #\endcond
  ##The attack arrange of the fish
  range = property(getRange)

  #\cond
  def getMaxAttacks(self):
    self.validify()
    return library.speciesGetMaxAttacks(self._ptr)
  #\endcond
  ##Maximum number of times this unit can attack per turn
  maxAttacks = property(getMaxAttacks)

  #\cond
  def getSeason(self):
    self.validify()
    return library.speciesGetSeason(self._ptr)
  #\endcond
  ##Determines what season this species will be spawnable in
  season = property(getSeason)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "name: %s\n" % self.getName()
    ret += "index: %s\n" % self.getIndex()
    ret += "cost: %s\n" % self.getCost()
    ret += "maxHealth: %s\n" % self.getMaxHealth()
    ret += "maxMovement: %s\n" % self.getMaxMovement()
    ret += "carryCap: %s\n" % self.getCarryCap()
    ret += "attackPower: %s\n" % self.getAttackPower()
    ret += "range: %s\n" % self.getRange()
    ret += "maxAttacks: %s\n" % self.getMaxAttacks()
    ret += "season: %s\n" % self.getSeason()
    return ret

##This is your primary unit for Reef. It will perform all of your major actions (pickup, attack, move, drop). It stats are based off of its species
class Fish(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.fishGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.fishes:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Command a fish to move to a specified position
  def move(self, x, y):
    self.validify()
    return library.fishMove(self._ptr, x, y)

  ##Command a fish to pick up some trash at a specified position
  def pickUp(self, x, y, weight):
    self.validify()
    return library.fishPickUp(self._ptr, x, y, weight)

  ##Command a fish to drop some trash at a specified position
  def drop(self, x, y, weight):
    self.validify()
    return library.fishDrop(self._ptr, x, y, weight)

  ##Command a fish to attack a target
  def attack(self, target):
    self.validify()
    if not isinstance(target, Fish):
      raise TypeError('target should be of [Fish]')
    target.validify()
    return library.fishAttack(self._ptr, target._ptr)

  #\cond
  def getId(self):
    self.validify()
    return library.fishGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.fishGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.fishGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)

  #\cond
  def getOwner(self):
    self.validify()
    return library.fishGetOwner(self._ptr)
  #\endcond
  ##The owner of this fish
  owner = property(getOwner)

  #\cond
  def getMaxHealth(self):
    self.validify()
    return library.fishGetMaxHealth(self._ptr)
  #\endcond
  ##The maximum health of the fish
  maxHealth = property(getMaxHealth)

  #\cond
  def getCurrentHealth(self):
    self.validify()
    return library.fishGetCurrentHealth(self._ptr)
  #\endcond
  ##The current health of the fish
  currentHealth = property(getCurrentHealth)

  #\cond
  def getMaxMovement(self):
    self.validify()
    return library.fishGetMaxMovement(self._ptr)
  #\endcond
  ##The maximum number of movements in a turn
  maxMovement = property(getMaxMovement)

  #\cond
  def getMovementLeft(self):
    self.validify()
    return library.fishGetMovementLeft(self._ptr)
  #\endcond
  ##The number of movements left
  movementLeft = property(getMovementLeft)

  #\cond
  def getCarryCap(self):
    self.validify()
    return library.fishGetCarryCap(self._ptr)
  #\endcond
  ##The total weight the fish can carry
  carryCap = property(getCarryCap)

  #\cond
  def getCarryingWeight(self):
    self.validify()
    return library.fishGetCarryingWeight(self._ptr)
  #\endcond
  ##The current amount of weight the fish is carrying
  carryingWeight = property(getCarryingWeight)

  #\cond
  def getAttackPower(self):
    self.validify()
    return library.fishGetAttackPower(self._ptr)
  #\endcond
  ##The power of the fish's attack
  attackPower = property(getAttackPower)

  #\cond
  def getMaxAttacks(self):
    self.validify()
    return library.fishGetMaxAttacks(self._ptr)
  #\endcond
  ##The maximum number of attacks this fish has per turn
  maxAttacks = property(getMaxAttacks)

  #\cond
  def getAttacksLeft(self):
    self.validify()
    return library.fishGetAttacksLeft(self._ptr)
  #\endcond
  ##The number of attacks a fish has left
  attacksLeft = property(getAttacksLeft)

  #\cond
  def getRange(self):
    self.validify()
    return library.fishGetRange(self._ptr)
  #\endcond
  ##The attack range of the fish
  range = property(getRange)

  #\cond
  def getSpecies(self):
    self.validify()
    return library.fishGetSpecies(self._ptr)
  #\endcond
  ##The fish species
  species = property(getSpecies)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    ret += "maxHealth: %s\n" % self.getMaxHealth()
    ret += "currentHealth: %s\n" % self.getCurrentHealth()
    ret += "maxMovement: %s\n" % self.getMaxMovement()
    ret += "movementLeft: %s\n" % self.getMovementLeft()
    ret += "carryCap: %s\n" % self.getCarryCap()
    ret += "carryingWeight: %s\n" % self.getCarryingWeight()
    ret += "attackPower: %s\n" % self.getAttackPower()
    ret += "maxAttacks: %s\n" % self.getMaxAttacks()
    ret += "attacksLeft: %s\n" % self.getAttacksLeft()
    ret += "range: %s\n" % self.getRange()
    ret += "species: %s\n" % self.getSpecies()
    return ret

##
class Player(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.playerGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.players:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Allows a player to display messages on the screen
  def talk(self, message):
    self.validify()
    return library.playerTalk(self._ptr, message)

  #\cond
  def getId(self):
    self.validify()
    return library.playerGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getPlayerName(self):
    self.validify()
    return library.playerGetPlayerName(self._ptr)
  #\endcond
  ##Player's Name
  playerName = property(getPlayerName)

  #\cond
  def getTime(self):
    self.validify()
    return library.playerGetTime(self._ptr)
  #\endcond
  ##Time remaining, updated at start of turn
  time = property(getTime)

  #\cond
  def getCurrentReefHealth(self):
    self.validify()
    return library.playerGetCurrentReefHealth(self._ptr)
  #\endcond
  ##The player's current reef health
  currentReefHealth = property(getCurrentReefHealth)

  #\cond
  def getSpawnFood(self):
    self.validify()
    return library.playerGetSpawnFood(self._ptr)
  #\endcond
  ##Food used to spawn new fish
  spawnFood = property(getSpawnFood)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "playerName: %s\n" % self.getPlayerName()
    ret += "time: %s\n" % self.getTime()
    ret += "currentReefHealth: %s\n" % self.getCurrentReefHealth()
    ret += "spawnFood: %s\n" % self.getSpawnFood()
    return ret
