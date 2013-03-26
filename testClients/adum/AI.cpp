#include "AI.h"
#include "util.h"

AI::AI(Connection* conn) : BaseAI(conn) {}

const char* AI::username()
{
   return "Want to go bowling?";
}

const char* AI::password()
{
   return "password";
}

//This function is run once, before your first turn.
void AI::init(){}

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

int findTrashY(std::vector<Tile>& tiles,int mapWidth)
{
   int y=255;
   for(int i=0;i<tiles.size();i++)
   {
      if(tiles[i].trashAmount() > 0 && tiles[i].y()<y && tiles[i].x()<mapWidth/2)
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
         species[i].carryCap() > 0)
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
      int y=findTrashY(tiles,mapWidth());
      for(int i=0;i<fishes[i].movementLeft();i++)
      {
         if(fishes[i].carryingWeight()==0 && fishes[i].y()!=y)
         {
            if(y>fishes[i].y())
            {
               fishes[i].move(fishes[i].x(),fishes[i].y()+1);
               fishes[i].pickUp(fishes[i].x(),fishes[i].y()+1,1);
            }
            else
            {
               fishes[i].move(fishes[i].x(),fishes[i].y()-1);
               fishes[i].pickUp(fishes[i].x(),fishes[i].y()-1,1);
            }
         }
         else
         {
            fishes[i].move(fishes[i].x()+1,fishes[i].y());
         }

         fishes[i].pickUp(fishes[i].x()+1,fishes[i].y(),1);
         /*
         Fish* target=getFish(fishes[i].x()+1,fishes[i].y(),fishes);
         if(target!=NULL)
         {
            fishes[i].attack(*target);
         }
         */
         if(fishes[i].x() > mapWidth()/2+boundLength())
         {
            fishes[i].drop(fishes[i].x()+1,fishes[i].y(),1);
         }
      }
   }

   //how wealthy I am by fish
   std::cout<<"Fishes: "<<fishes.size()<<"\n";
   return true;
}

//This function is run once, after your last turn.
void AI::end()
{
}
