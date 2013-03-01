import networking.config.config

#Initializes cfgSpecies
cfgSpecies = networking.config.config.readConfig("config/species.cfg")
for key in cfgSpecies.keys():
  cfgSpecies[key]['type'] = key


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
  def __init__(self, game, id, species, cost, maxHealth, maxMovement, carryCap, attackPower, range, maxAttacks, turnsTillAvailalbe, turnsTillUnavailable):
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
    self.turnsTillAvailalbe = turnsTillAvailalbe
    self.turnsTillUnavailable = turnsTillUnavailable

  def toList(self):
    return [self.id, self.species, self.cost, self.maxHealth, self.maxMovement, self.carryCap, self.attackPower, self.range, self.maxAttacks, self.turnsTillAvailalbe, self.turnsTillUnavailable, ]

  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, species = self.species, cost = self.cost, maxHealth = self.maxHealth, maxMovement = self.maxMovement, carryCap = self.carryCap, attackPower = self.attackPower, range = self.range, maxAttacks = self.maxAttacks, turnsTillAvailalbe = self.turnsTillAvailalbe, turnsTillUnavailable = self.turnsTillUnavailable, )

  def nextTurn(self):
    pass

  def spawn(self, x, y):
    pass



class Tile(Mappable):
  def __init__(self, game, id, x, y, trashAmount, owner, isCove):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.trashAmount = trashAmount
    self.owner = owner
    self.isCove = isCove

  def toList(self):
    return [self.id, self.x, self.y, self.trashAmount, self.owner, self.isCove, ]

  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, trashAmount = self.trashAmount, owner = self.owner, isCove = self.isCove, )

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

  def nextTurn(self):
    pass

  def move(self, x, y):
    if self.owner != self.game.playerID:
        return "You can only control your own fish"
    elif (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
        return "Cannot move off of the map"
    elif self.movemmentLeft <= 0:
        return "You have no moves left"
    elif abs(self.x-x) + abs(self.y-y) != 1:
        return "Can only move to adjacent locations"
    elif self.game.grid[x][y].trashAmount > 0:
        return "Cannot move onto a tile containing trash"
    elif isinstance(self.game.getObject(x,y), Fish):
        return "Another fish is occupying that tile"
        #stealth unit?
    elif self.game.grid[x][y].isCove:
        return "Cannot move into enemy's cove"
    #how to test for moving above a certain y value?

    #updating map
    self.game.grid[self.x][self.y].remove(self)
    self.game.grid[x][y].append(self)
    self.x = x
    self.y = y
    self.movementLeft -= 1
    pass

  def pickUp(self, x, y, weight):
    if self.owner != self.game.playerID:
      return "You can only control your own fish."
    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return "Cannot pick up trash off the map."
    elif abs(self.x-x) + abs(self.y-y) !=1:
      return "Can only pick up adjacent trash."
    elif (self.carryingWeight + weight) > self.carryCap:
      return "Cannot carry more weight than the fish's carry cap."
    elif weight == 0:
      return "Cannot pick up a weight of 0."
    elif getTile(x,y).trashAmount < weight:
      return "You can't pick up more trash then there is trash present."
    
    #don't need to bother checking for fish because a space with a 
    #fish shouldn't have any trash, right?
    
    #unstealth fish... because that's what drop did
    if not self.Visible:
       self.Visible = True;
    
    #TODO: Check for the fish that's immune to trash damage (?)
    #TODO: Determine damage taken
    #take damage
    self.currentHealth -= self.trashDamage*weight
    #check if dead
    if self.currentHealth < 0:
      #remove object
      self.game.removeObject(self.game.getObject(x,y))
      self.game.grid[x][y].remove(self.game.getObject(x,y))
      return "Your fish died trying to pick up the trash."
    #reduce weight of tile
    getTile(x,y).trashAmount -= weight
    #add weight to fish
    self.carryingWeight += weight
    pass

  def drop(self, x, y, weight):
    if self.owner != self.game.playerID:
      return "You can only control your own fish"
    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return "Cannot drop off the map"
    elif abs(self.x-x) + abs(self.y-y) != 1:
      return "Can only drop onto adjacent locations"
    elif weight > self.carryingWeight:
      return "You cannot drop more than you're carrying"
    elif self.game.getFish(x,y) != []:
      return "Cannot drop onto a fish"

    if not self.isVisible:
      self.isVisible = True #unstealth while dropping
    
    #TODO: what happens when dropping onto a stealth fish?
    
    self.game.getTile(x,y).trashAmount += weight
    self.carryingWeight -= weight
    return True 

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

  def toList(self):
    return [self.id, self.playerName, self.time, self.currentReefHealth, self.spawnFood, ]

  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, currentReefHealth = self.currentReefHealth, spawnFood = self.spawnFood, )

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

