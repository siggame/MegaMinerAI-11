#include "AI.h"
#include "util.h"

#include <cstdlib>
#include <memory.h>
#include <ctype.h>
#include <stdio.h>
#include <memory.h>
#include <math.h>

#include <vector>
#include <iostream>

std::vector<Tile*> MAI_COVEZ;
std::vector<Tile*> wallz;

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
   for(int i=0;i<tiles.size();i++)
   {
      if(tiles[i].owner() == playerID())
      {
         MAI_COVEZ.push_back(&tiles[i]);
      }
      if(tiles[i].owner() == 3 ||
         tiles[i].owner() == 1-playerID())
      {
         wallz.push_back(&tiles[i]);
      }
   }
}

struct point
{
   int x;
   int y;
   point(int x,int y):x(x),y(y){}
};

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

//x = can't walk
/*void findPath(int startX,int startY,int endX,int endY,char map2[],
              std::vector<point>& path)
{
   char map[20*40];
   for(int i=0;i<20*40;i++)
   {
      map2[i]=map[i];
   }
   int x = startX, y = startY;
   path.push_back(point(x+1,y));
   while(x != endX && y != endY)
   {
      if(map[(x+1)*40 + y] != 'x')
      {
         path.push_back(point(x+1,y));
         x++;
      }
         else
         {
            map[x*40 + y] = 'x';
            x = path.end()->x;
            y = path.end()->y;
            path.pop_back();
         }
      }
      else if(x>endX)
      {
         if(map[(x-1)*40 + y] != 'x')
         {
            path.push_back(point(x-1,y));
            x--;
         }
         else
         {
            map[x*40 + y] = 'x';
            x = path.end()->x;
            y = path.end()->y;
            path.pop_back();
         }
      }
      else if (y<endY)
      {
         if(map[x*40 + y + 1]!='x')
         {
            path.push_back(point(x,y+1));
            y++;
         }
         else
         {
            map[x*40 + y] = 'x';
            x = path.end()->x;
            y = path.end()->y;
            path.pop_back();
         }
      }
      else if (y>endY)
      {
         if(map[x*40 + y - 1]!='x')
         {
            path.push_back(point(x,y-1));
            y--;
         }
         else
         {
            map[x*40 + y] = 'x';
            x = path.end()->x;
            y = path.end()->y;
            path.pop_back();
         }
      }
      if(x == startX && y == startY)
      {
         return;
      }
   }
}*/

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
   char map[40*20];
   bool claimed[40*20];
   //BuildMapArray();
   //std::vector<VECTOR2D> yoyoyo;
   Species* toSpawn = NULL;
   //spawn da fish
   for(int i=0;i<speciesList.size();i++)
   {
      if(speciesList[i].season() == currentSeason() &&
         speciesList[i].carryCap() > 0)
      {
         if(toSpawn == NULL)
         {
            toSpawn = &speciesList[i];
         }
         else if(toSpawn->maxMovement() * toSpawn->carryCap() <
                 speciesList[i].maxMovement() * speciesList[i].carryCap())
         {
            toSpawn = &speciesList[i];
         }
      }
   }

   if(toSpawn != NULL)
   {
      for(int p=0;p<MAI_COVEZ.size();p++)
      {
         if(MAI_COVEZ[p]->hasEgg()==false &&
            toSpawn->cost() < players[playerID()].spawnFood() &&
            MAI_COVEZ[p]->owner() == playerID())
         {
            toSpawn->spawn(getTile(MAI_COVEZ[p]->x(),MAI_COVEZ[p]->y()));
         }
      }
   }

   //make a map
   for(int i=0;i<wallz.size();i++)
   {
      map[wallz[i]->x() + wallz[i]->y()*mapWidth()]='x';
   }
   for(int i=0;i<fishes.size();i++)
   {
      map[fishes[i].x() + fishes[i].y()*mapWidth()]='x';
   }

   //be a slave driver to da fish
   for(int i=0;i<fishes.size();i++)
   {
      std::vector<point> path;
      int y,x;
      findTrashYX(tiles,mapWidth(),mapHeight(),x,y);
      if(fishes[i].owner() == playerID())
      {
         //findPath(fishes[i].x(),fishes[i].y(),0,0,map,path);
         for(int p=0;p<fishes[i].movementLeft();p++)
         {
            //fishes[i].move(path[i+1].x,path[i+1].y);

            if(fishes[i].carryingWeight()==0 && fishes[i].y()!=y)
            {
               if(x > 0 && x < mapWidth() - 1)
               {
                  fishes[i].pickUp(getTile(fishes[i].x()+1,fishes[i].y()),1);
                  fishes[i].pickUp(getTile(fishes[i].x()-1,fishes[i].y()),1);
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
                     fishes[i].pickUp(getTile(fishes[i].x(),fishes[i].y()+1),crap);
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
                     fishes[i].pickUp(getTile(fishes[i].x(),fishes[i].y()-1),crap);
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
                     fishes[i].pickUp(getTile(fishes[i].x()+xChange,fishes[i].y()),crap);
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

            Fish* target=getFish(fishes[i].x()+xChange,fishes[i].y());
            if(target!=NULL)
            {
               fishes[i].attack(*target);
            }
            if(xChange == 1)
            {
               if(fishes[i].x() > mapWidth()/2+boundLength()+2)
               {
                  if(fishes[i].drop(getTile(fishes[i].x()-1,fishes[i].y()),fishes[i].carryingWeight()));
                  else if(fishes[i].drop(getTile(fishes[i].x(),fishes[i].y()-1),fishes[i].carryingWeight()));
                  else if(fishes[i].drop(getTile(fishes[i].x(),fishes[i].y()+1),fishes[i].carryingWeight()));
               }
            }
            else
            {
               if(fishes[i].x() < mapWidth()/2-boundLength()-2)
               {
                  if(fishes[i].drop(getTile(fishes[i].x()+1,fishes[i].y()),fishes[i].carryingWeight()));
                  else if(fishes[i].drop(getTile(fishes[i].x(),fishes[i].y()-1),fishes[i].carryingWeight()));
                  else if(fishes[i].drop(getTile(fishes[i].x(),fishes[i].y()+1),fishes[i].carryingWeight()));
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
