class Mappable:
  def __init__(self, game, id, x, y):
    self.game = game
    self.id = id
    self.x = x
    self.y = y

  def toList(self):
    return [self.id, self.x, self.y, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, )
  
  def nextTurn(self):
    pass


#fdlksafld
class Trash(Mappable):
  def __init__(self, game, id, x, y, weight):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.weight = weight

  def toList(self):
    return [self.id, self.x, self.y, self.weight, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, weight = self.weight, )
  
  def nextTurn(self):
    pass



class Fish(Mappable):
  def __init__(self, game, id, x, y, owner, species, maxHealth, curHealth, maxMoves, movementLeft, carryCap, carryWeight, attackPower, isVisible, attacksLeft):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.species = species
    self.maxHealth = maxHealth
    self.curHealth = curHealth
    self.maxMoves = maxMoves
    self.movementLeft = movementLeft
    self.carryCap = carryCap
    self.carryWeight = carryWeight
    self.attackPower = attackPower
    self.isVisible = isVisible
    self.attacksLeft = attacksLeft

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.species, self.maxHealth, self.curHealth, self.maxMoves, self.movementLeft, self.carryCap, self.carryWeight, self.attackPower, self.isVisible, self.attacksLeft, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, species = self.species, maxHealth = self.maxHealth, curHealth = self.curHealth, maxMoves = self.maxMoves, movementLeft = self.movementLeft, carryCap = self.carryCap, carryWeight = self.carryWeight, attackPower = self.attackPower, isVisible = self.isVisible, attacksLeft = self.attacksLeft, )
  
  def nextTurn(self):
    pass

  def move(self, x, y):
    pass

  def pickUp(self, x, y, weight):
    pass

  def drop(self, x, y, weight):
    pass

  def attack(self, x, y):
    pass



class Player:
  def __init__(self, game, id, playerName, time, curReefHealth, sandDollars):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.curReefHealth = curReefHealth
    self.sandDollars = sandDollars

  def toList(self):
    return [self.id, self.playerName, self.time, self.curReefHealth, self.sandDollars, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, curReefHealth = self.curReefHealth, sandDollars = self.sandDollars, )
  
  def nextTurn(self):
    pass

  def talk(self, message):
    pass




# The following are animations and do not need to have any logic added
class SpawnAnimation:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def toList(self):
    return ["spawn", self.x, self.y, ]

  def toJson(self):
    return dict(type = "spawn", x = self.x, y = self.y)

class MoveAnimation:
  def __init__(self, actingID, fromX, fromY, toX, toY):
    self.actingID = actingID
    self.fromX = fromX
    self.fromY = fromY
    self.toX = toX
    self.toY = toY

  def toList(self):
    return ["move", self.actingID, self.fromX, self.fromY, self.toX, self.toY, ]

  def toJson(self):
    return dict(type = "move", actingID = self.actingID, fromX = self.fromX, fromY = self.fromY, toX = self.toX, toY = self.toY)

class PickUpAnimation:
  def __init__(self, x, y, actingID):
    self.x = x
    self.y = y
    self.actingID = actingID

  def toList(self):
    return ["pickUp", self.x, self.y, self.actingID, ]

  def toJson(self):
    return dict(type = "pickUp", x = self.x, y = self.y, actingID = self.actingID)

class DeathAnimation:
  def __init__(self, actingID):
    self.actingID = actingID

  def toList(self):
    return ["death", self.actingID, ]

  def toJson(self):
    return dict(type = "death", actingID = self.actingID)

class DropAnimation:
  def __init__(self, x, y, actingID):
    self.x = x
    self.y = y
    self.actingID = actingID

  def toList(self):
    return ["drop", self.x, self.y, self.actingID, ]

  def toJson(self):
    return dict(type = "drop", x = self.x, y = self.y, actingID = self.actingID)

class AttackAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["attack", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "attack", actingID = self.actingID, targetID = self.targetID)

class PlayerTalkAnimation:
  def __init__(self, actingID, message):
    self.actingID = actingID
    self.message = message

  def toList(self):
    return ["playerTalk", self.actingID, self.message, ]

  def toJson(self):
    return dict(type = "playerTalk", actingID = self.actingID, message = self.message)

