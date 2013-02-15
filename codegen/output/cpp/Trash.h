// -*-c++-*-

#ifndef TRASH_H
#define TRASH_H

#include <iostream>
#include "structures.h"

#include "Mappable.h"

///This is a Trash object
class Trash : public Mappable {
  public:
  Trash(_Trash* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///X position of the object
  int x();
  ///Y position of the object
  int y();
  ///The weight of the trash
  int weight();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Trash ob);
};

#endif

