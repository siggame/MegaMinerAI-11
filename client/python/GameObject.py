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

##This is a Trash object
class Trash(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.trashGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.trashs:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  #\cond
  def getId(self):
    self.validify()
    return library.trashGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.trashGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.trashGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)

  #\cond
  def getWeight(self):
    self.validify()
    return library.trashGetWeight(self._ptr)
  #\endcond
  ##The weight of the trash
  weight = property(getWeight)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "weight: %s\n" % self.getWeight()
    return ret

##
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
    for i in BaseAI.fishs:
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

  ##Command a fish to attack another fish at a specified position
  def attack(self, x, y):
    self.validify()
    return library.fishAttack(self._ptr, x, y)

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
  def getSpecies(self):
    self.validify()
    return library.fishGetSpecies(self._ptr)
  #\endcond
  ##The type/species of the fish
  species = property(getSpecies)

  #\cond
  def getMaxHealth(self):
    self.validify()
    return library.fishGetMaxHealth(self._ptr)
  #\endcond
  ##The maximum health of the fish
  maxHealth = property(getMaxHealth)

  #\cond
  def getCurHealth(self):
    self.validify()
    return library.fishGetCurHealth(self._ptr)
  #\endcond
  ##The current health of the fish
  curHealth = property(getCurHealth)

  #\cond
  def getMaxMoves(self):
    self.validify()
    return library.fishGetMaxMoves(self._ptr)
  #\endcond
  ##The maximum number of movements in a turn
  maxMoves = property(getMaxMoves)

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
  def getCarryWeight(self):
    self.validify()
    return library.fishGetCarryWeight(self._ptr)
  #\endcond
  ##The current amount of weight the fish is carrying
  carryWeight = property(getCarryWeight)

  #\cond
  def getAttackPower(self):
    self.validify()
    return library.fishGetAttackPower(self._ptr)
  #\endcond
  ##The power of the fish's attack
  attackPower = property(getAttackPower)

  #\cond
  def getIsVisible(self):
    self.validify()
    return library.fishGetIsVisible(self._ptr)
  #\endcond
  ##The visibleness of the fish
  isVisible = property(getIsVisible)

  #\cond
  def getAttacksLeft(self):
    self.validify()
    return library.fishGetAttacksLeft(self._ptr)
  #\endcond
  ##The number of attacks a fish has left
  attacksLeft = property(getAttacksLeft)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    ret += "species: %s\n" % self.getSpecies()
    ret += "maxHealth: %s\n" % self.getMaxHealth()
    ret += "curHealth: %s\n" % self.getCurHealth()
    ret += "maxMoves: %s\n" % self.getMaxMoves()
    ret += "movementLeft: %s\n" % self.getMovementLeft()
    ret += "carryCap: %s\n" % self.getCarryCap()
    ret += "carryWeight: %s\n" % self.getCarryWeight()
    ret += "attackPower: %s\n" % self.getAttackPower()
    ret += "isVisible: %s\n" % self.getIsVisible()
    ret += "attacksLeft: %s\n" % self.getAttacksLeft()
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
  def getCurReefHealth(self):
    self.validify()
    return library.playerGetCurReefHealth(self._ptr)
  #\endcond
  ##The player's current reef health
  curReefHealth = property(getCurReefHealth)

  #\cond
  def getSandDollars(self):
    self.validify()
    return library.playerGetSandDollars(self._ptr)
  #\endcond
  ##Currency for fish
  sandDollars = property(getSandDollars)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "playerName: %s\n" % self.getPlayerName()
    ret += "time: %s\n" % self.getTime()
    ret += "curReefHealth: %s\n" % self.getCurReefHealth()
    ret += "sandDollars: %s\n" % self.getSandDollars()
    return ret
