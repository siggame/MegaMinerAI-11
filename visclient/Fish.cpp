// -*-c++-*-

#include "Fish.h"
#include "game.h"


namespace client
{

Fish::Fish(_Fish* pointer)
{
    ptr = (void*) pointer;
}

int Fish::id()
{
  return ((_Fish*)ptr)->id;
}

int Fish::x()
{
  return ((_Fish*)ptr)->x;
}

int Fish::y()
{
  return ((_Fish*)ptr)->y;
}

int Fish::owner()
{
  return ((_Fish*)ptr)->owner;
}

int Fish::maxHealth()
{
  return ((_Fish*)ptr)->maxHealth;
}

int Fish::currentHealth()
{
  return ((_Fish*)ptr)->currentHealth;
}

int Fish::maxMovement()
{
  return ((_Fish*)ptr)->maxMovement;
}

int Fish::movementLeft()
{
  return ((_Fish*)ptr)->movementLeft;
}

int Fish::carryCap()
{
  return ((_Fish*)ptr)->carryCap;
}

int Fish::carryWeight()
{
  return ((_Fish*)ptr)->carryWeight;
}

int Fish::attackPower()
{
  return ((_Fish*)ptr)->attackPower;
}

int Fish::isVisible()
{
  return ((_Fish*)ptr)->isVisible;
}

int Fish::attacksLeft()
{
  return ((_Fish*)ptr)->attacksLeft;
}

int Fish::range()
{
  return ((_Fish*)ptr)->range;
}

char* Fish::species()
{
  return ((_Fish*)ptr)->species;
}


int Fish::move(int x, int y)
{
  return fishMove( (_Fish*)ptr, x, y);
}

int Fish::pickUp(int x, int y, int weight)
{
  return fishPickUp( (_Fish*)ptr, x, y, weight);
}

int Fish::drop(int x, int y, int weight)
{
  return fishDrop( (_Fish*)ptr, x, y, weight);
}

int Fish::attack(int x, int y)
{
  return fishAttack( (_Fish*)ptr, x, y);
}



std::ostream& operator<<(std::ostream& stream,Fish ob)
{
  stream << "id: " << ((_Fish*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Fish*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Fish*)ob.ptr)->y  <<'\n';
  stream << "owner: " << ((_Fish*)ob.ptr)->owner  <<'\n';
  stream << "maxHealth: " << ((_Fish*)ob.ptr)->maxHealth  <<'\n';
  stream << "currentHealth: " << ((_Fish*)ob.ptr)->currentHealth  <<'\n';
  stream << "maxMovement: " << ((_Fish*)ob.ptr)->maxMovement  <<'\n';
  stream << "movementLeft: " << ((_Fish*)ob.ptr)->movementLeft  <<'\n';
  stream << "carryCap: " << ((_Fish*)ob.ptr)->carryCap  <<'\n';
  stream << "carryWeight: " << ((_Fish*)ob.ptr)->carryWeight  <<'\n';
  stream << "attackPower: " << ((_Fish*)ob.ptr)->attackPower  <<'\n';
  stream << "isVisible: " << ((_Fish*)ob.ptr)->isVisible  <<'\n';
  stream << "attacksLeft: " << ((_Fish*)ob.ptr)->attacksLeft  <<'\n';
  stream << "range: " << ((_Fish*)ob.ptr)->range  <<'\n';
  stream << "species: " << ((_Fish*)ob.ptr)->species  <<'\n';
  return stream;
}

}
