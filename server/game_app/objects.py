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
    if self.game.playerID == self.owner:
      if self.hasEgg:
        species = self.species
        stats = [self.x, self.y, self.owner, species.maxHealth, species.maxHealth, species.maxMovement, species.maxMovement, species.carryCap, 0, species.attackPower, species.maxAttacks, species.maxAttacks, species.range, species.speciesNum]

        newFish = self.game.addObject(Fish, stats)
        self.game.grid[newFish.x][newFish.y].append(newFish)
        self.hasEgg = False

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Species(object):
  game_state_attributes = ['id', 'name', 'speciesNum', 'cost', 'maxHealth', 'maxMovement', 'carryCap', 'attackPower', 'range', 'maxAttacks', 'season']
  def __init__(self, game, id, name, speciesNum, cost, maxHealth, maxMovement, carryCap, attackPower, range, maxAttacks, season):
    self.game = game
    self.id = id
    self.name = name
    self.speciesNum = speciesNum
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
    return [self.id, self.name, self.speciesNum, self.cost, self.maxHealth, self.maxMovement, self.carryCap, self.attackPower, self.range, self.maxAttacks, self.season, ]

  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, name = self.name, speciesNum = self.speciesNum, cost = self.cost, maxHealth = self.maxHealth, maxMovement = self.maxMovement, carryCap = self.carryCap, attackPower = self.attackPower, range = self.range, maxAttacks = self.maxAttacks, season = self.season, )

  def nextTurn(self):
    pass

  def spawn(self, tile):
    player = self.game.objects.players[self.game.playerID]
    x, y = tile.x, tile.y
    if player.spawnFood < self.cost:
      return "Turn %i: The %s requires %i food to spawn. Current food: %i."%(self.game.turnNumber, self.name, self.cost, player.spawnFood)
    elif self.game.currentSeason != self.season:
      return "Turn %i: The %s can only spawn in season %i. Current Season: %i" % (self.game.turnNumber,self.name, self.season, self.game.currentSeason)
    elif len(self.game.getFish(x, y)) != 0:
      return "Turn %i: The %s cannot spawn on Tile %i because a fish is already there."%(self.game.turnNumber, self.name, tile.id)

    if tile.owner != self.game.playerID:
      return "Turn %i: The %s cannot spawn on Tile %i because it is not your cove."%(self.game.turnNumber, self.name, tile.id)
    elif tile.hasEgg:
      return "Turn %i: The %s cannot spawn on Tile %i because it contains an egg."%(self.game.turnNumber, self.name, tile.id)
    elif tile.trashAmount > 0:
      return "Turn %i: The %s cannot spawn on Tile %i because it contains %i trash."%(self.game.turnNumber, self.name, tile.id, tile.trashAmount)
    else:
      tile.hasEgg = True
      tile.species = self
      player.spawnFood -= self.cost
      player.spawnQueue.append(self.cost)
      self.game.addAnimation(SpawnAnimation(tile.owner,tile.x,tile.y,self.name))
    return True

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Fish(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'maxHealth', 'currentHealth', 'maxMovement', 'movementLeft', 'carryCap', 'carryingWeight', 'attackPower', 'maxAttacks', 'attacksLeft', 'range', 'species']
  def __init__(self, game, id, x, y, owner, maxHealth, currentHealth, maxMovement, movementLeft, carryCap, carryingWeight, attackPower, maxAttacks, attacksLeft, range, species):
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
    self.maxAttacks = maxAttacks
    self.attacksLeft = attacksLeft
    self.range = range
    self.species = species
    self.updatedAt = game.turnNumber
    self.attacked = []

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.maxHealth, self.currentHealth, self.maxMovement, self.movementLeft, self.carryCap, self.carryingWeight, self.attackPower, self.maxAttacks, self.attacksLeft, self.range, self.species, ]

  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, maxHealth = self.maxHealth, currentHealth = self.currentHealth, maxMovement = self.maxMovement, movementLeft = self.movementLeft, carryCap = self.carryCap, carryingWeight = self.carryingWeight, attackPower = self.attackPower, maxAttacks = self.maxAttacks, attacksLeft = self.attacksLeft, range = self.range, species = self.species, )

  def heal(self,fish):
    fish.currentHealth += math.ceil(fish.maxHealth * (self.game.healPercent/100))
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
    speciesName = self.game.speciesStrings[self.species]
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
      if self.species != 6: #Tomcod
        self.currentHealth -= self.carryingWeight #May need to do this at the end of turns in match.py, to ensure a player doesn't think they have a dead fish
        if self.currentHealth <= 0:
          self.game.grid[self.x][self.y].remove(self)
          self.game.addAnimation(DeathAnimation(self.id))
          tile = self.game.getTile(self.x, self.y)
          tile.trashAmount += self.carryingWeight
