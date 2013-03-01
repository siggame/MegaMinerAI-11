// -*-c++-*-

#include "FishSpecies.h"
#include "game.h"


namespace client
{

FishSpecies::FishSpecies(_FishSpecies* pointer)
{
    ptr = (void*) pointer;
}

int FishSpecies::id()
{
  return ((_FishSpecies*)ptr)->id;
}

char* FishSpecies::species()
{
  return ((_FishSpecies*)ptr)->species;
}

int FishSpecies::cost()
{
  return ((_FishSpecies*)ptr)->cost;
}

int FishSpecies::maxHealth()
{
  return ((_FishSpecies*)ptr)->maxHealth;
}

int FishSpecies::maxMovement()
{
  return ((_FishSpecies*)ptr)->maxMovement;
}

int FishSpecies::carryCap()
{
  return ((_FishSpecies*)ptr)->carryCap;
}

int FishSpecies::attackPower()
{
  return ((_FishSpecies*)ptr)->attackPower;
}

int FishSpecies::range()
{
  return ((_FishSpecies*)ptr)->range;
}

int FishSpecies::maxAttacks()
{
  return ((_FishSpecies*)ptr)->maxAttacks;
}

int FishSpecies::turnsTillAvailalbe()
{
  return ((_FishSpecies*)ptr)->turnsTillAvailalbe;
}

int FishSpecies::turnsTillUnavailable()
{
  return ((_FishSpecies*)ptr)->turnsTillUnavailable;
}


int FishSpecies::spawn(int x, int y)
{
  return fishSpeciesSpawn( (_FishSpecies*)ptr, x, y);
}



std::ostream& operator<<(std::ostream& stream,FishSpecies ob)
{
  stream << "id: " << ((_FishSpecies*)ob.ptr)->id  <<'\n';
  stream << "species: " << ((_FishSpecies*)ob.ptr)->species  <<'\n';
  stream << "cost: " << ((_FishSpecies*)ob.ptr)->cost  <<'\n';
  stream << "maxHealth: " << ((_FishSpecies*)ob.ptr)->maxHealth  <<'\n';
  stream << "maxMovement: " << ((_FishSpecies*)ob.ptr)->maxMovement  <<'\n';
  stream << "carryCap: " << ((_FishSpecies*)ob.ptr)->carryCap  <<'\n';
  stream << "attackPower: " << ((_FishSpecies*)ob.ptr)->attackPower  <<'\n';
  stream << "range: " << ((_FishSpecies*)ob.ptr)->range  <<'\n';
  stream << "maxAttacks: " << ((_FishSpecies*)ob.ptr)->maxAttacks  <<'\n';
  stream << "turnsTillAvailalbe: " << ((_FishSpecies*)ob.ptr)->turnsTillAvailalbe  <<'\n';
  stream << "turnsTillUnavailable: " << ((_FishSpecies*)ob.ptr)->turnsTillUnavailable  <<'\n';
  return stream;
}

}
