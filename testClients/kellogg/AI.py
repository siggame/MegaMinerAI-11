#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    self.coves = []
    for tile in self.tiles:
      if tile.owner == self.playerID:
        self.coves.append(tile)

  ##This function is called once, after your last turn
  def end(self):
    pass

  def getObject(self,x,y):
   if len(self.grid[x][y])>0:
     return self.grid[x][y][0]
   else:
    return []
    
  def moveTo(self,fish,target):
     path = self.pathFind(fish.x,fish.y,target.x,target.y)
     if path != None:
       while fish.movementLeft>0 and len(path)>0:
         next = path.pop()
         if next!=(fish.x,fish.y) and fish.movementLeft>0:
           self.removeGrid(fish)
           fish.move(next[0],next[1])
           self.addGrid(fish.x,fish.y,fish)    
    
  def removeGrid(self,target):
    self.grid[target.x][target.y].remove(target)
    
  def addGrid(self,x,y,target):
    self.grid[x][y].append(target)
      
  def adjacent(self,x,y):
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
  
  def pathFind(self,startX,startY,goalX,goalY):
    closedSet = set();closedTup=set()
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
       if self.getObject(neighbor[0],neighbor[1])==[] or (neighbor[0],neighbor[1])==(goalX,goalY):# or (neighbor[0],neighbor[1])==(startX,startY):
        if neighbor in closedTup:
         continue
        g = current[3]+self.distance(neighbor[0],neighbor[1],current[1][0],current[1][1])
        if neighbor == (goalX,goalY) or self.distance(neighbor[0],neighbor[1],startX,startY)<=g+1 and neighbor not in openTup:
          neighborTup = (g+self.distance(neighbor[0],neighbor[1],goalX,goalY),(neighbor[0],neighbor[1]),(current[1]),g)
          heapq.heappush(open,neighborTup);openTup.append(neighbor)
    return None
  
  def findFish(self,myDude):
    dis = 400
    nearest = 1
    for fish in self.fishes:
      if self.distance(myDude,fish)<dis and fish.id!=myDude:
          nearest = fish
    return nearest
  
  def distance(self,source,target):
    return abs(source.x-target.x)+abs(source.y-target.y)

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    self.grid = [[[] for _ in range(self.mapHeight)] for _ in range(self.mapWidth)]
    for life in self.tiles+self.fishes:
      self.addGrid(life.x,life.y,life)

    for species in self.species:
      for cove in self.coves:
        species.spawn(cove.x,cove.y)
        
    for fish in self.fishes:
      fish.move(fish.x+1,fish.y)
      fish.pickUp(fish.x,fish.y+1,1)
      fish.pickUp(fish.x,fish.y-1,1)
      fish.drop(fish.x-1,fish.y,1)
      fish.attack(self.findFish(fish))
      fish.attack(fish)
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
