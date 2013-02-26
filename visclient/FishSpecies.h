// -*-c++-*-

#ifndef FISHSPECIES_H
#define FISHSPECIES_H

#include <iostream>
#include "vc_structures.h"


namespace client
{


class FishSpecies {
  public:
  void* ptr;
  FishSpecies(_FishSpecies* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The fish species
  char* species();
  ///The amount of food it takes to raise this fish
  int cost();
  ///The maximum health of this fish
  int maxHealth();
  ///The maximum number of movements in a turn
  int maxMovement();
  ///The total weight the fish can carry
  int carryCap();
  ///The power of the fish's attack
  int attackPower();
  ///The attack arrange of the fish
  int range();
  ///Maximum number of times this unit can attack per turn
  int maxAttacks();
  ///How many turns until you can spawn this fish species
  int turnsTillAvailalbe();
  ///How many turns until you can no longer spawn this fish species
  int turnsTillUnavailable();

  // Actions
  ///Have a new fish spawn and join the fight!
  int spawn(int x, int y);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, FishSpecies ob);
};

}

#endif

