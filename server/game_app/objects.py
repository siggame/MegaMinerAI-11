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
            species.range, species.index]
        newFish = self.game.addObject(Fish, stats)
        self.game.addAnimation(SpawnAnimation(self.owner,newFish.x,newFish.y,newFish.species))
        self.game.grid[newFish.x][newFish.y].append(newFish)
        self.hasEgg = False
     
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

  def spawn(self, x, y):
    player = self.game.objects.players[self.game.playerID]
    if player.spawnFood < self.cost:
      return "You don't  have enough food to spawn this fish in"
    if not (0 <= x < self.game.mapWidth or 0 <= y < self.game.mapHeight):
      return "You can't spawn your fish out of the edges of the map"
    elif self.game.currentSeason != self.season:
      return "This fish can't spawn in this season"
    elif len(self.game.getFish(x, y)) != 0:
      return "There is already a fish here"

    tile = self.game.getTile(x,y)
    if tile.owner != self.game.playerID:
      return "You can only spawn fish inside of your cove tiles"
    elif tile.hasEgg:
      return "There is already a fish to be spawned here"
    else:
      tile.hasEgg = True
      tile.species = self
      player.spawnFood -= self.cost
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
    self.attacked = []

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.maxHealth, self.currentHealth, self.maxMovement, self.movementLeft, self.carryCap, self.carryingWeight, self.attackPower, self.isVisible, self.maxAttacks, self.attacksLeft, self.range, self.species, ]

  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, maxHealth = self.maxHealth, currentHealth = self.currentHealth, maxMovement = self.maxMovement, movementLeft = self.movementLeft, carryCap = self.carryCap, carryingWeight = self.carryingWeight, attackPower = self.attackPower, isVisible = self.isVisible, maxAttacks = self.maxAttacks, attacksLeft = self.attacksLeft, range = self.range, species = self.species, )

  def heal(self,fish):
    fish.currentHealth += fish.maxHealth * self.game.healPercent
    if fish.currentHealth > fish.maxHealth:
      fish.currentHealth = fish.maxHealth

  #Distance for Taxicab Distance
  def taxiDist(self, source, x, y):
    return abs(source.x-x) + abs(source.y-y)

  #Distance for Euclidean Distance
  def eucDist(self,source,x,y):
    return math.sqrt( (source.x-x)**2 + (source.y-y)**2 )
  
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
      self.attacked = []
      if self.game.getTile(self.x,self.y).owner == self.owner:
        self.heal(self)
      if self.movementLeft == -1:
        self.movementLeft = 0
        self.attackLeft = 0
      else:
        self.movementLeft = self.maxMovement
        self.attacksLeft = self.maxAttacks
      if self.species == 8: #Cuttlefish
        #Set to invisible
        if self.isVisible is True:
          self.game.addAnimation(StealthAnimation(self.id))
        self.isVisible = False
      if self.species != 6: #Tomcod
        self.currentHealth -= self.carryingWeight * self.game.trashDamage #May need to do this at the end of turns in match.py, to ensure a player doesn't think they have a dead fish
        if self.currentHealth < 0:
          self.game.grid[self.x][self.y].remove(self)
          self.game.addAnimation(DeathAnimation(self.id))
          self.game.getTile(self.x, self.y).trashAmount += self.carryingWeight
          self.addTrash(self.x,self.y,self.carryingWeight)
          self.game.removeObject(self)
     #     print "dude died from carrying so much trash"
    return True

  def specName(self, index):
    for spec in self.game.objects.species:
      if index == spec.index:
        return spec.name
    return "Invalid"

  def move(self, x, y):
    speciesName = self.specName(self.species)
    if self.owner != self.game.playerID: #check that you own the fish
      return "You cannot move the other player's %s %i." % (speciesName, self.id)

    elif self.movementLeft <= 0: #check that there are moves left
      return "Your %s %i has no moves left." % (speciesName, self.id)

    elif not (0<=x<self.game.mapWidth) or not (0<=y<self.game.mapHeight):
      return "Your %s %i cannot move off the map. (%i, %i)->(%i, %i)" % (speciesName, self.id, self.x, self.y,  x, y)

    elif self.taxiDist(self,x,y)!=1:
      return "Your %s %i can only move to adjacent locations. (%i, %i)->(%i, %i)" % (speciesName, self.id, self.x, self.y, x, y)

    T = self.game.getTile(x, y) #The tile the player wants to walk onto
    if T.trashAmount > 0:
      return "Your %s %i can't move on top of trash. (%i, %i)->(%i, %i)" % (speciesName, self.id, self.x, self.y, x, y)

    elif T.owner == self.owner^1:
      return "Your %s %i can't move into an opponent's cove. (%i, %i)->(%i, %i)" % (speciesName, self.id, self.x, self.y, x, y)

    elif T.hasEgg:
      return "Your %s %i can't move onto an egg. (%i, %i)->(%i, %i)" % (speciesName, self.id, self.x, self.y, x, y)

    Fishes = self.game.getFish(x,y)
    # print Fishes
    if len(Fishes)>0: #If there is a fish on the tile
      for fish in Fishes:
        if fish.isVisible:
          return "Your %s %i is trying to move onto %s %i." % (speciesName, self.id, self.specName(fish.species), fish.id)
        else:
          #return "Fringe case: moving onto a stealthed fish."
          pass
    self.game.grid[self.x][self.y].remove(self)
    self.game.grid[x][y].append(self)
    self.game.addAnimation(MoveAnimation(self.id,self.x,self.y,x,y))        
    self.movementLeft -= 1
    self.x = x
    self.y = y
    #print "moving a dude"
    return True

  def pickUp(self, x, y, weight):
    speciesName = self.specName(self.id)
    T = self.game.getTile(x,y)
    if self.owner != self.game.playerID:
      return "You cannot control your opponent's %s %i." % (speciesName, self.id)

    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return "Your %s %i cannot pick up trash off the map. (%i, %i)" % (speciesName, self.id, x, y)

    elif self.taxiDist(self,x,y) != 1:
      return "Your %s %i can only pick up adjacent trash. Distance: %i" % (speciesName, self.id, self.taxiDist(self,x,y))

    elif (self.carryingWeight + weight) > self.carryCap:
      return "Your %s %i cannot carry more weight than %i." % (speciesName, self.id, self.carryCap)

    elif weight == 0:
      return "Your %s %i cannot pick up a weight of 0." % (speciesName, self.id)

    elif T.trashAmount < weight:
      return "Your %s %i cannot pick up more trash(%i) than trash present(%i)." % (speciesName, self.id, weight, T.trashAmount)

    elif T.trashAmount == 0:
      return "Your %s %i cannot pick up trash when there is no trash." % (speciesName, self.id)

    elif self.currentHealth < weight*self.game.trashDamage:
      return "Your %s %i cannot pick up trash that would kill it. Health: %i Damage: %i" % (speciesName, self.id, self.currentHealth, weight * self.game.trashDamage)
    
    #don't need to bother checking for fish because a space with a
    #fish shouldn't have any trash, right?
    
    #unstealth fish... because that's what drop did
    if self.isVisible is False:
      self.game.addAnimation(DeStealthAnimation(self.id))
    self.isVisible = True
    
    #take damage if not immune to it
    if self.species != 6: #Tomcod
      self.currentHealth -= self.game.trashDamage * weight
        
    #reduce weight of tile
    tile = self.game.getTile(x,y) 
    priorAmount = tile.trashAmount
    tile.trashAmount-= weight
    self.removeTrash(x,y,weight)
    #add weight to fish
    self.carryingWeight += weight
    print "pickup fish id is %i tile id is %i weight is %i priorAmount was %i new amount is %i"%(self.id, tile.id, weight, priorAmount, tile.trashAmount)
    self.game.addAnimation(PickUpAnimation(self.id,tile.id, tile.x, tile.y,weight))
    #print "dude picked up some trash"
    return True

  def drop(self, x, y, weight):
    speciesName = self.specName(self.species)
    if self.owner != self.game.playerID:
      return "You cannot control the opponent's %s %i." % (speciesName, self.id)

    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return "Your %s %i cannot drop trash off the map. (%i, %i)" % (speciesName, self.id, x, y)

    elif self.taxiDist(self, x, y) != 1:
      return "Your %s %i can only drop onto adjacent locations. Distance: %i" % (speciesName, self.id, self.taxiDist(self,x,y))

    elif weight > self.carryingWeight:
      return "Your %s %i cannot drop more weight(%i) than you're carrying(%i)." % (speciesName, self.id, weight, self.carryingWeight)

    elif weight == 0:
     return "Your %s %i cannot drop a weight of 0." % (speciesName, self.id)

    Fishes = self.game.getFish(x,y)
    if len(Fishes)>0: #If there is a fish on the tile
      for fish in Fishes:
        if fish.isVisible:
          return "Your %s %i cannot drop weight onto %s %i." % (speciesName, self.id, self.specName(fish.species), fish.id)
        else:
          pass #TODO: "Fringe case: dropping onto a stealthed fish."    

    if self.isVisible is False:
      self.game.addAnimation(DeStealthAnimation(self.id))
    self.isVisible = True #unstealth while dropping

    tile = self.game.getTile(x,y)
    tile.trashAmount += weight
    self.carryingWeight -= weight
    print "drop tile id is %i fish id is %i trash amount is %i, weight is %i"%(tile.id,self.id,tile.trashAmount,weight)
    self.game.addAnimation(DropAnimation(self.id,tile.id, tile.x, tile.y, weight))
    self.addTrash(x,y,weight)
    return True

  def attack(self, target):  
    x = target.x
    y = target.y
    speciesName = self.specName(self.species)
    targetName = self.specName(target.species)

    #I feel like stealth units are going to mess up this function
    if self.owner != self.game.playerID:
      return "You cannot control the opponent's %s %i." % (speciesName, self.id)

    elif target.id in self.attacked:
      return "%s %i has already attacked %s %i this turn." % (speciesName, self.id, targetName, target.id)

    elif self.eucDist(self, x, y) > self.range:
      return "Your %s %i can't attack %s %i because it is out of your fish's range(%i). Distance: %i" % (speciesName, self.id, targetName, target.id, self.range, self.eucDist(self, x, y))

    elif self.attacksLeft == 0:
      return "Your %s %i has no attacks left." % (speciesName, self.id)

    elif not isinstance(target, Fish):
      return "Your %s %i can only attack other Fish." % (speciesName, self.id)

    elif target.isVisible is False and target.owner != self.game.playerID:
      return "Your %s %i isn't supposed to see or attack invisible Fish." % (speciesName, self.id)

    elif target.owner != self.owner and self.attackPower < 0:
      return "Your %s %i cannot heal the opponent's %s %i." % (speciesName, self.id, targetName, target.id)

    elif target.owner == self.owner and self.attackPower > 0:
      return "Your %s %i cannot attack a friendly %s %i." % (speciesName, self.id, targetName, target.id)

    elif self.x == x and self.y == y:
      return "Your stealthed %s %i cannot attack a fish above it." % (speciesName, self.id)

    #print "attacking a dude with another dude"
    #Add target to list of attacked targets
    self.attacked.append(target.id)
    if self.species == 9: #Cleaner Shrimp
      self.heal(target)
      if target.isVisible is False:
        self.game.addAnimation(DeStealthAnimation(target.id))
      target.isVisible = True

    #eel stun
    elif self.species == 10: #Electric Eel
      target.movementLeft = -1
      target.attacksLeft = -1
   
    else:   
      #hurt the other fish
      target.currentHealth -= self.attackPower
      #make the attacking fish visible
      if self.isVisible is False:
        self.game.addAnimation(DeStealthAnimation(self.id))
      self.isVisible = True  
    
    #check if target is dead
    if target.currentHealth <= 0:
      #drop trash on tile
      self.game.grid[x][y].remove(target)
      if target.carryingWeight > 0:
        self.game.getTile(x, y).trashAmount += target.carryingWeight
        self.addTrash(target.x, target.y, target.carryingWeight)
      self.game.removeObject(target)
     
    self.game.addAnimation(AttackAnimation(self.id, target.id))
    self.attacksLeft -= 1
    #check for sea urchin counter attacks
    if target.species == 4 and target.owner != self.owner: #Sea Urchin
      self.currentHealth -= target.attackPower / 2.0
      #check if the counter attack killed the fish
      if self.currentHealth <= 0:
        if self.carryingWeight > 0:
          self.game.getTile(x, y).trashAmount += self.carryingWeight
          self.addTrash(self.x, self.y, self.carryingWeight)
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
    if self.game.playerID == self.id:
      self.spawnFood += self.game.spawnFoodPerTurn
      
    return True
    
  def talk(self, message):
    if '\\' in message:
      return "No backslashes in your message, shame on you"
    else:
      self.game.addAnimation(PlayerTalkAnimation(self.id,message))
      return True
  
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

