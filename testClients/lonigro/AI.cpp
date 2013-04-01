#include "AI.h"
#include "util.h"

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

//This function is run once, before your first turn.
void AI::init(){}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
   //spawns fish
   for(int i=0;i<species.size();i++)
   {
      if(species[i].season() == currentSeason() &&
         species[i].carryCap() > 0)
      {
         for(int p=0;p<tiles.size();p++)
         {
            if(tiles[p].hasEgg()==false && tiles[p].trashAmount()== 0)
            {
               species[i].spawn(tiles[p].x(),tiles[p].y());
            }
            
         }
      }
   }
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}
