// -*-c++-*-

#include "Trash.h"
#include "game.h"


Trash::Trash(_Trash* pointer)
{
    ptr = (void*) pointer;
}

int Trash::id()
{
  return ((_Trash*)ptr)->id;
}

int Trash::x()
{
  return ((_Trash*)ptr)->x;
}

int Trash::y()
{
  return ((_Trash*)ptr)->y;
}

int Trash::weight()
{
  return ((_Trash*)ptr)->weight;
}




std::ostream& operator<<(std::ostream& stream,Trash ob)
{
  stream << "id: " << ((_Trash*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Trash*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Trash*)ob.ptr)->y  <<'\n';
  stream << "weight: " << ((_Trash*)ob.ptr)->weight  <<'\n';
  return stream;
}
