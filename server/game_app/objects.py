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
    T = self.game.getTile (x, y) [0] #The tile the player wants to walk onto
    if T.trashAmount > 0:
      return "You can't move on top of trash"
    elif len(self.game.getFish (x, y)) > 0: #If there is a fish on the tile
      for i in range(1, len(self.game.getFish(x,y))):
        if not self.game.getFish(x, y)[i].isStealthed:
          return "You can't move onto a fish." 
        else:
          print "Fringe case: moving onto a stealthed fish."
          pass
    elif self.game.getTile(x,y)[0].isCove == True and self.game.getTile(x,y)[0].owner != self.owner:
      return "Can't go into an opponent's cove."
    #Working under the assumption that ground units can move anywhere
    self.game.grid[self.x][self.y].remove(self)
    self.game.grid[x][y].append(self)
            
    self.movementLeft -= 1
    self.x = x
    self.y = y
    return "Successful movement. Congrats."

  def pickUp(self, x, y, weight):
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
    # foodPerTurn logic
    p1 = self.players[0]
    p2 = self.objects.players[1]
    fishWorth = [0, 0]
    netWorth = [0, 0]
    # Get current value of fish owned by each player
    for fish in self.objects.fishs:
      fishWorth[fish.owner] += cfgSpecies[fish.species]["cost"]
    # Add value of fish to value of spawn food in respective players' banks to get net worth
    netWorth[0] += (p1.spawnFood + fishWorth[0])
    netWorth[1] += (p2.spawnFood + fishWorth[1])
    # Compare players' net worths
    deltaNetWorth = abs(netWorth[0] - netWorth[1])
    # Calculate food both players get this turn based on whoever is closer to the cap
    # As the fish value cap is approached, the food given to both players decreases
    if fishWorth[0] > fishWorth[1] or fishWorth[0] == fishWorth[1]:
      foodPlayersGetThisTurn = math.floor(self.initialFood * math.sqrt((fishValueCap - fishWorth[0]) / fishValueCap)) # Too fancy?
    elif fishWorth[0] < fishWorth[1]:
      foodPlayersGetThisTurn = math.floor(self.initialFood * math.sqrt((fishValueCap - fishWorth[1]) / fishValueCap))
    p1.spawnFood += foodPlayersGetThisTurn
    p2.spawnFood += foodPlayersGetThisTurn
    # Give player with lower netWorth extra food based on relative error (make deltaNetWorth within a certain percent of the wealthier player's net worth)
    if netWorth[0] > netWorth[1]:
      p2.spawnFood +=
    elif netWorth[1] > netWorth[0]:
      p1.spawnFood +=
    elif deltaNetWorth == 0:
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

