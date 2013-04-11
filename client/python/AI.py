#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH = range(12)

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
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):

    #Iterate through all tiles
    for tile in self.tiles:

      #Check tile information
      if tile.owner == self.playerID and tile.hasEgg == 0 and self.getFishIndex(tile.x, tile.y) == -1:

        #Iterate through all the species.
        for species in self.speciesList:

          #If the species is in season and if there is enough money.
          if species.season == self.currentSeason and self.players[self.playerID].spawnFood >= species.cost:

            #Spawn the fish
            species.spawn(tile)
            #Don't spawn multiple fish on the same tile.
            break

    #Iterate through all the fish
    for fish in self.fishes:

      #Only attempt to move owned fish
      if fish.owner == self.playerID:

        if (fish.x+1 < self.mapWidth                                         # We aren't moving off the map
          and self.getTile(fish.x+1, fish.y).owner != self.playerID^1   # We aren't moving onto an enemy cove
          and self.getTile(fish.x+1, fish.y).hasEgg == 0                   # We aren't moving onto an egg
          and self.getFishIndex(fish.x+1, fish.y) == -1                      # There is no fish at that spot
          and self.getTile(fish.x+1, fish.y).trashAmount == 0                # There is no trash on the tile
          and fish.movementLeft > 0):                                        # We have moves left

          #Move to the right one tile.
          fish.move(fish.x+1, fish.y)

        # Try to pick up trash one tile below the fish
        if(fish.y+1 < self.mapHeight                               # Ensure we do not pick up off the map
          and fish.carryCap - fish.carryingWeight > 0            # Ensure we have the necessary weight
          and fish.currentHealth >= 1                              # Ensure we have enough health
          and self.getTile(fish.x, fish.y+1).trashAmount > 0): # Ensure the tile has trash

          # Pick up 1 trash one tile below the fish
          fish.pickUp(self.getTile(fish.x, fish.y+1), 1)

        # Attempt to drop trash one above the fish
        if(fish.y-1 >= 0                                  # Ensure we don't drop off the map
          and self.getFishIndex(fish.x, fish.y-1) == -1   # Make sure there's no fish where we intend to drop
          and fish.carryingWeight > 0):                 # Ensure we have something to drop

          # Drop 1 trash one tile above the fish
          fish.drop(self.getTile(fish.x, fish.y-1), 1)

        # Try to attack to the right
        if(fish.x+1 < self.mapWidth                                                         # We aren't attacking off the map
          and self.getFishIndex(fish.x+1,fish.y) != -1                                  # There is a fish at that spot
          and self.fishes[self.getFishIndex(fish.x+1, fish.y)].owner != self.playerID # Then that fish is the opponent's
          and fish.attacksLeft > 0):                                                      # We have attacks left

          # Attack the fish one to the right
          fish.attack(self.fishes[self.getFishIndex(fish.x+1,fish.y)])

    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)

