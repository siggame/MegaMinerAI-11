// -*-c++-*-

#ifndef TILE_H
#define TILE_H

#include <iostream>
#include "structures.h"

#include "Mappable.h"

///Represents a single tile on the map, can contain some amount of trash. Example: 5 trash can be split to 2 and 3
class Tile : public Mappable {
  public:
  Tile(_Tile* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///X position of the object
  int x();
  ///Y position of the object
  int y();
  ///The amount of trash on this tile
  int trashAmount();
  ///The owner of the tile if it is part of a cove
  int owner();
  ///If the current tile is part of a cove
  int isCove();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Tile ob);
};

#endif

