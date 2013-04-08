#include "AI.h"
#include "util.h"

#include <cstdlib>

enum AI::speciesIndex { SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH };

AI::AI(Connection* conn) : BaseAI(conn) {}

const char* AI::username()
{
   return "Want to go bowling?";
}

const char* AI::password()
{
   return "password";
}

int xChange;

//This function is run once, before your first turn.
void AI::init()
{
   if(playerID() == 0)
   {
      xChange = 1;
   }
   else
   {
      xChange = -1;
   }
}

Fish* getFish(int x,int y,std::vector<Fish>& fishes)
{
   for(int i=0;i<fishes.size();i++)
   {
      if(fishes[i].x() == x &&
         fishes[i].y() == y)
      {
         return &fishes[i];
      }
   }
   return NULL;
}

void findTrashYX(std::vector<Tile>& tiles,int mapWidth,int mapHeight,int& x,int& y)
{
   bool cool = false;
   for(int p = 0; p <123 ; p++)
   {
      int i = rand()%mapHeight;
      int garbage=0;
      if(xChange == 1)
      {
         for(int p=0;p<mapWidth/2;p++)
         {
            garbage += tiles[p*mapHeight + i].trashAmount();
         }
      }
      else
      {
         for(int p=mapWidth/2;p<mapWidth;p++)
         {
            garbage += tiles[p*mapHeight + i].trashAmount();
         }
      }
      if(garbage > 0)
      {
         y=tiles[i].y();
         x=tiles[i].x();
         cool = true;
      }
   }
   if(!cool)
   {
      x=0;
      y=0;
   }
   return;
}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
   Species* toSpawn = NULL;
   //spawn da fish
   for(int i=0;i<species.size();i++)
   {
      if(species[i].season() == currentSeason() &&
         species[i].carryCap() > 0)
      {
         if(species[i].index() != CUTTLEFISH)
         {
            if(toSpawn == NULL)
            {
               toSpawn = &species[i];
            }
            else if(toSpawn->maxMovement() * toSpawn->carryCap() <
                    species[i].maxMovement() * species[i].carryCap())
            {
               toSpawn = &species[i];
            }
         }
      }
   }

   if(toSpawn != NULL)
   {
      for(int p=0;p<tiles.size();p++)
      {
         if(tiles[p].hasEgg()==false &&
            toSpawn->cost() < players[playerID()].spawnFood())
         {
            toSpawn->spawn(tiles[p].x(),tiles[p].y());
         }
      }
   }


   //be a slave driver to da fish
   for(int i=0;i<fishes.size();i++)
   {
      int y,x;
      findTrashYX(tiles,mapWidth(),mapHeight(),x,y);
      for(int p=0;p<fishes[i].movementLeft();p++)
      {
         std::cout<<i<<std::endl;
         std::cout<<fishes[i].x()<<std::endl;
         if(fishes[i].owner() == playerID())
         {
            if(fishes[i].carryingWeight()==0 && fishes[i].y()!=y)
            {
               fishes[i].pickUp(fishes[i].x()+1,fishes[i].y(),1);
               fishes[i].pickUp(fishes[i].x()-1,fishes[i].y(),1);
               if(y>fishes[i].y())
               {
                  if(fishes[i].move(fishes[i].x(),fishes[i].y()+1));
                  else(fishes[i].move(fishes[i].x()+xChange,fishes[i].y()));
               }
               else
               {
                  if(fishes[i].move(fishes[i].x(),fishes[i].y()-1));
                  else(fishes[i].move(fishes[i].x()+xChange,fishes[i].y()));
               }
            }
            else
            {
               int crap;
               if(fishes[i].y()!=mapHeight()-1)
               {
                  crap=tiles[fishes[i].x()*mapHeight()+fishes[i].y()+1].trashAmount();
                  if(crap > fishes[i].carryCap())
                  {
                     crap = fishes[i].carryCap();
                  }
                  if(crap > 0)
                  {
                     fishes[i].pickUp(fishes[i].x(),fishes[i].y()+1,crap);
                  }
               }
               if(fishes[i].y()!=0)
               {
                  crap=tiles[fishes[i].x()*mapHeight()+fishes[i].y()-1].trashAmount();
                  if(crap > fishes[i].carryCap())
                  {
                     crap = fishes[i].carryCap();
                  }
                  if(crap > 0)
                  {
                     fishes[i].pickUp(fishes[i].x(),fishes[i].y()-1,crap);
                  }
               }
               if(fishes[i].x()!=0 && fishes[i].x()!=mapWidth()-1)
               {
                  crap=tiles[(fishes[i].x()+xChange)*mapHeight()+fishes[i].y()].trashAmount();
                  if(crap > fishes[i].carryCap())
                  {
                     crap = fishes[i].carryCap();
                  }
                  if(crap > 0)
                  {
                     fishes[i].pickUp(fishes[i].x()+xChange,fishes[i].y(),crap);
                  }
               }
               if(fishes[i].carryingWeight() == 0)
               {
                  if(fishes[i].x() < x)
                  {
                     fishes[i].move(fishes[i].x() + 1,fishes[i].y());
                  }
                  else
                  {
                     fishes[i].move(fishes[i].x() - 1,fishes[i].y());
                  }
               }
               else
               {
                  //hahaha this code
                  if(fishes[i].move(fishes[i].x() + xChange,fishes[i].y()));
                  else if(fishes[i].move(fishes[i].x(),fishes[i].y() - 1));
                  else(fishes[i].move(fishes[i].x(),fishes[i].y() + 1));
               }
            }

            Fish* target=getFish(fishes[i].x()+xChange,fishes[i].y(),fishes);
            if(target!=NULL)
            {
               fishes[i].attack(*target);
            }
            if(xChange == 1)
            {
               if(fishes[i].x() > mapWidth()/2+boundLength()+2)
               {
                  if(fishes[i].drop(fishes[i].x()-1,fishes[i].y(),fishes[i].carryingWeight()));
                  else if(fishes[i].drop(fishes[i].x(),fishes[i].y()-1,fishes[i].carryingWeight()));
                  else if(fishes[i].drop(fishes[i].x(),fishes[i].y()+1,fishes[i].carryingWeight()));
               }
            }
            else
            {
               if(fishes[i].x() < mapWidth()/2-boundLength()-2)
               {
                  if(fishes[i].drop(fishes[i].x()+1,fishes[i].y(),fishes[i].carryingWeight()));
                  else if(fishes[i].drop(fishes[i].x(),fishes[i].y()-1,fishes[i].carryingWeight()));
                  else if(fishes[i].drop(fishes[i].x(),fishes[i].y()+1,fishes[i].carryingWeight()));
               }
            }
         }
      }
   }
   return true;
}

//This function is run once, after your last turn.
void AI::end()
{
}
