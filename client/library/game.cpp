//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#pragma warning(disable : 4996)

#include <string>
#include <cstring>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <fstream>
#include <memory>

#include "game.h"
#include "network.h"
#include "structures.h"

#include "sexp/sfcompat.h"

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

#ifdef _WIN32
//Doh, namespace collision.
namespace Windows
{
    #include <Windows.h>
};
#else
#include <unistd.h>
#endif

#ifdef ENABLE_THREADS
#define LOCK(X) pthread_mutex_lock(X)
#define UNLOCK(X) pthread_mutex_unlock(X)
#else
#define LOCK(X)
#define UNLOCK(X)
#endif

using std::cout;
using std::cerr;
using std::endl;
using std::stringstream;
using std::string;
using std::ofstream;

DLLEXPORT Connection* createConnection()
{
  Connection* c = new Connection;
  c->socket = -1;
  #ifdef ENABLE_THREADS
  pthread_mutex_init(&c->mutex, NULL);
  #endif

  c->maxReefHealth = 0;
  c->boundLength = 0;
  c->turnNumber = 0;
  c->playerID = 0;
  c->gameNumber = 0;
  c->mapWidth = 0;
  c->mapHeight = 0;
  c->trashAmount = 0;
  c->currentSeason = 0;
  c->seasonLength = 0;
  c->healPercent = 0;
  c->maxFood = 0;
  c->Mappables = NULL;
  c->MappableCount = 0;
  c->Tiles = NULL;
  c->TileCount = 0;
  c->SpeciesList = NULL;
  c->SpeciesCount = 0;
  c->Fishes = NULL;
  c->FishCount = 0;
  c->Players = NULL;
  c->PlayerCount = 0;
  return c;
}

DLLEXPORT void destroyConnection(Connection* c)
{
  #ifdef ENABLE_THREADS
  pthread_mutex_destroy(&c->mutex);
  #endif
  if(c->Mappables)
  {
    for(int i = 0; i < c->MappableCount; i++)
    {
    }
    delete[] c->Mappables;
  }
  if(c->Tiles)
  {
    for(int i = 0; i < c->TileCount; i++)
    {
    }
    delete[] c->Tiles;
  }
  if(c->SpeciesList)
  {
    for(int i = 0; i < c->SpeciesCount; i++)
    {
      delete[] c->SpeciesList[i].name;
    }
    delete[] c->SpeciesList;
  }
  if(c->Fishes)
  {
    for(int i = 0; i < c->FishCount; i++)
    {
    }
    delete[] c->Fishes;
  }
  if(c->Players)
  {
    for(int i = 0; i < c->PlayerCount; i++)
    {
      delete[] c->Players[i].playerName;
    }
    delete[] c->Players;
  }
  delete c;
}

DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port)
{
  c->socket = open_server_connection(host, port);
  return c->socket + 1; //false if socket == -1
}

DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password)
{
  string expr = "(login \"";
  expr += username;
  expr += "\" \"";
  expr += password;
  expr +="\")";

  send_string(c->socket, expr.c_str());

  sexp_t* expression, *message;

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  message = expression->list;
  if(message->val == NULL || strcmp(message->val, "login-accepted") != 0)
  {
    cerr << "Unable to login to server" << endl;
    destroy_sexp(expression);
    return 0;
  }
  destroy_sexp(expression);
  return 1;
}

DLLEXPORT int createGame(Connection* c)
{
  sexp_t* expression, *number;

  send_string(c->socket, "(create-game)");

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  number = expression->list->next;
  c->gameNumber = atoi(number->val);
  destroy_sexp(expression);

  std::cout << "Creating game " << c->gameNumber << endl;

  c->playerID = 0;

  return c->gameNumber;
}

DLLEXPORT int joinGame(Connection* c, int gameNum, const char* playerType)
{
  sexp_t* expression;
  stringstream expr;

  c->gameNumber = gameNum;

  expr << "(join-game " << c->gameNumber << " "<< playerType << ")";
  send_string(c->socket, expr.str().c_str());

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  if(strcmp(expression->list->val, "join-accepted") == 0)
  {
    destroy_sexp(expression);
    c->playerID = 1;
    send_string(c->socket, "(game-start)");
    return 1;
  }
  else if(strcmp(expression->list->val, "create-game") == 0)
  {
    std::cout << "Game did not exist, creating game " << c->gameNumber << endl;
    destroy_sexp(expression);
    c->playerID = 0;
    return 1;
  }
  else
  {
    cerr << "Cannot join game "<< c->gameNumber << ": " << expression->list->next->val << endl;
    destroy_sexp(expression);
    return 0;
  }
}

