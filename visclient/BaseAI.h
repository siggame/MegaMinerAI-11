//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef BASEAI_H
#define BASEAI_H

#include <vector>
#include <ctime>
#include "game.h"

#include "Mappable.h"
#include "Trash.h"
#include "Fish.h"
#include "Player.h"

namespace client
{

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of boiler-plate code out of the way
///The provided AI class does just that.
class BaseAI
{
protected:
  Connection* c;
  std::vector<Mappable> mappables;
  std::vector<Trash> trashs;
  std::vector<Fish> fishs;
  std::vector<Player> players;
public:
  ///How many sand dollars a player receives
  int dollarsPerTurn();
  ///How many turns it has been since the beginning of the game
  int turnNumber();
  ///Player Number; either 0 or 1
  int playerID();
  ///What number game this is for the server
  int gameNumber();
  ///Turns until you can spawn new fish
  int turnsTillSpawn();
  ///How much health a reef has initially
  int maxReefHealth();
  ///How much damage trash does
  int trashDamage();
  ///How wide the map is
  int mapWidth();
  ///How high the map is
  int mapHeight();
  
  BaseAI(Connection* c);
  virtual ~BaseAI();
  ///
  ///Make this your username, which should be provided.
  virtual const char* username() = 0;
  ///
  ///Make this your password, which should be provided.
  virtual const char* password() = 0;
  ///
  ///This function is run once, before your first turn.
  virtual void init() = 0;
  ///
  ///This function is called each time it is your turn
  ///Return true to end your turn, return false to ask the server for updated information
  virtual bool run() = 0;
  ///
  ///This function is called after the last turn.
  virtual void end() = 0;


  bool startTurn();
};

}

#endif
