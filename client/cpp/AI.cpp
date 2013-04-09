#include "AI.h"
#include "util.h"

AI::AI(Connection* conn) : BaseAI(conn) {}

enum AI::speciesIndex { SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH };


const char* AI::username()
{
  return "Shell AI";
}

const char* AI::password()
{
  return "password";
}

//This function is run once, before your first turn.
void AI::init(){}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  //Iterate through all tiles
  for(int i = 0;i < tiles.size();i++)
  {
    //check tile information
    if(tiles[i].owner() == playerID() &&               //Is the tile a cove belonging to you
       tiles[i].hasEgg() == 0 &&                       //Does the tile not have an egg
       getFishIndex(tiles[i].x(), tiles[i].y()) == -1) //Is there not a fish on the cove
    {
      //Interate through all the species
      for(int i = 0;i < species.size(); i++)
      {
        if(species[i].season() == currentSeason() &&             //If the species is in season
           players[playerID()].spawnFood() >= species[i].cost()) //If there is enough money
        {
          //spawn the fish
          species[i].spawn(tiles[i].x(), tiles[i].y());
          //Don't spawn multiple fish on the same tile
          break;
        }
      }
    }
  }

  //Iterate through all the fish
  for(int i = 0;i < fishes.size();i++)
  {
    //only attempt to move owned fish
    if(fishes[i].owner() == playerID())
    {
      //Try to move to the right
      if(fishes[i].x()+1 < mapWidth() &&                                     // We aren't moving off the map
         getTile(fishes[i].x()+1,fishes[i].y()).owner() != 1-playerID() &&   // We aren't moving onto an enemy cove
         getTile(fishes[i].x()+1,fishes[i].y()).hasEgg() == 0 &&             // We aren't moving onto an egg
         getFishIndex(fishes[i].x()+1,fishes[i].y()) == -1 &&                // There is no fish at that spot
         getTile(fishes[i].x()+1, fishes[i].y()).trashAmount() == 0 &&       // There is no trash on the tile
         fishes[i].movementLeft() > 0)                                       // We have moves left
      {
        //move to the right one tile
        fishes[i].move(fishes[i].x()+1,fishes[i].y());
      }

      // Try to pick up trash one tile below the fish
      if(fishes[i].y()+1 < mapHeight() &&                          // Ensure we do not pick up off the map
         fishes[i].carryCap()-fishes[i].carryingWeight() > 0 &&    // Ensure we have the necessary weight
         fishes[i].currentHealth() >= 1 &&                         // Ensure we have enough health
         getTile(fishes[i].x(),fishes[i].y()+1).trashAmount() > 0) // Ensure the tile has trash
      {
        //pick up 1 trash one tile below
        fishes[i].pickUp(fishes[i].x(),fishes[i].y()+1,1);
      }

      // Attempt to drop trash one above the fish
      if(fishes[i].y()-1 >= 0 &&                              // Ensure we don't drop off the map
         getFishIndex(fishes[i].x(),fishes[i].y()-1) == -1 && // Make sure there's no fish where we intend to drop
         fishes[i].carryingWeight() > 0)                      // Ensure we have something to drop
      {
        //drop 1 trash one tile above the fish
        fishes[i].drop(fishes[i].x(),fishes[i].y()-1,1);
      }

      // Try to attack to the right
      if(fishes[i].x()+1 < mapWidth() &&                                                // We aren't attacking off the map
         getFishIndex(fishes[i].x()+1,fishes[i].y()) != -1 &&                           // There is a fish at that spot
         fishes[getFishIndex(fishes[i].x()+1,fishes[i].y())].owner() != playerID() &&   // Then that fish is the opponent's
         fishes[i].attacksLeft() > 0)                                                   // We have attacks left
      {
        //attack the fish one to the right
        fishes[i].attack(fishes[getFishIndex(fishes[i].x()+1,fishes[i].y())]);
      }
    }
  }
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}
