import networking.config.config
import math

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
    if self.game.playerID == self.owner:
      if self.hasEgg:
        species = self.species
        print 'Spawning ' + species.name
        stats = [self.x, self.y, self.owner,
            species.maxHealth, species.maxHealth,
            species.maxMovement, species.maxMovement,
            species.carryCap, 0, species.attackPower, True,
            species.maxAttacks, species.maxAttacks,
            species.range, species.name]
        newFish = self.game.addObject(Fish, stats)
        self.game.addAnimation(SpawnAnimation(newFish.x,newFish.y,newFish.species))
        self.game.grid[newFish.x][newFish.y].append(newFish)
        self.hasEgg = False
     
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
    if player.spawnFood<self.cost:
      return "You don'thave enough food to spawn this fish in"
    if not (0<=x<self.game.mapWidth or 0<=y<self.game.mapHeight):
      return "You can't spawn your fish out of the edges of the map"
    elif self.game.currentSeason != self.season:
      return "This fish can't spawn in this season"
    tile = self.game.getTile(x,y)
    if tile.owner != self.game.playerID:
      return "You can only spawn fish inside of your cove tiles"
    elif tile.hasEgg:
      return "there is already a fish to be spawned here"
    else:
      player.spawnFood-=self.cost
      tile.hasEgg = True
      tile.species = self
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

  def heal(self,fish):
    fish.currentHealth+=fish.maxHealth*self.game.healPercent
    if fish.currentHealth>fish.maxHealth:
      fish.currentHealth = fish.maxHealth

  def distance(self,source,x,y):
    return math.sqrt((source.x-x)**2 + (source.y-y)**2) 
  
  def addTrash(self,x,y,weight):
    if (x,y) not in self.game.trashDict:      
      self.game.trashDict[(x,y)] = weight
    else:
      self.game.trashDict[(x,y)] += weight 
  
  def removeTrash(self,x,y,weight):
    self.game.trashDict[(x,y)]-=weight
    if self.game.trashDict[(x,y)] == 0:
      del self.game.trashDict[(x,y)]

  def nextTurn(self):
    #TODO set fish stats to 0 if stunned by an eel
    if self.owner == self.game.playerID:
      if self.game.getTile(self.x,self.y).owner == self.owner:
        self.heal(self)
      self.movementLeft = self.maxMovement
      self.attacksleft = self.maxAttacks
      if self.species == "Cuttlefish":
        self.isVisible = False
      if self.species != "Tomcod":
        self.currentHealth -= self.carryingWeight * self.game.trashDamage #May need to do this at the end of turns in match.py, to ensure a player doesn't think they have a dead fish
        if self.currentHealth <0:
          self.game.grid[self.x][self.y].remove(self)         
          self.game.addAnimation(DeathAnimation(self.id))
          self.removeTrash(self.x,self.y,self.carryingWeight)
          self.game.removeObject(self)
          print "dude died from carrying so much trash"
    return True

  def move(self, x, y):
    if self.owner != self.game.playerID: #check that you own the fish
      return "You cannot move the other player's fish."
    elif self.movementLeft <= 0: #check that there are moves left
      return "Your fish has no moves left."
    elif not (0<=x<self.game.mapWidth) or not (0<=y<self.game.mapHeight):
      return "Your fish cannot move off the map."
    elif self.distance(self,x,y)!=1:
      return "You can only move to adjacent locations."
    T = self.game.getTile(x, y) #The tile the player wants to walk onto
    if T.trashAmount > 0:
      return "You can't move on top of trash"
    elif T.owner != self.owner:
      return "Can't go into an opponent's cove."
    elif T.hasEgg:
      return "A fish is about to be spawned here"
    Fishes = self.game.getFish(x,y)
   # print Fishes
    if len(Fishes)>0: #If there is a fish on the tile
      for fish in Fishes:
        if fish.isVisible:
          return "You can't move onto a fish."
        else:
          return "Fringe case: moving onto a stealthed fish."    
    self.game.grid[self.x][self.y].remove(self)
    self.game.grid[x][y].append(self)
    self.game.addAnimation(MoveAnimation(self.id,self.x,self.y,x,y))        
    self.movementLeft -= 1
    self.x = x
    self.y = y
    print "moving a dude"
    return True

  def pickUp(self, x, y, weight):
    if self.owner != self.game.playerID:
      return "You can only control your own fish."
    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return "Cannot pick up trash off the map."
    elif self.distance(self,x,y) !=1:
      return "Can only pick up adjacent trash."
    elif (self.carryingWeight + weight) > self.carryCap:
      return "Cannot carry more weight than the fish's carry cap."
    elif weight == 0:
      return "Cannot pick up a weight of 0."
    elif self.game.getTile(x,y).trashAmount < weight:
      return "You can't pick up more trash then there is trash present."
    elif self.currentHealth < weight:
      return "Can't pick that up, would kill your fish"
    
    #don't need to bother checking for fish because a space with a
    #fish shouldn't have any trash, right?
    
    #unstealth fish... because that's what drop did
    if not self.isVisible:
      self.isVisible = True
    
    #take damage if not immune to it
    if self.species != "TomCod":
      self.currentHealth -= self.game.trashDamage * weight
        
    #reduce weight of tile
    self.game.getTile(x,y).trashAmount -= weight
    self.removeTrash(x,y,weight)
    #add weight to fish
    self.carryingWeight += weight
    self.game.addAnimation(PickUpAnimation(x,y,self.id,weight))
    print "dude picked up some trash"
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
    Fishes = self.game.getFish(x,y)
    if len(Fishes)>0: #If there is a fish on the tile
      for fish in Fishes:
        if fish.isVisible:
          return "Cannot drop onto a fish"
        else:
          return "Fringe case: dropping onto a stealthed fish."    

    if not self.isVisible:
      self.isVisible = True #unstealth while dropping    
    
    self.game.getTile(x,y).trashAmount += weight
    self.carryingWeight -= weight
    self.game.addAnimation(self.x,self.y,self.id,weight)
    self.addTrash(x,y,weight)
    return True

  def attack(self, target):  
    x = target.x
    y = target.y
  
    #I feel like stealth units are going to mess up this function
    if self.owner != self.game.playerID:
      return "You can only control your own fish."
    elif self.distance(self,x,y) > self.range:
      return "You can't attack further than your fish's range."
    elif self.attacksLeft == 0:
      return "This fish has no attacks left."
    elif not isinstance(target,Fish):
      return "You  can only attack Fish"
    elif target.isVisible == False and target.owner != self.game.playerID:
      return "You aren't even supposed to see invisible fish, let alone attack them."
    elif target.owner != self.owner and self.attackPower < 0:
      return "You can't heal the opponent's fish."
    elif target.owner == self.owner and self.attackPower > 0:
      return "You can't attack your own fish."
    elif self.x == x and self.y == y:
      return "A stealthed unit can't attack a fish above it."

    print "attacking a dude  with another dude"
    
    #TODO Eel stun case
    
    if self.species == "cleanerShrimp":
      self.heal(target)
      target.isVisible = True
   
    else:   
      #hurt the other fish
      target.currentHealth -= self.attackPower
      #make the attacking fish visible
      self.isVisible = True  
    
    #check if target is dead
    if target.currentHealth <= 0:
      #drop trash on tile
      self.game.grid[x][y].remove(target)
      if target.carryingWeight>0:
        self.addTrash(target.x,target.y,target.carryingWeight)
      self.game.removeObject(target)
     
    self.game.addAnimation(AttackAnimation(self.id,target.id))
    self.attacksLeft-=1  
    #check for sea urchin counter attacks
    if target.species == "SeaUrchin" and target.owner != self.owner:
      self.currentHealth -= target.attackPower
      #check if the counter attack killed the fish
      if self.currentHealth <= 0:
        if self.carryingWeight>0:
          self.addTrash(self.x,self.y,self.carryingWeight)
        self.game.grid[x][y].remove(self)
        self.game.removeObject(self)
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
      
    return True
    
  def talk(self, message):
    self.game.addAnimations(PlayerTalkAnimation(self.id,message))
    
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

