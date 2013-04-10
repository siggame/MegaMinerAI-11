#-*-python-*-
from BaseAI import BaseAI
from operator import attrgetter
from pathing import Pathfinder

SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH = range(12)

class AI(BaseAI):
  """The class implementing gameplay logic."""

  @staticmethod
  def username():
    return "Virtuamancer"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    self.coves = [i for i in self.tiles if i.owner == self.playerID]
    self.grid = Pathfinder(self)
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    self.in_season = [i for i in self.species if i.season == self.currentSeason]
    self.move_all()
    self.spawn()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)

  def move_all(self):
    for i in self.fishes:
      if i.owner == self.playerID:
        self.move_fish(i)

  def move_fish(self, fish):
    if self.playerID == 0:
      target = range(23, 41)
    else:
      target = range(0, 18)
    self.grid.populate()
    dests = self.grid.path(fish)
    for i in dests:
      #TODO: Find nearest enemy tile rather than a cove.
      if i.x in target:
        closest = i
        break
    else:
      return
    dest = closest.source
    self.moveToward(fish, dest)
    if fish.x == dest.x and fish.y == dest.y:
      self.players[self.playerID].talk('Down you go!')
      fish.drop(closest.x, closest.y, -1)
      fish.pickUp(closest.x, closest.y, -30000)


  def moveToward(self, fish, tile):
    path = [tile]
    while path[-1].source:
      path.append(path[-1].source)
    path = path[-fish.movementLeft - 1:]
    path.pop()
    while path:
      next = path.pop()
      fish.move(next.x, next.y)

  def spawn(self):
    closest = min(self.coves, key = lambda x: abs(self.mapWidth/2 - x.x))
    fastest = max(self.in_season, key = attrgetter('maxMovement'))

    fastest.spawn(closest.x, closest.y)
