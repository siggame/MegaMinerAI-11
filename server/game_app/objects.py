import networking.config.config

#Initializes cfgSpecies
cfgSpecies = networking.config.config.readConfig("config/species.cfg")

for key in cfgSpecies.keys():
  cfgSpecies[key]['type'] = key

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
  game_state_attributes = ['id', 'x', 'y', 'trashAmount', 'owner', 'hasEgg']
  def __init__(self, game, id, x, y, trashAmount, owner, hasEgg):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.trashAmount = trashAmount
    self.owner = owner
    self.hasEgg = hasEgg
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.trashAmount, self.owner, self.hasEgg, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, trashAmount = self.trashAmount, owner = self.owner, hasEgg = self.hasEgg, )
  
  def nextTurn(self):
    pass

  def spawn(self, x, y):
    return True
    player = self.game.objects.players[self.game.playerID]
    if x < 0 or x >= self.game.mapWidth:
      return "You cannot spawn outside the breeding grounds."
    elif y < 0:
      return "You cannot spawn in the sky."
    elif y >= self.game.mapHeight:
      return "You cannot spawn in the ground."
    elif self.game.getTile(x, y).owner is not self.game.playerID:
      return "You can only spawn on a cove you own."
    elif player.spawnFood < self.cost:
      return "You do not have enough food to spawn this fish."
    elif self.game.currentSeason is not self.season:
      return "You can only spawn this fish in the season %s"%(self.season)
    else:
      player.spawning.append([self.type, x, y])
      player.spawnFood -= self.cost

    return True

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Species(object):
  game_state_attributes = ['id', 'name', 'cost', 'maxHealth', 'maxMovement', 'carryCap', 'attackPower', 'range', 'maxAttacks', 'season']
  def __init__(self, game, id, name, cost, maxHealth, maxMovement, carryCap, attackPower, range, maxAttacks, season):
    self.game = game
    self.id = id
    self.name = name
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
    return [self.id, self.name, self.cost, self.maxHealth, self.maxMovement, self.carryCap, self.attackPower, self.range, self.maxAttacks, self.season, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, name = self.name, cost = self.cost, maxHealth = self.maxHealth, maxMovement = self.maxMovement, carryCap = self.carryCap, attackPower = self.attackPower, range = self.range, maxAttacks = self.maxAttacks, season = self.season, )
  
  def nextTurn(self):
    pass

  def spawn(self, x, y):
    player = self.game.objects.players[self.game.playerID]
    if not self.game.getTile(x,y).isCove:
      return "You can only spawn fish inside of a cove tile"
    elif player.spawnFood<self.cost:
      return "You don'thave enough food to spawn this fish in"
    elif not (0<x<=self.game.mapWidth or 0<y<self.game.mapHeight):
      return "You can't spawn your fish out of the edges of the map"
    elif self.game.currentSeason != self.season:
      return "This fish can't spawn in this season"
    elif self.game.getTile(x,y).hasEgg:
      return "there is already a fish to be spawned here"
    else:
      player.spawnFood-=self.cost
      player.spawning.append(self,x,y)
    return True

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

  ### TODO: move one space at a time, can't move over trash or other fish, need to figure out what to do about stealth things 

  def move(self, x, y):
    if self.owner != self.game.playerID: #check that you own the fish
      return "You cannot move the other player's fish." 
    elif self.movementLeft <= 0: #check that there are moves left
      return "Your fish has no moves left."
    elif not (0<=x<self.game.mapWidth) or not (0<=y<self.game.mapHeight):
      return "Your fish cannot move off the map."
    elif abs(self.x-x) > 1 or abs(self.y - y) > 1 or (abs(self.x-x) == 1 and abs(self.y - y) == 1):
      return "You can only move to adjacent locations."
    T = self.game.getTile(x, y) #The tile the player wants to walk onto
    if T.trashAmount > 0:
      return "You can't move on top of trash"
    elif len(self.game.getFish (x, y)) > 0: #If there is a fish on the tile
      for i in range(1, len(self.game.getFish(x,y))):
        if not self.game.getFish(x, y)[i].isStealthed:
          return "You can't move onto a fish." 
        else:
          print "Fringe case: moving onto a stealthed fish."
          pass
    elif self.game.getTile(x,y).isCove == True and self.game.getTile(x,y).owner != self.owner:
      return "Can't go into an opponent's cove."
    #Working under the assumption that ground units can move anywhere
    self.game.grid[self.x][self.y].remove(self)
    self.game.grid[x][y].append(self)
            
    self.movementLeft -= 1
    self.x = x
    self.y = y
    return "Successful movement. Congrats."

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
    elif self.game.getTile(x,y).trashAmount < weight:
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
    self.game.getTile(x,y).trashAmount -= weight
    #add weight to fish
    self.carryingWeight += weight
    return True

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

#TODO: Update to work with being passed a Fish to attack
  def attack(self, target):
  
    x = target.x
    y = target.y
  
    #I feel like stealth units are going to mess up this function
    if self.owner != self.game.playerID:
      return "You can only control your own fish."
    elif abs(self.x-x) + abs(self.y-y) > self.range:
      return "You can't attack further than your fish's range."
    elif self.attacksLeft == 0:
      return "This fish has no attacks left."
    elif target == []:
      return "You can't attack nothing!"
    elif target.isVisible == False and target.owner != self.game.playerID:
      return "You aren't even supposed to see invisible fish, let alone attack them."
    elif target.owner != self.game.playerID and self.attackPower < 0:
      return "You can't heal the opponent's fish."
    elif target.owner == self.game.playerID and self.attackPower > 0:
      return "You can't attack your own fish."
    elif self.isVisible == False and self.attackPower < target.currentHealth:
      return "A stealthed unit can't attack a fish above it if it can't kill it."
    
    #hurt the other fish
    target.currentHealth -= self.attackPower
    #make the other fish visible; in case an invisible fish is being healed
    target.isVisible = True
    #make the attacking fish visible
    self.isVisible = True
    
    #check if dead
    if target.currentHealth <= 0:
      #drop trash on tile
      self.game.getTile(x,y).trashAmount += target.carryingWeight
      if x == self.x and y == self.y:
        #stealth fish on same tile must pick up garbage
        #TODO: Currently the stealthed fish dies if it kills a fish with too much weight.
        #      Is this desired?
        if target.carryingWeight + self.carryingWeight <= self.carryingCap:
           #can carry all that weight
           self.pickUp(x,y,target.carryingWeight)
        else:
           #can't carry that weight, just die.
           self.game.grid[x][y].remove(self)
           self.game.remove(self)
      self.game.grid[x][y].remove(target)
      self.game.remove(target)
      
    #don't allow infinite health bugs to create super fish
    elif target.currentHealth > target.maxHealth:
      target.currentHealth = target.maxHealth
    return True

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
    self.spawning = []

  def toList(self):
    return [self.id, self.playerName, self.time, self.currentReefHealth, self.spawnFood, ]

  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, currentReefHealth = self.currentReefHealth, spawnFood = self.spawnFood, )

  def nextTurn(self):
    #TODO: Give food back to player
    #Fish spawn in at beginning of turn
    if self.game.playerID is self.id:
      self.spawnFood +=10
      
      for spawn in self.spawning:
        print spawn
        fishStats = [cfgSpecies[spawn[0]][stat] for stat in self.game.statList]
        self.game.addObject(Fish, [[spawn[1], spawn[2], self.game.playerID]] + fishStats)

    self.spawning = []
    return True

  def talk(self, message):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)


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

