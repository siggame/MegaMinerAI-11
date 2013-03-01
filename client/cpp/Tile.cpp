// -*-c++-*-

#include "Tile.h"
#include "game.h"


Tile::Tile(_Tile* pointer)
{
    ptr = (void*) pointer;
}

int Tile::id()
{
  return ((_Tile*)ptr)->id;
}

int Tile::x()
{
  return ((_Tile*)ptr)->x;
}

int Tile::y()
{
  return ((_Tile*)ptr)->y;
}

int Tile::trashAmount()
{
  return ((_Tile*)ptr)->trashAmount;
}

int Tile::owner()
{
  return ((_Tile*)ptr)->owner;
}

int Tile::isCove()
{
  return ((_Tile*)ptr)->isCove;
}




std::ostream& operator<<(std::ostream& stream,Tile ob)
{
  stream << "id: " << ((_Tile*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Tile*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Tile*)ob.ptr)->y  <<'\n';
  stream << "trashAmount: " << ((_Tile*)ob.ptr)->trashAmount  <<'\n';
  stream << "owner: " << ((_Tile*)ob.ptr)->owner  <<'\n';
  stream << "isCove: " << ((_Tile*)ob.ptr)->isCove  <<'\n';
  return stream;
}
