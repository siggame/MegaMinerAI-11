// -*-c++-*-

#include "Species.h"
#include "game.h"


namespace client
{

Species::Species(_Species* pointer)
{
    ptr = (void*) pointer;
}

int Species::id()
{
  return ((_Species*)ptr)->id;
}

char* Species::name()
{
  return ((_Species*)ptr)->name;
}

int Species::index()
{
  return ((_Species*)ptr)->index;
}

int Species::cost()
{
  return ((_Species*)ptr)->cost;
}

int Species::maxHealth()
{
  return ((_Species*)ptr)->maxHealth;
}

int Species::maxMovement()
{
  return ((_Species*)ptr)->maxMovement;
}

int Species::carryCap()
{
  return ((_Species*)ptr)->carryCap;
}

int Species::attackPower()
{
  return ((_Species*)ptr)->attackPower;
}

int Species::range()
{
  return ((_Species*)ptr)->range;
}

int Species::maxAttacks()
{
  return ((_Species*)ptr)->maxAttacks;
}

int Species::season()
{
  return ((_Species*)ptr)->season;
}


int Species::spawn(int x, int y)
{
  return speciesSpawn( (_Species*)ptr, x, y);
}



std::ostream& operator<<(std::ostream& stream,Species ob)
{
  stream << "id: " << ((_Species*)ob.ptr)->id  <<'\n';
  stream << "name: " << ((_Species*)ob.ptr)->name  <<'\n';
  stream << "index: " << ((_Species*)ob.ptr)->index  <<'\n';
  stream << "cost: " << ((_Species*)ob.ptr)->cost  <<'\n';
  stream << "maxHealth: " << ((_Species*)ob.ptr)->maxHealth  <<'\n';
  stream << "maxMovement: " << ((_Species*)ob.ptr)->maxMovement  <<'\n';
  stream << "carryCap: " << ((_Species*)ob.ptr)->carryCap  <<'\n';
  stream << "attackPower: " << ((_Species*)ob.ptr)->attackPower  <<'\n';
  stream << "range: " << ((_Species*)ob.ptr)->range  <<'\n';
  stream << "maxAttacks: " << ((_Species*)ob.ptr)->maxAttacks  <<'\n';
  stream << "season: " << ((_Species*)ob.ptr)->season  <<'\n';
  return stream;
}

}
