// -*-c++-*-

#ifndef PLAYER_H
#define PLAYER_H

#include <iostream>
#include "structures.h"


class Player {
  public:
  void* ptr;
  Player(_Player* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///Player's Name
  char* playerName();
  ///Time remaining, updated at start of turn
  float time();
  ///The player's current reef health
  int currentReefHealth();
  ///Food used to spawn new fish
  int spawnFood();

  // Actions
  ///Allows a player to display messages on the screen
  bool talk(char* message);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Player ob);
};

#endif