DLLEXPORT void endTurn(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(end-turn)");
  UNLOCK( &c->mutex );
}

DLLEXPORT void getStatus(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(game-status)");
  UNLOCK( &c->mutex );
}




DLLEXPORT int speciesSpawn(_Species* object, _Tile* tile)
{
  stringstream expr;
  expr << "(game-spawn " << object->id
      << " " << tile->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);

  Connection * c = object->_c;

  //must have enough food
  if(c->Players[c->playerID].spawnFood < object->cost)
  {
    return 0;
  }
  //needs to be in season
  if(c->currentSeason != object->season)
  {
    return 0;
  }
  //tile has to be owned by the owner
  if(tile->owner != c->playerID)
  {
    return 0;
  }
  //tile can't have an egg
  if(tile->hasEgg)
  {
    return 0;
  }

  c->Players[c->playerID].spawnFood -= object->cost;
  tile->hasEgg = true;
  //I don't think this is needed; it does not work either way though
  //tile->species = object;

  return 1;
}


DLLEXPORT int fishMove(_Fish* object, int x, int y)
{
  stringstream expr;
  expr << "(game-move " << object->id
       << " " << x
       << " " << y
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);

  Connection * c = object->_c;
  //Cannot move a fish you do not own.
  if(object->owner != c->playerID) {
    return 0;
  }
  //Cannot move if there is no movement left.
  else if(object->movementLeft <= 0) {
   return 0;
  }
  //Cannot move out of bounds
  else if( (x<0 || x>=c->mapWidth) || (y<0 || y>=c->mapHeight) ) {
    return 0;
  }
  //Cannot move more than one space away at a time
  else if(abs(object->x-x) + abs(object->y-y) != 1) {
   return 0;
  }
  //Do not move on top of another fish.
  for(int ii = 0; ii < c->FishCount; ii++) {
    if (c->Fishes[ii].x == x && c->Fishes[ii].y == y) {
     return 0;
    }
  }
  //Do not move on top of trash (tile with trash amount > 0) with size.
  if(c->Tiles[x*c->mapHeight + y].trashAmount > 0)
  {
    return 0;
  }
  //Do not move on top of the enemy's cove
  if(c->Tiles[x*c->mapHeight +y].owner == abs(c->playerID - 1)) {
    return 0;
  }
  //Do not move on top of a wall
  if(c->Tiles[x*c->mapHeight +y].owner == 3){
    return 0;
  }

  //Decrement movement
  object->movementLeft = object->movementLeft-1;

  //Apply new movement
  object->x = x;
  object->y = y;

  return 1;
}

DLLEXPORT int fishPickUp(_Fish* object, _Tile* tile, int weight)
{
  stringstream expr;
  expr << "(game-pick-up " << object->id
      << " " << tile->id
       << " " << weight
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);

  Connection * c = object->_c;
  //can't control enemy fish
  if(object -> owner != c->playerID)
  {
    return 0;
  }
  //can only pickup from adjacent tiles
  else if(abs(object->x - tile->x) + abs(object->y - tile->y) != 1)
  {
   return 0;
  }
  //cannot carry more than the fish's carrying capacity
  else if( (object->carryingWeight + weight) > object->carryCap )
  {
    return 0;
  }
  //cannot pick up a weight of 0
  else if(weight == 0)
  {
    return 0;
  }
  //cannot pick up something that will kill you
  else if(object->currentHealth < weight)
  {
    return 0;
  }
  //can't pick up more trash than is present
  if(tile->trashAmount < weight)
  {
    return 0;
  }

  if(!object->isVisible)
    object->isVisible = true;

  if(object->species != 6) //Tomcod
    object->currentHealth -= weight;

  tile->trashAmount -= weight;
  object->carryingWeight += weight;

  return 1;
}

DLLEXPORT int fishDrop(_Fish* object, _Tile* tile, int weight)
{
  stringstream expr;
  expr << "(game-drop " << object->id
      << " " << tile->id
       << " " << weight
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);

  Connection * c = object->_c;
  //can't control enemy fish
  if(object -> owner != c->playerID)
  {
    return 0;
  }
  //Cannot drop more than the fish is carrying
  else if(weight > object->carryingWeight)
  {
    return 0;
  }

  //Cannot drop on a fish
  int x = tile->x;
  int y = tile->y;
  for(int i = 0; i < c->FishCount; i++)
  {
    if(x == c->Fishes[i].x &&
       y == c->Fishes[i].y)
    {
       return 0;
    }
  }
  //Make fish visible when dropping
  object->isVisible = true;

  //add weight to tile
  object->carryingWeight -= weight;
  tile->trashAmount += weight;

  return 1;
}

