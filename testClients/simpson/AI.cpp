#include "AI.h"
#include "util.h"
#include <iostream>
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

//void adjacentPickUp

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  int bogus;
  
  //attempting to spawn a fish on every single tile in the grid
  for(int i = 0; i < mapWidth(); i++)
  {
    for(int j = 0; j < mapHeight(); j++)
    {
      for(int k = 0; k < species.size(); k++) //size_t?
      {
        if(species[k].cost() <= players[playerID()].spawnFood())
        {
          species[k].spawn(i,j);
        }
      }
    }
  }
  for(int i = 0; i < fishes.size(); i++)
  {
    bogus = fishes[i].carryCap() - fishes[i].carryingWeight();
    //attempting to move the fish to a non adjacent tile
    fishes[i].move((fishes[i].x()+2),(fishes[i].y()+2));      
    
    /*attempting to move the fish off the map in every direction and picking
             up everywhere. Also tries to drop a bogus amount on a tile*/
    for(int k = 0; k < mapWidth(); k++)
    {
      fishes[i].move((fishes[i].x() + 1),fishes[i].y());
      fishes[i].pickUp(fishes[i].x(),(fishes[i].y()-1),5);
      fishes[i].pickUp((fishes[i].x()+1),(fishes[i].y()-1),5);
      fishes[i].pickUp((fishes[i].x()+1),fishes[i].y(),5);
      fishes[i].pickUp((fishes[i].x()+1),(fishes[i].y()+1),5);
      fishes[i].pickUp(fishes[i].x(),(fishes[i].y()+1),5);
      fishes[i].pickUp((fishes[i].x()-1),(fishes[i].y()+1),5);
      fishes[i].pickUp((fishes[i].x()-1),fishes[i].y(),5);
      fishes[i].pickUp((fishes[i].x()-1),(fishes[i].y()-1),5);
      fishes[i].drop(fishes[i].x(),(fishes[i].y()+1),bogus);
    }/*
    for(int k = 0; k < mapWidth(); k++)
    {
      fishes[i].move((fishes[i].x() - 1),fishes[i].y());
      fishes[i].pickUp(fishes[i].x(),(fishes[i].y()-1),5);
      fishes[i].pickUp((fishes[i].x()+1),(fishes[i].y()-1),5);
      fishes[i].pickUp((fishes[i].x()+1),fishes[i].y(),5);
      fishes[i].pickUp((fishes[i].x()+1),(fishes[i].y()+1),5);
      fishes[i].pickUp(fishes[i].x(),(fishes[i].y()+1),5);
      fishes[i].pickUp((fishes[i].x()-1),(fishes[i].y()+1),5);
      fishes[i].pickUp((fishes[i].x()-1),fishes[i].y(),5);
      fishes[i].pickUp((fishes[i].x()-1),(fishes[i].y()-1),5);
      fishes[i].drop(fishes[i].x(),(fishes[i].y()+1),bogus);
    }
    for(int k = 0; k < mapWidth(); k++)
    {
      fishes[i].move(fishes[i].x(),(fishes[i].y() + 1));
      fishes[i].pickUp(fishes[i].x(),(fishes[i].y()-1),5);
      fishes[i].pickUp((fishes[i].x()+1),(fishes[i].y()-1),5);
      fishes[i].pickUp((fishes[i].x()+1),fishes[i].y(),5);
      fishes[i].pickUp((fishes[i].x()+1),(fishes[i].y()+1),5);
      fishes[i].pickUp(fishes[i].x(),(fishes[i].y()+1),5);
      fishes[i].pickUp((fishes[i].x()-1),(fishes[i].y()+1),5);
      fishes[i].pickUp((fishes[i].x()-1),fishes[i].y(),5);
      fishes[i].pickUp((fishes[i].x()-1),(fishes[i].y()-1),5);
      fishes[i].drop(fishes[i].x(),(fishes[i].y()+1),bogus);
    }
    for(int k = 0; k < mapWidth(); k++)
    {
      fishes[i].move(fishes[i].x(),(fishes[i].y() - 1));
      fishes[i].pickUp(fishes[i].x(),(fishes[i].y()-1),5);
      fishes[i].pickUp((fishes[i].x()+1),(fishes[i].y()-1),5);
      fishes[i].pickUp((fishes[i].x()+1),fishes[i].y(),5);
      fishes[i].pickUp((fishes[i].x()+1),(fishes[i].y()+1),5);
      fishes[i].pickUp(fishes[i].x(),(fishes[i].y()+1),5);
      fishes[i].pickUp((fishes[i].x()-1),(fishes[i].y()+1),5);
      fishes[i].pickUp((fishes[i].x()-1),fishes[i].y(),5);
      fishes[i].pickUp((fishes[i].x()-1),(fishes[i].y()-1),5);
      fishes[i].drop(fishes[i].x(),(fishes[i].y()+1),bogus);
    }
  }*/
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}
