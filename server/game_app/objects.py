class Mappable(object):
  game_state_attributes = ['id', 'x', 'y']
  def __init__(self, game, id, x, y):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, )
  
  def nextTurn(self):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Tile(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'trashAmount', 'owner', 'hasEgg', 'damages']
  def __init__(self, game, id, x, y, trashAmount, owner, hasEgg, damages):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.trashAmount = trashAmount
    self.owner = owner
    self.hasEgg = hasEgg
    self.damages = damages
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.trashAmount, self.owner, self.hasEgg, self.damages, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, trashAmount = self.trashAmount, owner = self.owner, hasEgg = self.hasEgg, damages = self.damages, )
  
  def nextTurn(self):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Species(object):
  game_state_attributes = ['id', 'name', 'index', 'cost', 'maxHealth', 'maxMovement', 'carryCap', 'attackPower', 'range', 'maxAttacks', 'season']
  def __init__(self, game, id, name, index, cost, maxHealth, maxMovement, carryCap, attackPower, range, maxAttacks, season):
    self.game = game
    self.id = id
    self.name = name
    self.index = index
    self.cost = cost
    self.maxHealth = maxHealth
    self.maxMovement = maxMovement
    self.carryCap = carryCap
    self.attackPower = attackPower
    self.range = range
    self.maxAttacks = maxAttacks
    self.season = season
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.name, self.index, self.cost, self.maxHealth, self.maxMovement, self.carryCap, self.attackPower, self.range, self.maxAttacks, self.season, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, name = self.name, index = self.index, cost = self.cost, maxHealth = self.maxHealth, maxMovement = self.maxMovement, carryCap = self.carryCap, attackPower = self.attackPower, range = self.range, maxAttacks = self.maxAttacks, season = self.season, )
  
  def nextTurn(self):
    pass

  def spawn(self, tile):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Fish(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'maxHealth', 'currentHealth', 'maxMovement', 'movementLeft', 'carryCap', 'carryingWeight', 'attackPower', 'isVisible', 'maxAttacks', 'attacksLeft', 'range', 'species']
  def __init__(self, game, id, x, y, owner, maxHealth, currentHealth, maxMovement, movementLeft, carryCap, carryingWeight, attackPower, isVisible, maxAttacks, attacksLeft, range, species):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.maxHealth = maxHealth
    self.currentHealth = currentHealth
    self.maxMovement = maxMovement
    self.movementLeft = movementLeft
    self.carryCap = carryCap
    self.carryingWeight = carryingWeight
    self.attackPower = attackPower
    self.isVisible = isVisible
    self.maxAttacks = maxAttacks
    self.attacksLeft = attacksLeft
    self.range = range
    self.species = species
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.maxHealth, self.currentHealth, self.maxMovement, self.movementLeft, self.carryCap, self.carryingWeight, self.attackPower, self.isVisible, self.maxAttacks, self.attacksLeft, self.range, self.species, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, maxHealth = self.maxHealth, currentHealth = self.currentHealth, maxMovement = self.maxMovement, movementLeft = self.movementLeft, carryCap = self.carryCap, carryingWeight = self.carryingWeight, attackPower = self.attackPower, isVisible = self.isVisible, maxAttacks = self.maxAttacks, attacksLeft = self.attacksLeft, range = self.range, species = self.species, )
  
  def nextTurn(self):
    pass

  def move(self, x, y):
    pass

  def pickUp(self, tile, weight):
    pass

  def drop(self, tile, weight):
    pass

  def attack(self, target):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Player(object):
  game_state_attributes = ['id', 'playerName', 'time', 'currentReefHealth', 'spawnFood']
  def __init__(self, game, id, playerName, time, currentReefHealth, spawnFood):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.currentReefHealth = currentReefHealth
    self.spawnFood = spawnFood
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.playerName, self.time, self.currentReefHealth, self.spawnFood, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, currentReefHealth = self.currentReefHealth, spawnFood = self.spawnFood, )
  
  def nextTurn(self):
    pass

  def talk(self, message):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)


# The following are animations and do not need to have any logic added
class SpawnAnimation:
  def __init__(self, playerID, x, y, species):
    self.playerID = playerID
    self.x = x
    self.y = y
    self.species = species

  def toList(self):
    return ["spawn", self.playerID, self.x, self.y, self.species, ]

  def toJson(self):
    return dict(type = "spawn", playerID = self.playerID, x = self.x, y = self.y, species = self.species)

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
  def __init__(self, actingID, targetID, x, y, amount):
    self.actingID = actingID
    self.targetID = targetID
    self.x = x
    self.y = y
    self.amount = amount

  def toList(self):
    return ["pickUp", self.actingID, self.targetID, self.x, self.y, self.amount, ]

  def toJson(self):
    return dict(type = "pickUp", actingID = self.actingID, targetID = self.targetID, x = self.x, y = self.y, amount = self.amount)

class DeathAnimation:
  def __init__(self, actingID):
    self.actingID = actingID

  def toList(self):
    return ["death", self.actingID, ]

  def toJson(self):
    return dict(type = "death", actingID = self.actingID)

class DropAnimation:
  def __init__(self, actingID, targetID, x, y, amount):
    self.actingID = actingID
    self.targetID = targetID
    self.x = x
    self.y = y
    self.amount = amount

  def toList(self):
    return ["drop", self.actingID, self.targetID, self.x, self.y, self.amount, ]

  def toJson(self):
    return dict(type = "drop", actingID = self.actingID, targetID = self.targetID, x = self.x, y = self.y, amount = self.amount)

class AttackAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["attack", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "attack", actingID = self.actingID, targetID = self.targetID)

class StealthAnimation:
  def __init__(self, actingID):
    self.actingID = actingID

  def toList(self):
    return ["stealth", self.actingID, ]

  def toJson(self):
    return dict(type = "stealth", actingID = self.actingID)

class PlayerTalkAnimation:
  def __init__(self, actingID, message):
    self.actingID = actingID
    self.message = message

  def toList(self):
    return ["playerTalk", self.actingID, self.message, ]

  def toJson(self):
    return dict(type = "playerTalk", actingID = self.actingID, message = self.message)

class DeStealthAnimation:
  def __init__(self, actingID):
    self.actingID = actingID

  def toList(self):
    return ["deStealth", self.actingID, ]

  def toJson(self):
    return dict(type = "deStealth", actingID = self.actingID)

