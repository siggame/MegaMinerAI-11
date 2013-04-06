#include "AI.h"
#include "util.h"

AI::AI(Connection* conn) : BaseAI(conn) {}

//IMPORTANT NOTE!
//Accessing the species as followes:
//species[SEA_STAR]
//Will NOT work.
//Use getSpecies(SEA_STAR) instead.
enum AI::speciesIndex { SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH };


const char* AI::username()
{
  return "Shell AI";
}

const char* AI::password()
{
  return "password";
}

int enemyAI_ID;

//This function is run once, before your first turn.
void AI::init()
{
  //get the opponent's ID
  if(playerID() == 0)
  {
    enemyAI_ID = 1;
  }
  else
  {
    enemyAI_ID = 0;
  }
}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  //loop through all of the tiles
  for(int i = 0;i < tiles.size();i++)
  {
    //if this tile is one of my coves and does not have a fish on it
    if(tiles[i].owner() == playerID() &&
       getFishIndex(tiles[i].x(), tiles[i].y()) == -1)
    {
      //loop through all of the species
      for(int p = 0;p<species.size(); p++)
      {
        //if the current species is in season
        if(species[p].season() == currentSeason())
        {
          //if I have enough food to spawn the fish in and there is not
          //an egg on that tile already
          if(players[playerID()].spawnFood() >= species[p].cost() &&
             tiles[i].hasEgg() == false)
          {
            //spawn the fish on that tile
            species[p].spawn(tiles[i].x(), tiles[i].y());
          }
        }
      }
    }
  }

  //loop through all of the fish
  for(int i = 0;i < fishes.size();i++)
  {
    //if this is my fish
    if(fishes[i].owner() == playerID())
    {
      int x = fishes[i].x();
      int y = fishes[i].y();
      if(fishes[i].x() >= 1)
      {
        //if the tile to the left has trash and the current fish can
        //carry at least one more trash
        if(getTile(x - 1, y).trashAmount() > 0 &&
           fishes[i].carryingWeight() + 1 <= fishes[i].carryCap())
        {
          //if the fish has enought health to pick up trash
          if(1 * trashDamage() < fishes[i].currentHealth())
          {
            //pick up trash to the left of the fish
            fishes[i].pickUp(x - 1, y, 1);
          }
        }
      }
      //if the fish carrying any trash
      if(fishes[i].carryingWeight() > 0)
      {
        //if the fish in the enemy's side
        if((fishes[i].x() < mapWidth()/2 - boundLength() - 1 && enemyAI_ID == 0) ||
           (fishes[i].x() > mapWidth()/2 + boundLength() + 1 && enemyAI_ID == 1))
        {
          if(fishes[i].y() != 0)
          {
            //if the tile above the fish is not a cove and has no fish
            if(getTile(x, y - 1).owner() == 2 && getFishIndex(x, y + 1) == -1)
            {
              //drop all of the trash the fish is carrying
              fishes[i].drop(x, y - 1, fishes[i].carryingWeight());
            }
          }
          else if(fishes[i].y() != mapHeight() - 1)
          {
            //if the tile below the fish is not a cove and has no fish
            if(getTile(x,y + 1).owner() == 2 && getFishIndex(x,y + 1) == -1)
            {
              //drop all of the trash the fish is carrying
              fishes[i].drop(x, y + 1, fishes[i].carryingWeight());
            }
          }
        }
      }
      if(fishes[i].x() >= 1)
      {
        //if the tile to the left is not an enemy cove and there is no trash
        if(getTile(x - 1,y).owner() != enemyAI_ID &&
           getTile(x - 1,y).trashAmount() == 0)
        {
          //if the tile to the left does not have a fish and does not have an
          //egg
          if(getFishIndex(x - 1, y) == -1 &&
             getTile(x - 1, y).hasEgg() == false)
          {
            //move to the left
            fishes[i].move(x - 1, y);
          }
        }
        //get the fish to the left
        int target = getFishIndex(x - 1, y);
        //if there is a fish to the left and the fish has attacks left
        if(target != -1 && fishes[i].attacksLeft() > 0)
        {
          //if the fish is not a cleaner shrimp
          if(fishes[i].species() != CLEANER_SHRIMP)
          {
            //if the fish to the left is an enemy fish
            if(fishes[target].owner() == enemyAI_ID)
            {
               //attack the fish
               fishes[i].attack(fishes[target]);
            }
          }
          else
          {
             //this is if the fish is a cleaner shrimp

             //if the fish to the left is a friendly fish
             if(fishes[target].owner() != enemyAI_ID)
             {
                //heal the fish
                fishes[i].attack(fishes[target]);
             }
          }
        }
      }
    }
  }
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}
