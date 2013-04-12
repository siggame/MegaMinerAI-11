// -*-c++-*-

#ifndef SPECIES_H
#define SPECIES_H

#include <iostream>
#include "vc_structures.h"


namespace client
{

class Tile;

///This class describes the characteristics for each type of fish. A species will only be available for so long, and new species will become available as a match progreses. 
class Species {
  public:
  void* ptr;
  Species(_Species* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The name of this species
  char* name();
  ///The species index of the species.
  int index();
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
  ///The attack range of the fish
  int range();
  ///Maximum number of times this unit can attack per turn
  int maxAttacks();
  ///Determines what season this species will be spawnable in
  int season();

  // Actions
  ///Have a new fish spawn and join the fight! Select which tile you want the fish to spawn on
  int spawn(Tile& tile);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Species ob);
};

}

#endif

