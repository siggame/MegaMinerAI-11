// -*-c++-*-

#ifndef FISH_H
#define FISH_H

#include <iostream>
#include "vc_structures.h"

#include "Mappable.h"

namespace client
{

class Tile;
class Fish;

///This is your primary unit for Reef. It will perform all of your major actions (pickup, attack, move, drop). It stats are based off of its species
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
  ///The index of the fish species.
  int species();

  // Actions
  ///Command a fish to move to a specified position
  int move(int x, int y);
  ///Command a fish to pick up some trash at a specified position
  int pickUp(Tile& tile, int weight);
  ///Command a fish to drop some trash at a specified position
  int drop(Tile& tile, int weight);
  ///Command a fish to attack a target
  int attack(Fish& target);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Fish ob);
};

}

#endif