#          self.game.addAnimation(DropAnimation(self.id,tile.id, self.x, self.y, self.carryingWeight))
          self.addTrash(self.x,self.y,self.carryingWeight)
          self.game.removeObject(self)
    return True

  def move(self, x, y):
    speciesName = self.game.speciesStrings[self.species]
    if self.owner != self.game.playerID: #check that you own the fish
      return "Turn %i: You cannot move the other player's %s %i. (%i, %i)->(%i, %i)"%(self.game.turnNumber, speciesName, self.id, self.x, self.y, x, y)

    elif self.movementLeft <= 0: #check that there are moves left
      return "Turn %i: Your %s %i has no moves left."%(self.game.turnNumber, speciesName, self.id)

    elif not (0<=x<self.game.mapWidth) or not (0<=y<self.game.mapHeight):
      return "Turn %i: Your %s %i cannot move off the map. (%i, %i)->(%i, %i)"%(self.game.turnNumber, speciesName, self.id, self.x, self.y,  x, y)

    elif self.taxiDist(self,x,y)!=1:
      return "Turn %i: Your %s %i can only move to adjacent locations. (%i, %i)->(%i, %i)"%(self.game.turnNumber, speciesName, self.id, self.x, self.y, x, y)

    T = self.game.getTile(x, y) #The tile the player wants to walk onto
    if T.trashAmount > 0:
      return "Turn %i: Your %s %i can't move on top of trash. (%i, %i)->(%i, %i)"%(self.game.turnNumber, speciesName, self.id, self.x, self.y, x, y)

    elif T.owner == self.owner^1:
      return "Turn %i: Your %s %i can't move into an opponent's cove. (%i, %i)->(%i, %i)"%(self.game.turnNumber, speciesName, self.id, self.x, self.y, x, y)

    elif T.owner == 3:
      return "Turn %i: Your %s %i can't move into an a wall. (%i, %i)->(%i, %i)"%(self.game.turnNumber, speciesName, self.id, self.x, self.y, x, y)

    elif T.hasEgg:
      return "Turn %i: Your %s %i can't move onto an egg. (%i, %i)->(%i, %i)"%(self.game.turnNumber, speciesName, self.id, self.x, self.y, x, y)

    Fishes = self.game.getFish(x,y)
    if len(Fishes)>0: #If there is a fish on the tile
      for fish in Fishes:
        return "Turn %i: Your %s %i is trying to move onto %s %i. (%i, %i)->(%i, %i)" % (self.game.turnNumber, speciesName, self.id, self.game.speciesStrings[self.species], fish.id, self.x, self.y, x, y)
    self.game.grid[self.x][self.y].remove(self)
    self.game.grid[x][y].append(self)
    self.game.addAnimation(MoveAnimation(self.id,self.x,self.y,x,y))
    self.movementLeft -= 1
    self.x = x
    self.y = y
    return True

  def pickUp(self, tile, weight):
    x, y = tile.x, tile.y
    speciesName = self.game.speciesStrings[self.species]
    if self.owner != self.game.playerID:
      return "Turn %i: You cannot control your opponent's %s %i."%(self.game.turnNumber, speciesName, self.id)

    elif self.taxiDist(self,x,y) != 1:
      return "Turn %i: Your %s %i can only pick up adjacent trash. Distance: %i"%(self.game.turnNumber, speciesName, self.id, self.taxiDist(self,x,y))

    elif (self.carryingWeight + weight) > self.carryCap:
      return "Turn %i: Your %s %i cannot carry more weight than %i."%(self.game.turnNumber, speciesName, self.id, self.carryCap)

    elif weight < 1 :
      return "Turn %i: Your %s %i cannot pick up a weight less than 1."%(self.game.turnNumber, speciesName, self.id)


    if tile.trashAmount < weight:
      return "Turn %i: Your %s %i cannot pick up more trash(%i) than trash present(%i)."%(self.game.turnNumber, speciesName, self.id, weight, tile.trashAmount)

    elif tile.trashAmount < 1:
      return "Turn %i: Your %s %i cannot pick up trash when there is no trash." % (self.game.turnNumber, speciesName, self.id)

    #don't need to bother checking for fish because a space with a
    #fish shouldn't have any trash, right?

    #take damage if not immune to it
    if self.species != 6: #Tomcod
      self.currentHealth -= weight

    #reduce weight of tile
    priorAmount = tile.trashAmount
    tile.trashAmount-= weight
    self.removeTrash(x,y,weight)
    #add weight to fish
    self.carryingWeight += weight
    self.game.addAnimation(PickUpAnimation(self.id, tile.id, x, y, weight))
    if self.currentHealth <= 0:
      self.game.grid[self.x][self.y].remove(self)
      self.game.addAnimation(DeathAnimation(self.id))
      tile = self.game.getTile(self.x, self.y)
      tile.trashAmount += self.carryingWeight
      #          self.game.addAnimation(DropAnimation(self.id,tile.id, self.x, self.y, self.carryingWeight))
      self.addTrash(self.x,self.y,self.carryingWeight)
      self.game.removeObject(self)
    return True

  def drop(self, tile, weight):
    x, y = tile.x, tile.y
    speciesName = self.game.speciesStrings[self.species]
    if self.owner != self.game.playerID:
      return "Turn %i: You cannot control the opponent's %s %i."%(self.game.turnNumber, speciesName, self.id)

    elif self.taxiDist(self, x, y) != 1:
      return "Turn %i: Your %s %i can only drop onto adjacent locations. Distance: %i"%(self.game.turnNumber, speciesName, self.id, self.taxiDist(self,x,y))

    elif tile.hasEgg == 1:
      return "Turn %i: Your %s %i cannot drop trash on a tile that has an egg."%(self.game.turnNumber, speciesName, self.id)

    elif weight > self.carryingWeight:
      return "Turn %i: Your %s %i cannot drop more weight(%i) than you're carrying(%i)."%(self.game.turnNumber, speciesName, self.id, weight, self.carryingWeight)

    elif weight < 1:
     return "Turn %i: Your %s %i cannot drop a weight of 0."%(self.game.turnNumber,speciesName, self.id)

    Fishes = self.game.getFish(x,y)
    if len(Fishes)>0: #If there is a fish on the tile
      for fish in Fishes:
        return "Turn %i: Your %s %i cannot drop weight onto %s %i."%(self.game.turnNumber, speciesName, self.id, self.game.speciesStrings[self.species], fish.id)

    tile.trashAmount += weight
    self.carryingWeight -= weight
    self.game.addAnimation(DropAnimation(self.id,tile.id, tile.x, tile.y, weight))
    self.addTrash(x,y,weight)
    return True

  def attack(self, target):
    x = target.x
    y = target.y
    speciesName = self.game.speciesStrings[self.species]
    targetName = self.game.speciesStrings[target.species]

    #I feel like stealth units are going to mess up this function
    if self.owner != self.game.playerID:
      return "Turn %i: You cannot control the opponent's %s %i."%(self.game.turnNumber, speciesName, self.id)

    elif target.id in self.attacked:
      return "Turn %i: %s %i has already attacked %s %i this turn."%(self.game.turnNumber, speciesName, self.id, targetName, target.id)

    elif self.taxiDist(self, x, y) > self.range:
      return "Turn %i: Your %s %i can't attack %s %i because it is out of your fish's range(%i). Distance: %i"%(self.game.turnNumber, speciesName, self.id, targetName, target.id, self.range, self.eucDist(self, x, y))

    elif self.attacksLeft < 1:
      return "Turn %i: Your %s %i has no attacks left."%(self.game.turnNumber, speciesName, self.id)

    elif not isinstance(target, Fish):
      return "Turn %i: Your %s %i can only attack other Fish."%(self.game.turnNumber, speciesName, self.id)

    elif target.currentHealth < 0:
      return "Turn %i: Your %s %i cannot attack a dead fish %s %i."%(self.game.turnNumber, speciesName, self.id, targetName, target.id)

    elif target.owner != self.owner and self.attackPower < 0:
      return "Turn %i: Your %s %i cannot heal the opponent's %s %i."%(self.game.turnNumber, speciesName, self.id, targetName, target.id)

    elif target.owner == self.owner and self.attackPower > 0:
      return "Turn %i: Your %s %i cannot attack a friendly %s %i."%(self.game.turnNumber, speciesName, self.id, targetName, target.id)

    #Add target to list of attacked targets
    self.attacked.append(target.id)
    if self.species == 9: #Cleaner Shrimp
      self.heal(target)

    #eel stun
    elif self.species == 10: #Electric Eel
      target.movementLeft = -1
      target.attacksLeft = -1

    else:
      #hurt the other fish
      target.currentHealth -= self.attackPower
      #make the attacking fish visible

    self.game.addAnimation(AttackAnimation(self.id, target.id))
    self.attacksLeft -= 1
    #check for sea urchin counter attacks
    if target.species == 4 and target.owner != self.owner: #Sea Urchin
      if abs(target.x - self.x) + abs(target.y - self.y) == target.range: #Only counter-attack if it's within range
        self.currentHealth -= target.attackPower
        #check if the counter attack killed the fish
        if self.currentHealth <= 0:
          if self.carryingWeight > 0:
            self.game.getTile(self.x, self.y).trashAmount += self.carryingWeight
            self.addTrash(self.x, self.y, self.carryingWeight)
          self.game.grid[self.x][self.y].remove(self)
          self.game.removeObject(self)

    #check if target is dead
    if target.currentHealth <= 0:
      #drop trash on tile
      self.game.grid[x][y].remove(target)
      if target.carryingWeight > 0:
        self.game.getTile(x, y).trashAmount += target.carryingWeight
        self.addTrash(target.x, target.y, target.carryingWeight)
      self.game.removeObject(target)

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
    self.turnNumber = game.turnNumber
    self.spawnQueue = []

  def toList(self):
    return [self.id, self.playerName, self.time, self.currentReefHealth, self.spawnFood, ]

  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, currentReefHealth = self.currentReefHealth, spawnFood = self.spawnFood, )

  def nextTurn(self):
    #TODO: Give food back to player
    #Fish spawn in at beginning of turn
    #if self.game.playerID == self.id:
    #  self.spawnFood += self.game.spawnFoodPerTurn
    #
    # Identify player who is getting money
    if self.game.playerID == self.id:
      # Get current value of fish owned by each player
      fishWorth = [0, 0]
      for fish in self.game.objects.fishes:
        #fishWorth[fish.owner] += cfgSpecies[fish.species]["cost"]
        fishWorth[fish.owner] += self.game.speciesDict[fish.species].cost
      # Get value of fish in spawnQueue
      inSpawnQueue = sum(self.spawnQueue)
      self.spawnQueue = []
      # Calculate currentPlayer's net worth by adding value of owned fish and spawning fish to available spawn food
      netWorth = fishWorth[self.id] + self.spawnFood + inSpawnQueue
      # How much your net worth should be if you have not lost any units
      foodYouShouldHave = self.game.maxFood
      # How much spawn food you get
      foodYouGet = math.ceil((foodYouShouldHave - netWorth) * self.game.foodRate)
      self.spawnFood += foodYouGet
      #print "Giving player", self.id, foodYouGet, "spawn food"

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

class PlayerTalkAnimation:
  def __init__(self, actingID, message):
    self.actingID = actingID
    self.message = message

  def toList(self):
    return ["playerTalk", self.actingID, self.message, ]

  def toJson(self):
    return dict(type = "playerTalk", actingID = self.actingID, message = self.message)

