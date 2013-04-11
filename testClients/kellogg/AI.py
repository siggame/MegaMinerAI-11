#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math
import heapq
import random

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Kellogg"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    self.coves = [tile for tile in self.tiles if tile.owner==self.playerID]
    self.adjacentList = [(-1,0),(1,0),(0,1),(0,-1)]
    self.seasonDict = {0:[],2:[],3:[],1:[]}
    for species in self.species:
      self.seasonDict[species.season].append(species)
    self.allSpecies = [species.name for species in self.species]
    self.myPlayer = self.players[self.playerID]

  ##This function is called once, after your last turn
  def end(self):
    pass

#can return a tile or a fish
  def getObject(self,x,y):
    return self.grid[x][y][-1]

  def getFish(self,x,y):
    if len(self.grid[x][y])>1:
      return self.grid[x][y][1:]
    return None
    
  def getTile(self,x,y):
    return self.tiles[x*self.mapHeight+y]

  def moveTo(self,fish,target):
     path = self.pathFind(fish.x,fish.y,target.x,target.y)
     if path != None:
       while fish.movementLeft>0 and len(path)>0:
         next = path.pop()
         if next!=(fish.x,fish.y) and fish.movementLeft>0:
           self.removeGrid(fish)
           fish.move(next[0],next[1])
           self.addGrid(fish.x,fish.y,fish)    

  def findAdjacent(self,x,y):
    for adj in self.adjacentList:
      dx = x+adj[0]; dy = y+adj[1]
      thing = self.getObject(dx,dy)
      if isinstance(thing, Tile) and thing.trashAmount == 0 and thing.owner != self.playerID^1 and not thing.hasEgg:
        if 0<=thing.x<self.mapWidth and 0<=thing.y<self.mapHeight:
          return (dx,dy)
    return None

  def removeGrid(self, target):
    self.grid[target.x][target.y].remove(target)
    
  def addGrid(self, x, y, target):
    self.grid[x][y].append(target)
      
  def adjacent(self, x, y):
    adj = []
    if x+1<self.mapWidth:
        adj.append((x+1,y))
    if y-1>=0:
        adj.append((x,y-1))
    if x-1>=0:
        adj.append((x-1,y))
    if y+1<self.mapHeight:
        adj.append((x,y+1))
    return adj  
  
  def pathFind(self, startX, startY, goalX, goalY):
    closedSet = set();closedTup=set()
    # 0 = distance from goal, 1 = current (x,y), 2 = parent (x,y) 3 = distance from start
    open = [(self.distance(startX,startY,goalX,goalY),(startX,startY),(startX,startY),0)];openTup=[(startX,startY)]
    path = []
    while len(open)>0:
      #open.sort()
      current = heapq.heappop(open)
      if current[1] == (goalX,goalY):
        node = current
        path = []
        while node[2]!=(startX,startY):
          for closed in closedSet:
            if self.distance(node[1][0],node[1][1],closed[1][0],closed[1][1])==1 and node[2] == closed[1]:
              path.append(node[2])
              node = closed
        return path
      closedSet.add(current);closedTup.add(current[1])
      openTup.remove(current[1])
      for neighbor in self.adjacent(current[1][0],current[1][1]):#,[(startX,startY),(goalX,goalY)]):
       #game specific
       tile = self.getTile(neighbor[0],neighbor[1])
       fish = self.getFish(neighbor[0],neighbor[1])
       ###
       if (tile.owner!=self.playerID^1 and tile.trashAmount==0 and fish==None) or (neighbor[0],neighbor[1])==(goalX,goalY):
        if neighbor in closedTup:
         continue
        g = current[3]+self.distance(neighbor[0],neighbor[1],current[1][0],current[1][1])
        if neighbor == (goalX,goalY) or self.distance(neighbor[0],neighbor[1],startX,startY)<=g+1 and neighbor not in openTup:
          neighborTup = (g+self.distance(neighbor[0],neighbor[1],goalX,goalY),(neighbor[0],neighbor[1]),(current[1]),g)
          heapq.heappush(open,neighborTup);openTup.append(neighbor)
    return None
  
  def findNearest(self,myDude, list):
    dis = 1000
    nearest = 1
    for mapp in list:
      if self.distance(myDude.x,myDude.y,mapp.x,mapp.y)<dis:
          nearest = mapp
    return nearest
  
  def distance(self,x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)

  def pickUpTrash(self,fish):
    #find nearest trash
    trashDir = {self.distance(fish.x,fish.x,key[0],key[1]):key for key in self.trashDict if not self.isSafe(key[0])}
    if len(trashDir)<1:
      return False
    trash = self.getTile(trashDir[min(trashDir)][0],trashDir[min(trashDir)][1])
    self.moveTo(fish,trash)
    if self.distance(fish.x,fish.y,trash.x,trash.y)==1 and fish.carryingWeight!=fish.carryCap:
      x = trash.trashAmount
      amount = min(fish.carryCap-fish.carryingWeight,trash.trashAmount, fish.currentHealth-1)   
      if amount>0:
        y = fish.pickUp(trash.x,trash.y,amount) 
        if y:
          self.removeTrash(trash.x,trash.y,amount)
      return True
    return False

  def addTrash(self,x,y,weight):
    if (x,y) not in self.trashDict:
      self.trashDict[(x, y)] = weight
    else:
      self.trashDict[(x, y)] += weight
  
  def removeTrash(self, x,y, weight):
    self.trashDict[(x,y)]-=weight
    if self.trashDict[(x,y)] == 0:
      del self.trashDict[(x,y)]

  def isSafe(self,x):
    if self.playerID == 0 and x > self.mapWidth / 2 + self.boundLength:
      return True
    elif self.playerID == 1 and x < self.mapWidth / 2 - self.boundLength:
      return True
    return False

  def pushTrash(self, fish):
    #theirTiles = [tile for tile in self.tiles if self.isSafe(tile.x) and tile.owner==2]
    #tile = random.choice(theirTiles)
    if self.playerID == 0:
      while fish.movementLeft > 0:
        y = fish.move(fish.x + 1, fish.y)
        if not y:
          return False
    else:
     while fish.movementLeft > 0:
       y = fish.move(fish.x - 1, fish.y)
       if not y:
         return False

  def smartSpawn(self):
    seasonal = self.seasonDict[self.currentSeason]
    speciesList = [species.name for species in seasonal]
    #print speciesList

  def speciesList(self, player, fish, index):
      return [fish for fish in self.fishes if fish.owner == player and fish.species == index]

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    self.grid = [[[] for _ in range(self.mapHeight)] for _ in range(self.mapWidth)]
    for life in self.tiles+self.fishes:
      self.addGrid(life.x, life.y, life)
    
    self.trashDict = {(tile.x, tile.y):tile.trashAmount for tile in self.tiles if tile.trashAmount > 0}
    self.myFish = [fish for fish in self.fishes if fish.owner == self.myPlayer.id]
    self.enemyFish = [fish for fish in self.fishes if fish.owner != self.myPlayer.id]

    self.pushers = ['Tomcod', 'Sponge', 'Angelfish', 'Sea Star']
    self.fighers = ['Cone Shell Snail', 'Reef Shark', 'Octopus', 'Jellyfish','Electric Eel']
    self.Shrimps = ['CleanerShrimp']
    self.Cuttles = ['Cuttlefish']

    self.myPlayer.talk("I'm so happy to be olive")
    self.smartSpawn()

    #spawn some dudes
    seasonal = self.seasonDict[self.currentSeason]







    for cove in self.coves:
      for species in seasonal:
        if species.carryCap > 0 and cove.owner == self.playerID and not cove.hasEgg and len(self.grid[cove.x][cove.y]) == 1 and self.myPlayer.spawnFood >= species.cost and species.index != 8:
          species.spawn(cove.x,cove.y)

    for fish in self.fishes: 
      if fish.owner == self.playerID and fish.carryCap > 0:
        if fish.carryCap > fish.carryingWeight:    
          self.pickUpTrash(fish)
        else:
          self.pushTrash(fish) 
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
