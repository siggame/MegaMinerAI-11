// -*-c++-*-

#ifndef PLAYER_H
#define PLAYER_H

#include <iostream>
#include "vc_structures.h"


namespace client
{


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
  int curReefHealth();
  ///Currency for fish
  int sandDollars();

  // Actions
  ///Allows a player to display messages on the screen
  int talk(char* message);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Player ob);
};

}

#endif

