#include "AI.h"
#include "util.h"
#include <iostream>
#include <cmath>
using namespace std;

AI::AI(Connection* conn) : BaseAI(conn) {}

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

Tile AI::myGetTile(const int x, const int y)
{
  return tiles[x*mapHeight() + y];
}

Fish AI::myGetFish(const int targetX, const int targetY)
{
  for(int i = 0; i < fishes.size(); i++)
  {
    if(fishes[i].x() == targetX && fishes[i].y() == targetY)
    {
      return fishes[i];
    }
  }
}

bool AI::findPath(const int beginX,const int beginY,const int endX,const int endY,
              Fish & f)
{
  int currentX = beginX;
  int currentY = beginY;
  for(int i = 0; i < 4; i++) //4 choices
  {
    switch(i)
    {
      case 0: //NORTH
        currentY--;
        break;
      
      case 1: //EAST
        currentX++;
        break;
        
      case 2: //SOUTH
        currentY++;
        break;
        
      case 3: //WEST
        currentX--;
        break;
    }
    if(myGetTile(currentX,currentY).hasEgg()) //invalid if egg
    {
      return false;
    }
    for(int j = 0; j < fishes.size(); j++)
    {
      if(fishes[j].x() == currentX && fishes[j].y() == currentY) //invalid if fish
      {
        return false;
      }
    }
    if(myGetTile(currentX,currentY).trashAmount() > 0) //invalid if trash
    {
      return false;
    }
    if(myGetTile(currentX,currentY).owner() != 2) //invalid if cove
    {
      return false;
    }
    if(currentX == endX && currentY == endY) //success!
    {
      f.move(currentX,currentY);
      return true;
    }
    else
    {
      f.move(currentX,currentY);
      findPath(currentX,currentY,endX,endY,f);
    }
  }
  return false;
}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
	int myX = -1,myY = -1,enemyX = -1, enemyY = -1, count = 0;
  bool bob;
  
	for(int i = 0; i < tiles.size(); i++) //spawn fish
	{
		if(tiles[i].owner() == playerID()) //find my cove
		{
			for(int k = 0; k < species.size(); k++)
			{
				if(species[k].cost() <= players[playerID()].spawnFood() && 
				   species[k].season() == currentSeason())
				{
					species[k].spawn(tiles[i].x(),tiles[i].y());
				}
			}
		}
	}
  
	//moves to the right/left, attacking any enemy fish
  for(int i = 0; i < fishes.size(); i++)
  {
    if(fishes[i].owner() == playerID())
    {
      while(fishes[i].movementLeft() > 0)
      {
        if(playerID() == 0)
          bob = true;
        else
          bob = false;
        //move right if player 1 else move left
        if(bob)
        {
          fishes[i].move(fishes[i].x()+1,fishes[i].y());
          //attack if fish
          for(int j = 0; j < fishes.size(); j++)
          {
            if(fishes[j].x() == fishes[i].x()+1 && fishes[j].y() == fishes[i].y())
              fishes[i].attack(fishes[j]);
          }
        }
        else
        {
          fishes[i].move(fishes[i].x()-1,fishes[i].y());
          //attack if fish
          for(int j = 0; j < fishes.size(); j++)
          {
            if(fishes[j].x() == fishes[i].x()-1 && fishes[j].y() == fishes[i].y())
              fishes[i].attack(fishes[j]);
          }
        }
      }
    }
  }
  
  /*do //find some enemy fish
  {
    if(fishes[count].owner != playerID())
    {
      enemyX = fishes[count].x();
      enemyY = fishes[count].y();
    }
    count++;
  }while(enemyX == -1 && enemyY == -1 && count < fishes.size());
  
  for(int i = 0; i < fishes.size(); i++)    //command one of my fish
  {
    if(fishes[i].owner() == playerID())
    {
      myX = fishes[i].x();
      myY = fishes[i].y();
    }
    findPath(myX,myY,(enemyX-1),enemyY,fishes[i]);
    fishes[i].attack(myGetFish(enemyX,enemyY));
  }*/
	
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}