DLLEXPORT int fishAttack(_Fish* object, _Fish* target)
{
  stringstream expr;
  expr << "(game-attack " << object->id
      << " " << target->id
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);

  Connection * c = object->_c;

  //must own fish
  if(object->owner != c->playerID)
  {
    return 0;
  }
  //must be within range
  else if(abs(object->x-target->x)+abs(object->y-target->y) > object->range)
  {
    return 0;
  }
  //must have attacks left
  else if(object->attacksLeft==0)
  {
    return 0;
  }
  //can't attack opponents invisible fish
  else if(target->owner != c->playerID &&
          !target->isVisible)
  {
    return 0;
  }
  //can't heal opponent fish
  else if(target->owner != c->playerID &&
          object->attackPower < 0)
  {
    return 0;
  }
  //can't attack own fish
  else if(target->owner == c->playerID &&
          object->attackPower > 0)
  {
     return 0;
  }
  //can't attack fish on the same tile as yourself
  else if(target->x == object->x &&
          target->y == object->y)
  {
     return 0;
  }

  //Heal if cleanershrimp[]
  if(object->species == 9) //Cleaner Shrimp
  {
    //healed by target->maxHealth*healPercent
    target->currentHealth += target->maxHealth * c->healPercent;
    //Make sure the healed target's health is not greater than its max health
    if(target->currentHealth > target->maxHealth)
    {
      target->currentHealth = target->maxHealth;
    }
    //The healed target should be visible after being healed
    target->isVisible = true;
  }
  else if(object->species == 10) //Electric Eel
  {
    //Stun target (cannot move cannot attack)
    target->movementLeft = -1;
    target->attacksLeft = -1;
  }
  object->attacksLeft -= 1;

  if(target->currentHealth <= 0)
  {
    //add weight to tile where target died
    c->Tiles[target->x * c->mapHeight + target->y].trashAmount += target->carryingWeight;
  }
  //If target is seaurchin and not owned by player
  if(target->species == 4 && target->owner != object->owner) //Sea Urchin
  {
    //Attacking object gets damaged by urchin
    object->currentHealth -= target->attackPower;
    if(object->currentHealth <= 0)
    {
      c->Tiles[object->x * c->mapHeight + object->y].trashAmount += object->carryingWeight;
    }
  }

  return 1;
}


DLLEXPORT int playerTalk(_Player* object, char* message)
{
  stringstream expr;
  expr << "(game-talk " << object->id
      << " \"" << escape_string(message) << "\""
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  return 1;
}


//Utility functions for parsing data
void parseMappable(Connection* c, _Mappable* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;

}
void parseTile(Connection* c, _Tile* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->trashAmount = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->hasEgg = atoi(sub->val);
  sub = sub->next;
  object->damages = atoi(sub->val);
  sub = sub->next;

}
void parseSpecies(Connection* c, _Species* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->name = new char[strlen(sub->val)+1];
  strncpy(object->name, sub->val, strlen(sub->val));
  object->name[strlen(sub->val)] = 0;
  sub = sub->next;
  object->index = atoi(sub->val);
  sub = sub->next;
  object->cost = atoi(sub->val);
  sub = sub->next;
  object->maxHealth = atoi(sub->val);
  sub = sub->next;
  object->maxMovement = atoi(sub->val);
  sub = sub->next;
  object->carryCap = atoi(sub->val);
  sub = sub->next;
  object->attackPower = atoi(sub->val);
  sub = sub->next;
  object->range = atoi(sub->val);
  sub = sub->next;
  object->maxAttacks = atoi(sub->val);
  sub = sub->next;
  object->season = atoi(sub->val);
  sub = sub->next;

}
void parseFish(Connection* c, _Fish* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->maxHealth = atoi(sub->val);
  sub = sub->next;
  object->currentHealth = atoi(sub->val);
  sub = sub->next;
  object->maxMovement = atoi(sub->val);
  sub = sub->next;
  object->movementLeft = atoi(sub->val);
  sub = sub->next;
  object->carryCap = atoi(sub->val);
  sub = sub->next;
  object->carryingWeight = atoi(sub->val);
  sub = sub->next;
  object->attackPower = atoi(sub->val);
  sub = sub->next;
  object->isVisible = atoi(sub->val);
  sub = sub->next;
  object->maxAttacks = atoi(sub->val);
  sub = sub->next;
  object->attacksLeft = atoi(sub->val);
  sub = sub->next;
  object->range = atoi(sub->val);
  sub = sub->next;
  object->species = atoi(sub->val);
  sub = sub->next;

}
void parsePlayer(Connection* c, _Player* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->playerName = new char[strlen(sub->val)+1];
  strncpy(object->playerName, sub->val, strlen(sub->val));
  object->playerName[strlen(sub->val)] = 0;
  sub = sub->next;
  object->time = atof(sub->val);
  sub = sub->next;
  object->currentReefHealth = atoi(sub->val);
  sub = sub->next;
  object->spawnFood = atoi(sub->val);
  sub = sub->next;

}

