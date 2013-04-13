#include "getters.h"

DLLEXPORT int mappableGetId(_Mappable* ptr)
{
  return ptr->id;
}
DLLEXPORT int mappableGetX(_Mappable* ptr)
{
  return ptr->x;
}
DLLEXPORT int mappableGetY(_Mappable* ptr)
{
  return ptr->y;
}
DLLEXPORT int tileGetId(_Tile* ptr)
{
  return ptr->id;
}
DLLEXPORT int tileGetX(_Tile* ptr)
{
  return ptr->x;
}
DLLEXPORT int tileGetY(_Tile* ptr)
{
  return ptr->y;
}
DLLEXPORT int tileGetTrashAmount(_Tile* ptr)
{
  return ptr->trashAmount;
}
DLLEXPORT int tileGetOwner(_Tile* ptr)
{
  return ptr->owner;
}
DLLEXPORT int tileGetHasEgg(_Tile* ptr)
{
  return ptr->hasEgg;
}
DLLEXPORT int tileGetDamages(_Tile* ptr)
{
  return ptr->damages;
}
DLLEXPORT int speciesGetId(_Species* ptr)
{
  return ptr->id;
}
DLLEXPORT char* speciesGetName(_Species* ptr)
{
  return ptr->name;
}
DLLEXPORT int speciesGetSpeciesNum(_Species* ptr)
{
  return ptr->speciesNum;
}
DLLEXPORT int speciesGetCost(_Species* ptr)
{
  return ptr->cost;
}
DLLEXPORT int speciesGetMaxHealth(_Species* ptr)
{
  return ptr->maxHealth;
}
DLLEXPORT int speciesGetMaxMovement(_Species* ptr)
{
  return ptr->maxMovement;
}
DLLEXPORT int speciesGetCarryCap(_Species* ptr)
{
  return ptr->carryCap;
}
DLLEXPORT int speciesGetAttackPower(_Species* ptr)
{
  return ptr->attackPower;
}
DLLEXPORT int speciesGetRange(_Species* ptr)
{
  return ptr->range;
}
DLLEXPORT int speciesGetMaxAttacks(_Species* ptr)
{
  return ptr->maxAttacks;
}
DLLEXPORT int speciesGetSeason(_Species* ptr)
{
  return ptr->season;
}
DLLEXPORT int fishGetId(_Fish* ptr)
{
  return ptr->id;
}
DLLEXPORT int fishGetX(_Fish* ptr)
{
  return ptr->x;
}
DLLEXPORT int fishGetY(_Fish* ptr)
{
  return ptr->y;
}
DLLEXPORT int fishGetOwner(_Fish* ptr)
{
  return ptr->owner;
}
DLLEXPORT int fishGetMaxHealth(_Fish* ptr)
{
  return ptr->maxHealth;
}
DLLEXPORT int fishGetCurrentHealth(_Fish* ptr)
{
  return ptr->currentHealth;
}
DLLEXPORT int fishGetMaxMovement(_Fish* ptr)
{
  return ptr->maxMovement;
}
DLLEXPORT int fishGetMovementLeft(_Fish* ptr)
{
  return ptr->movementLeft;
}
DLLEXPORT int fishGetCarryCap(_Fish* ptr)
{
  return ptr->carryCap;
}
DLLEXPORT int fishGetCarryingWeight(_Fish* ptr)
{
  return ptr->carryingWeight;
}
DLLEXPORT int fishGetAttackPower(_Fish* ptr)
{
  return ptr->attackPower;
}
DLLEXPORT int fishGetMaxAttacks(_Fish* ptr)
{
  return ptr->maxAttacks;
}
DLLEXPORT int fishGetAttacksLeft(_Fish* ptr)
{
  return ptr->attacksLeft;
}
DLLEXPORT int fishGetRange(_Fish* ptr)
{
  return ptr->range;
}
DLLEXPORT int fishGetSpecies(_Fish* ptr)
{
  return ptr->species;
}
DLLEXPORT int playerGetId(_Player* ptr)
{
  return ptr->id;
}
DLLEXPORT char* playerGetPlayerName(_Player* ptr)
{
  return ptr->playerName;
}
DLLEXPORT float playerGetTime(_Player* ptr)
{
  return ptr->time;
}
DLLEXPORT int playerGetCurrentReefHealth(_Player* ptr)
{
  return ptr->currentReefHealth;
}
DLLEXPORT int playerGetSpawnFood(_Player* ptr)
{
  return ptr->spawnFood;
}

