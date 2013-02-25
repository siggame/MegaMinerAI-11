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
DLLEXPORT int fishSpeciesGetId(_FishSpecies* ptr)
{
  return ptr->id;
}
DLLEXPORT char* fishSpeciesGetSpecies(_FishSpecies* ptr)
{
  return ptr->species;
}
DLLEXPORT int fishSpeciesGetCost(_FishSpecies* ptr)
{
  return ptr->cost;
}
DLLEXPORT int fishSpeciesGetMaxHealth(_FishSpecies* ptr)
{
  return ptr->maxHealth;
}
DLLEXPORT int fishSpeciesGetMaxMovement(_FishSpecies* ptr)
{
  return ptr->maxMovement;
}
DLLEXPORT int fishSpeciesGetCarryCap(_FishSpecies* ptr)
{
  return ptr->carryCap;
}
DLLEXPORT int fishSpeciesGetAttackPower(_FishSpecies* ptr)
{
  return ptr->attackPower;
}
DLLEXPORT int fishSpeciesGetRange(_FishSpecies* ptr)
{
  return ptr->range;
}
DLLEXPORT int fishSpeciesGetMaxAttacks(_FishSpecies* ptr)
{
  return ptr->maxAttacks;
}
DLLEXPORT int fishSpeciesGetCanStealth(_FishSpecies* ptr)
{
  return ptr->canStealth;
}
DLLEXPORT int fishSpeciesGetTurnsTillAvailalbe(_FishSpecies* ptr)
{
  return ptr->turnsTillAvailalbe;
}
DLLEXPORT int fishSpeciesGetTurnsTillUnavailable(_FishSpecies* ptr)
{
  return ptr->turnsTillUnavailable;
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
DLLEXPORT int tileGetIsCove(_Tile* ptr)
{
  return ptr->isCove;
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
DLLEXPORT int fishGetIsVisible(_Fish* ptr)
{
  return ptr->isVisible;
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
DLLEXPORT char* fishGetSpecies(_Fish* ptr)
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