DLLEXPORT int networkLoop(Connection* c)
{
  while(true)
  {
    sexp_t* base, *expression, *sub, *subsub;

    char* message = rec_string(c->socket);
    string text = message;
    base = extract_sexpr(message);
    delete[] message;
    expression = base->list;
    if(expression->val != NULL && strcmp(expression->val, "game-winner") == 0)
    {
      expression = expression->next->next->next;
      int winnerID = atoi(expression->val);
      if(winnerID == c->playerID)
      {
        cout << "You win!" << endl << expression->next->val << endl;
      }
      else
      {
        cout << "You lose. :(" << endl << expression->next->val << endl;
      }
      stringstream expr;
      expr << "(request-log " << c->gameNumber << ")";
      send_string(c->socket, expr.str().c_str());
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "log") == 0)
    {
      ofstream out;
      stringstream filename;
      expression = expression->next;
      filename << expression->val;
      filename << ".gamelog";
      expression = expression->next;
      out.open(filename.str().c_str());
      if (out.good())
        out.write(expression->val, strlen(expression->val));
      else
        cerr << "Error : Could not create log." << endl;
      out.close();
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "game-accepted")==0)
    {
      char gameID[30];

      expression = expression->next;
      strcpy(gameID, expression->val);
      cout << "Created game " << gameID << endl;
    }
    else if(expression->val != NULL && strstr(expression->val, "denied"))
    {
      cout << expression->val << endl;
      cout << expression->next->val << endl;
    }
    else if(expression->val != NULL && strcmp(expression->val, "status") == 0)
    {
      while(expression->next != NULL)
      {
        expression = expression->next;
        sub = expression->list;
        if(string(sub->val) == "game")
        {
          sub = sub->next;
          c->maxReefHealth = atoi(sub->val);
          sub = sub->next;

          c->boundLength = atoi(sub->val);
          sub = sub->next;

          c->turnNumber = atoi(sub->val);
          sub = sub->next;

          c->playerID = atoi(sub->val);
          sub = sub->next;

          c->gameNumber = atoi(sub->val);
          sub = sub->next;

          c->mapWidth = atoi(sub->val);
          sub = sub->next;

          c->mapHeight = atoi(sub->val);
          sub = sub->next;

          c->trashAmount = atoi(sub->val);
          sub = sub->next;

          c->currentSeason = atoi(sub->val);
          sub = sub->next;

          c->seasonLength = atoi(sub->val);
          sub = sub->next;

          c->healPercent = atoi(sub->val);
          sub = sub->next;

          c->maxFood = atoi(sub->val);
          sub = sub->next;

        }
        else if(string(sub->val) == "Mappable")
        {
          if(c->Mappables)
          {
            for(int i = 0; i < c->MappableCount; i++)
            {
            }
            delete[] c->Mappables;
          }
          c->MappableCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Mappables = new _Mappable[c->MappableCount];
          for(int i = 0; i < c->MappableCount; i++)
          {
            sub = sub->next;
            parseMappable(c, c->Mappables+i, sub);
          }
        }
        else if(string(sub->val) == "Tile")
        {
          if(c->Tiles)
          {
            sub = sub->next;
            for(int i = 0; i < c->TileCount; i++)
            {
              if(!sub)
              {
                break;
              }
              int id = atoi(sub->list->val);
              if(id == c->Tiles[i].id)
              {
                parseTile(c, c->Tiles+i, sub);
                sub = sub->next;
              }
            }
          }
          else
          {
            c->TileCount =  sexp_list_length(expression)-1; //-1 for the header
            c->Tiles = new _Tile[c->TileCount];
            for(int i = 0; i < c->TileCount; i++)
            {
              sub = sub->next;
              parseTile(c, c->Tiles+i, sub);
            }
          }
        }
        else if(string(sub->val) == "Species")
        {
          if(c->SpeciesList)
          {
            sub = sub->next;
            for(int i = 0; i < c->SpeciesCount; i++)
            {
              if(!sub)
              {
                break;
              }
              int id = atoi(sub->list->val);
              if(id == c->SpeciesList[i].id)
              {
                delete[] c->SpeciesList[i].name;
                parseSpecies(c, c->SpeciesList+i, sub);
                sub = sub->next;
              }
            }
          }
          else
          {
            c->SpeciesCount =  sexp_list_length(expression)-1; //-1 for the header
            c->SpeciesList = new _Species[c->SpeciesCount];
            for(int i = 0; i < c->SpeciesCount; i++)
            {
              sub = sub->next;
              parseSpecies(c, c->SpeciesList+i, sub);
            }
          }
        }
        else if(string(sub->val) == "Fish")
        {
          if(c->Fishes)
          {
            for(int i = 0; i < c->FishCount; i++)
            {
            }
            delete[] c->Fishes;
          }
          c->FishCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Fishes = new _Fish[c->FishCount];
          for(int i = 0; i < c->FishCount; i++)
          {
            sub = sub->next;
            parseFish(c, c->Fishes+i, sub);
          }
        }
        else if(string(sub->val) == "Player")
        {
          if(c->Players)
          {
            for(int i = 0; i < c->PlayerCount; i++)
            {
              delete[] c->Players[i].playerName;
            }
            delete[] c->Players;
          }
          c->PlayerCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Players = new _Player[c->PlayerCount];
          for(int i = 0; i < c->PlayerCount; i++)
          {
            sub = sub->next;
            parsePlayer(c, c->Players+i, sub);
          }
        }
      }
      destroy_sexp(base);
      return 1;
    }
    else
    {
#ifdef SHOW_WARNINGS
      cerr << "Unrecognized message: " << text << endl;
#endif
    }
    destroy_sexp(base);
  }
}

