// -*-c++-*-

#ifndef MAPPABLE_H
#define MAPPABLE_H

#include <iostream>
#include "vc_structures.h"


namespace client
{


///A mappable object!
class Mappable {
  public:
  void* ptr;
  Mappable(_Mappable* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///X position of the object
  int x();
  ///Y position of the object
  int y();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Mappable ob);
};

}

#endif

