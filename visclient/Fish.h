// -*-c++-*-

#ifndef FISH_H
#define FISH_H

#include <iostream>
#include "vc_structures.h"

#include "Mappable.h"

namespace client
{


class Fish : public Mappable {
  public:
  Fish(_Fish* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///X position of the object
  int x();
  ///Y position of the object
  int y();
  ///The owner of this fish
  int owner();
  ///The maximum health of the fish
  int maxHealth();
  ///The current health of the fish
  int currentHealth();
  ///The maximum number of movements in a turn
  int maxMovement();
  ///The number of movements left
  int movementLeft();
  ///The total weight the fish can carry
  int carryCap();
  ///The current amount of weight the fish is carrying
  int carryingWeight();
  ///The power of the fish's attack
  int attackPower();
  ///The visibleness of the fish
  int isVisible();
  ///The maximum number of attacks this fish has per turn
  int maxAttacks();
  ///The number of attacks a fish has left
  int attacksLeft();
  ///The attack range of the fish
  int range();
  ///The fish species
  char* species();

  // Actions
  ///Command a fish to move to a specified position
  int move(int x, int y);
  ///Command a fish to pick up some trash at a specified position
  int pickUp(int x, int y, int weight);
  ///Command a fish to drop some trash at a specified position
  int drop(int x, int y, int weight);
  ///Command a fish to attack another fish at a specified position
  int attack(int x, int y);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Fish ob);
};

}

#endif