DLLEXPORT _Mappable* getMappable(Connection* c, int num)
{
  return c->Mappables + num;
}
DLLEXPORT int getMappableCount(Connection* c)
{
  return c->MappableCount;
}

DLLEXPORT _Tile* getTile(Connection* c, int num)
{
  return c->Tiles + num;
}
DLLEXPORT int getTileCount(Connection* c)
{
  return c->TileCount;
}

DLLEXPORT _Species* getSpecies(Connection* c, int num)
{
  return c->SpeciesList + num;
}
DLLEXPORT int getSpeciesCount(Connection* c)
{
  return c->SpeciesCount;
}

DLLEXPORT _Fish* getFish(Connection* c, int num)
{
  return c->Fishes + num;
}
DLLEXPORT int getFishCount(Connection* c)
{
  return c->FishCount;
}

DLLEXPORT _Player* getPlayer(Connection* c, int num)
{
  return c->Players + num;
}
DLLEXPORT int getPlayerCount(Connection* c)
{
  return c->PlayerCount;
}


DLLEXPORT int getMaxReefHealth(Connection* c)
{
  return c->maxReefHealth;
}
DLLEXPORT int getBoundLength(Connection* c)
{
  return c->boundLength;
}
DLLEXPORT int getTurnNumber(Connection* c)
{
  return c->turnNumber;
}
DLLEXPORT int getPlayerID(Connection* c)
{
  return c->playerID;
}
DLLEXPORT int getGameNumber(Connection* c)
{
  return c->gameNumber;
}
DLLEXPORT int getMapWidth(Connection* c)
{
  return c->mapWidth;
}
DLLEXPORT int getMapHeight(Connection* c)
{
  return c->mapHeight;
}
DLLEXPORT int getTrashAmount(Connection* c)
{
  return c->trashAmount;
}
DLLEXPORT int getCurrentSeason(Connection* c)
{
  return c->currentSeason;
}
DLLEXPORT int getSeasonLength(Connection* c)
{
  return c->seasonLength;
}
DLLEXPORT int getHealPercent(Connection* c)
{
  return c->healPercent;
}
DLLEXPORT int getMaxFood(Connection* c)
{
  return c->maxFood;
}
