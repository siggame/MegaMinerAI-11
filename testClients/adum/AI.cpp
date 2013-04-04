#include "AI.h"
#include "util.h"

#include <cstdlib>

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

int findTrashY(std::vector<Tile>& tiles,int mapWidth,int mapHeight)
{
   int y=255;
   for(int i=rand()%mapHeight;y == 255;i=rand()%mapHeight)
   {
      std::cout<<"i: "<<i<<std::endl;
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
      }
   }
   return y;
}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
   //spawn da fish
   for(int i=0;i<species.size();i++)
   {
      if(species[i].season() == currentSeason() &&
         species[i].carryCap() > 0 &&
         species[i].cost() < players[playerID()].spawnFood())
      {
         for(int p=0;p<tiles.size();p++)
         {
            if(tiles[p].hasEgg()==false)
            {
               species[i].spawn(tiles[p].x(),tiles[p].y());
            }
         }
      }
   }


   //be a slave driver to da fish
   for(int i=0;i<fishes.size();i++)
   {
      int y=findTrashY(tiles,mapWidth(),mapHeight());
      for(int p=0;p<fishes[i].movementLeft();p++)
      {
         if(fishes[i].owner() == playerID())
         {
            if(fishes[i].carryingWeight()==0 && fishes[i].y()!=y)
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
               //hahaha this code
               if(fishes[i].move(fishes[i].x() + xChange,fishes[i].y()));
               else if(fishes[i].move(fishes[i].x(),fishes[i].y() - 1));
               else(fishes[i].move(fishes[i].x(),fishes[i].y() + 1));
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
