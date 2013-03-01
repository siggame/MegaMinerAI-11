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



class FishSpecies:
  def __init__(self, game, id, species, cost, maxHealth, maxMovement, carryCap, attackPower, range, maxAttacks, canStealth, turnsTillAvailalbe, turnsTillUnavailable):
    self.game = game
    self.id = id
    self.species = species
    self.cost = cost
    self.maxHealth = maxHealth
    self.maxMovement = maxMovement
    self.carryCap = carryCap
    self.attackPower = attackPower
    self.range = range
    self.maxAttacks = maxAttacks
    self.canStealth = canStealth
    self.turnsTillAvailalbe = turnsTillAvailalbe
    self.turnsTillUnavailable = turnsTillUnavailable

  def toList(self):
    return [self.id, self.species, self.cost, self.maxHealth, self.maxMovement, self.carryCap, self.attackPower, self.range, self.maxAttacks, self.canStealth, self.turnsTillAvailalbe, self.turnsTillUnavailable, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, species = self.species, cost = self.cost, maxHealth = self.maxHealth, maxMovement = self.maxMovement, carryCap = self.carryCap, attackPower = self.attackPower, range = self.range, maxAttacks = self.maxAttacks, canStealth = self.canStealth, turnsTillAvailalbe = self.turnsTillAvailalbe, turnsTillUnavailable = self.turnsTillUnavailable, )
  
  def nextTurn(self):
    pass

  
  ###TODO: Spawn logic. Parse through species.conf file and give each species the correct stats. turnsTill logic will need to be implmented. 
  def spawn(self, x, y):
    pass



class Tile(Mappable):
  def __init__(self, game, id, x, y, trashAmount):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.trashAmount = trashAmount

  def toList(self):
    return [self.id, self.x, self.y, self.trashAmount, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, trashAmount = self.trashAmount, )
  
  def nextTurn(self):
    pass



class Fish(Mappable):
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

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.maxHealth, self.currentHealth, self.maxMovement, self.movementLeft, self.carryCap, self.carryingWeight, self.attackPower, self.isVisible, self.maxAttacks, self.attacksLeft, self.range, self.species, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, maxHealth = self.maxHealth, currentHealth = self.currentHealth, maxMovement = self.maxMovement, movementLeft = self.movementLeft, carryCap = self.carryCap, carryingWeight = self.carryingWeight, attackPower = self.attackPower, isVisible = self.isVisible, maxAttacks = self.maxAttacks, attacksLeft = self.attacksLeft, range = self.range, species = self.species, )
  
  ### TODO: Reset movement, attack, possible stealth, damage if carrying trash, possibly more
  def nextTurn(self):
    pass
  ### TODO: move one space at a time, can't move over trash or other fish, need to figure out what to do about stealth things 

  def move(self, x, y):
    if self.owner != self.game.playerID: #check that you own the fish
      return "You cannot move the other player's fish." 
    elif self.movementLeft <= 0: #check that there are moves left
      return "Your fish has no moves left."
    elif not (0<=x<self.game.mapWidth) or not (0<=y<self.game.mapHeight):
      return "Your fish cannot move off the map."
    T = self.game.getTile (x, y) [0] #The tile the player wants to walk onto
    elif T.trashAmount > 0:
      return "You can't move on top of trash"
    elif len(self.game.getFish (x, y)) > 0: #If there is a fish on the tile
      for i in range(1, len(self.game.getFish(x,y)):
        if self.game.getFish(x,y)[i].isStealthed == false:
          return "You can't move onto a fish." 
        else
          print "Fringe case: moving onto a stealthed fish."
          pass
    #Working under the assumption that ground units can move anywhere
    movementLeft -= 1
    self.x = x
    self.y = y
    return "Succesful movement. Congrats."
  
  ### TODO: pick up trash from a tile 1 space away, can't exceec carrying cap, does damage on pickup,
  ### based off how trash was picked up, damage can't exceed health, can't pick up 0 trash
  def pickUp(self, x, y, weight):
    pass
 
  def drop(self, x, y, weight):
    pass

  def attack(self, x, y):
    pass



class Player:
  def __init__(self, game, id, playerName, time, currentReefHealth, spawnFood):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.currentReefHealth = currentReefHealth
    self.spawnFood = spawnFood
    self.spawning = []
    
  def toList(self):
    return [self.id, self.playerName, self.time, self.currentReefHealth, self.spawnFood, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, currentReefHealth = self.currentReefHealth, spawnFood = self.spawnFood, )
  
  
  ### TODO: Have trash to damage based off location, give food, spawn new fish
  def nextTurn(self):
    pass

  def talk(self, message):
    pass




# The following are animations and do not need to have any logic added
class SpawnAnimation:
  def __init__(self, x, y, species):
    self.x = x
    self.y = y
    self.species = species

  def toList(self):
    return ["spawn", self.x, self.y, self.species, ]

  def toJson(self):
    return dict(type = "spawn", x = self.x, y = self.y, species = self.species)

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
  def __init__(self, x, y, actingID, amount):
    self.x = x
    self.y = y
    self.actingID = actingID
    self.amount = amount

  def toList(self):
    return ["pickUp", self.x, self.y, self.actingID, self.amount, ]

  def toJson(self):
    return dict(type = "pickUp", x = self.x, y = self.y, actingID = self.actingID, amount = self.amount)

class DeathAnimation:
  def __init__(self, actingID):
    self.actingID = actingID

  def toList(self):
    return ["death", self.actingID, ]

  def toJson(self):
    return dict(type = "death", actingID = self.actingID)

class DropAnimation:
  def __init__(self, x, y, actingID, amount):
    self.x = x
    self.y = y
    self.actingID = actingID
    self.amount = amount

  def toList(self):
    return ["drop", self.x, self.y, self.actingID, self.amount, ]

  def toJson(self):
    return dict(type = "drop", x = self.x, y = self.y, actingID = self.actingID, amount = self.amount)

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

