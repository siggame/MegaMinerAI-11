//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef GAME_H
#define GAME_H

#include "network.h"
#include "structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)

#ifdef ENABLE_THREADS
#include "pthread.h"
#endif

#else
#define DLLEXPORT

#ifdef ENABLE_THREADS
#include <pthread.h>
#endif

#endif

struct Connection
{
  int socket;
  
  #ifdef ENABLE_THREADS
  pthread_mutex_t mutex;
  #endif
  
  int dollarsPerTurn;
  int turnNumber;
  int playerID;
  int gameNumber;
  int turnsTillSpawn;
  int maxReefHealth;
  int trashDamage;
  int mapWidth;
  int mapHeight;

  _Mappable* Mappables;
  int MappableCount;
  _Trash* Trashs;
  int TrashCount;
  _Fish* Fishs;
  int FishCount;
  _Player* Players;
  int PlayerCount;
};

#ifdef __cplusplus
extern "C"
{
#endif
  DLLEXPORT Connection* createConnection();
  DLLEXPORT void destroyConnection(Connection* c);
  DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port);

  DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password);
  DLLEXPORT int createGame(Connection* c);
  DLLEXPORT int joinGame(Connection* c, int id, const char* playerType);

  DLLEXPORT void endTurn(Connection* c);
  DLLEXPORT void getStatus(Connection* c);


//commands

  ///Command a fish to move to a specified position
  DLLEXPORT int fishMove(_Fish* object, int x, int y);
  ///Command a fish to pick up some trash at a specified position
  DLLEXPORT int fishPickUp(_Fish* object, int x, int y, int weight);
  ///Command a fish to drop some trash at a specified position
  DLLEXPORT int fishDrop(_Fish* object, int x, int y, int weight);
  ///Command a fish to attack another fish at a specified position
  DLLEXPORT int fishAttack(_Fish* object, int x, int y);
  ///Allows a player to display messages on the screen
  DLLEXPORT int playerTalk(_Player* object, char* message);

//derived properties



//accessors

DLLEXPORT int getDollarsPerTurn(Connection* c);
DLLEXPORT int getTurnNumber(Connection* c);
DLLEXPORT int getPlayerID(Connection* c);
DLLEXPORT int getGameNumber(Connection* c);
DLLEXPORT int getTurnsTillSpawn(Connection* c);
DLLEXPORT int getMaxReefHealth(Connection* c);
DLLEXPORT int getTrashDamage(Connection* c);
DLLEXPORT int getMapWidth(Connection* c);
DLLEXPORT int getMapHeight(Connection* c);

DLLEXPORT _Mappable* getMappable(Connection* c, int num);
DLLEXPORT int getMappableCount(Connection* c);

DLLEXPORT _Trash* getTrash(Connection* c, int num);
DLLEXPORT int getTrashCount(Connection* c);

DLLEXPORT _Fish* getFish(Connection* c, int num);
DLLEXPORT int getFishCount(Connection* c);

DLLEXPORT _Player* getPlayer(Connection* c, int num);
DLLEXPORT int getPlayerCount(Connection* c);



  DLLEXPORT int networkLoop(Connection* c);
#ifdef __cplusplus
}
#endif

#endif
