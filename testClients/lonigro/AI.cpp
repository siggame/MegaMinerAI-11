#include "AI.h"
#include "util.h"

#include <cstdlib>

AI::AI(Connection* conn) : BaseAI(conn) {}

enum AI::speciesIndex { SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH };


const char* AI::username()
{
  return "Anthony";
}

const char* AI::password()
{
  return "password";
}

int enemyAI_ID;

//This function is run once, before your first turn.
void AI::init()
{
  //Determines which player you are
  if(playerID() == 0)
  {
    enemyAI_ID = 1;
  }
  else
  {
    enemyAI_ID = 0;
  }
}

//Function to get the tile in front of you
Tile& getTile(int x,int y,int mapHeight,std::vector<Tile>& tiles)
{
  return tiles[x * mapHeight + y];
}

//Puts the species in order
int getSpecies(int speciesNum,std::vector<Species>& species)
{
  for(int i = 0;i < species.size();i++)
  {
    if(species[i].index() == speciesNum)
    {
      return i;
    }
  }
}

Fish* getFish(int x,int y,std::vector<Fish>& fishes)
{
  for(int i = 0;i < fishes.size(); i++)
  {
    if(fishes[i].x() == x && fishes[i].y() == y)
    {
      return &fishes[i];
    }
  }
  return NULL;
}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  Fish* coolFish = getFish(0, 0, fishes);
  if(coolFish != NULL)
  {
    coolFish->carryingWeight();
  }
  for(int i = 0;i < tiles.size();i++)
  {
    if(tiles[i].owner() == playerID() &&
       getFish(tiles[i].x(), tiles[i].y(), fishes) == NULL)
    {
      for(int p = 0;p<species.size(); p++)
      {
        if(species[p].season() == currentSeason())
        {
          if(players[playerID()].spawnFood() >= species[p].cost() &&
             tiles[i].hasEgg() == false)
          {
            species[p].spawn(tiles[i].x(), tiles[i].y());
          }
        }
      }
    }
  }
  for(int i = 0;i < fishes.size();i++)
  {
    if(fishes[i].owner() == playerID())
    {
      int x = fishes[i].x();
      int y = fishes[i].y();
      if(fishes[i].x() >= 1)
      {
        if(getTile(x - 1, y, mapHeight(), tiles).trashAmount() > 0 &&
           fishes[i].carryingWeight() + 1 <= fishes[i].carryCap())
        {
          fishes[i].pickUp(x - 1, y, 1);
        }
      }
      if(fishes[i].carryingWeight() > 0)
      {
        if(fishes[i].x() < mapWidth()/2 - boundLength() - 1)
        {
          if(fishes[i].y() != 0)
          {
            if(getTile(x,y - 1,mapHeight(),tiles).owner() == 2 &&
               getFish(x,y + 1,fishes) == NULL)
            {
              fishes[i].drop(x, y - 1, fishes[i].carryingWeight());
            }
          }
          else
          {
            if(getTile(x,y + 1,mapHeight(),tiles).owner() == 2 &&
               getFish(x,y + 1,fishes) == NULL)
            {
              fishes[i].drop(x, y + 1, fishes[i].carryingWeight());
            }
          }
        }
      }
      if(fishes[i].x() >= 1)
      {
        if(getTile(x - 1,y,mapHeight(),tiles).owner() != enemyAI_ID &&
           getTile(x - 1,y,mapHeight(),tiles).trashAmount() == 0)
        {
          if(getFish(x - 1, y, fishes) == NULL &&
             getTile(x - 1, y, mapHeight(), tiles).hasEgg() == false)
          {
            fishes[i].move(x - 1,y);
          }
        }
      }
    }
  }
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}
