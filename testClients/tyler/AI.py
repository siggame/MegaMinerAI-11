#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math
import random

SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH = range(12)

class AI(BaseAI):
  """The class implementing gameplay logic."""

  @staticmethod
  def username():
    return "Tyler"

  @staticmethod
  def password():
    return "yay"
  
  #This function is called once, before your first turn
  def init(self):
    self.myCoves = [tile for tile in self.tiles if tile.owner==self.playerID]
    self.seasonDict = {0:[],1:[],2:[],3:[]}
    for species in self.species:
      self.seasonDict[species.season].append(species)
    self.me = self.players[self.playerID]

  #This function is called once, after your last turn
  def end(self):
    pass
  
  def getObject(self,x,y):
    return self.map[x][y][-1]
  
  def addMap(self, x, y, target):
    self.map[x][y].append(target)
    
  def getTile(self,x,y):
    return self.tiles[x*self.mapHeight+y]
    
  def getTrash(self):
    trashTiles = []
    for tile in self.tiles:
      if tile.trashAmount > 0:
        trashTiles.append(tile)
    return trashTiles
  
  def getFriends(self):
    friends = []
    for guy in self.fishes:
      if guy.owner == self.playerID:
        friends.append(guy)
    return friends
    
  def getEnemies(self):
    enemies = []
    for guy in self.fishes:
      if guy.owner != self.playerID:
        enemies.append(guy)
    return enemies
    
  def getAdjacent(self, x, y):
    adj = []
    if x + 1 < self.mapWidth:
      adj.append(self.getTile(x+1,y))
    if x - 1 > 0:
      adj.append(self.getTile(x-1,y))
    if y + 1 < self.mapHeight:
      adj.append(self.getTile(x,y+1))
    if y - 1 > 0:
      adj.append(self.getTile(x,y-1))
    return adj
  
  def validMove(self, x, y):
    if x >= self.mapWidth or x < 0:
      return 0
    if y >= self.mapHeight or y < 0:
      return 0
    tile = self.getTile(x, y)
    if tile.owner != self.playerID or tile.hasEgg or tile.trashAmount > 0:
      return 0
    if isinstance(self.getObject(x,y), Fish):
      return 0
    return 1
  
  def affordable(self, money):
    afford = []
    curSpecies = self.seasonDict[self.currentSeason]
    for species in curSpecies:
      if species.cost <= money:
         afford.append(species)
    return afford
    
  def manhatdist(self, x, y, destx, desty):
    return abs(destx - x) + abs(desty - y)
    
  def pathfind(self, x, y, destx, desty):
    closed = set()
    path = []
    current = self.getTile(x, y)
    #path.append(current)
    target = self.getTile(destx, desty)
    #closed.add(current)
    while target not in closed:
      open = []
      for tile in self.getAdjacent(current.x, current.y):
        if self.validMove(tile.x, tile.y) == 1 and tile not in closed:
          open.append(tile)
      if len(open) > 0:
        min = self.manhatdist(open[0].x, open[0].y, destx, desty)
        mindex = 0
        for node in open:
          dist = self.manhatdist(node.x, node.y, destx, desty)
          if dist <= min:
            min = dist
            mindex = open.index(node)
        path.append(current)
        closed.add(current)
        current = open[mindex]
      
      else:
        return path
        '''
        if len(path) == 0:
          print "no moves to make, argh!"
          return path
        print "stuck at ", current.x, current.y
        closed.add(current)
        current = path.pop()
        #path.append(current)
        print "path = "
        for item in path:
          print item.x, item.y
        #closed.remove(current)
        print "popped"
        print "back to = ", current.x, " ", current.y
        '''
    return path
  
  def makeMove(self, fish, destx, desty):
    path = self.pathfind(fish.x, fish.y, destx, desty)
    for node in path:
      print node.x,node.y
    movesLeft = fish.maxMovement
    i = 0
    if len(path) == 0:
      return 0
    while movesLeft > 0 and i < len(path):
      fish.move(path[i].x, path[i].y)
      i += 1
      movesLeft -= 1
    return 1
    
  #This function is called each time it is your turn
  #Return true to end your turn, return false to ask the server for updated information
  def run(self):
    self.map = [[[] for _ in range(self.mapHeight)] for _ in range(self.mapWidth)]
    for life in self.tiles+self.fishes:
      self.addMap(life.x, life.y, life)
    enemies = self.getEnemies()
    friends = self.getFriends()
    #centerx = self.mapWidth/2
    centerx = 7
    #centery = self.mapHeight/2
    centery = 3
    
    #while money > :
    for friend in friends:
      print "start = ", friend.x, friend.y
      adjacent = self.getAdjacent(friend.x, friend.y)
      nearTrash = []
      nearEggs = []
      nearFish = []
      for tile in adjacent:
        if tile.trashAmount > 0:
          nearTrash.append(tile)
        if tile.hasEgg:
          nearEggs.append(tile)
        if isinstance(self.getObject(tile.x,tile.y), Fish):
          nearFish.append(tile)
      print "gonna make move"
      if self.makeMove(friend, centerx, centery) == 0:
        print "number of trash near: ",len(nearTrash)
        print "number of eggs near: ",len(nearEggs)
        print "number of fish near: ",len(nearFish)
        if len(nearTrash) > 0:
          carrying = friend.carryingWeight
          cap = friend.carryCap
          choice = nearTrash[random.randint(0, len(nearTrash)-1)]
          for spot in nearTrash:
            if spot.trashAmount <= cap:
              choice = spot
          while carrying < cap and choice.trashAmount > 0:
            friend.pickUp(choice.x, choice.y, 1)
            carrying += 1
          #self.makeMove(friend, centerx, centery)
      print "end", friend.x, friend.y
    money = self.me.spawnFood
    #idiotic spawn
    for cove in self.myCoves:
      canAfford = self.affordable(money)
      num = len(canAfford)
      if num > 0:
        speciesChoice = canAfford[random.randint(0,len(canAfford)-1)]
        if not cove.hasEgg:
          print "Cove location: "
          print cove.x, cove.y
          speciesChoice.spawn(cove.x, cove.y)
          cove.hasEgg = True
          #print "Species spawned: ", speciesChoice
          money = money - speciesChoice.cost
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
