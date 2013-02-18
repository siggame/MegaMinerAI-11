#include "getters.h"

namespace client
{

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
DLLEXPORT int trashGetId(_Trash* ptr)
{
  return ptr->id;
}
DLLEXPORT int trashGetX(_Trash* ptr)
{
  return ptr->x;
}
DLLEXPORT int trashGetY(_Trash* ptr)
{
  return ptr->y;
}
DLLEXPORT int trashGetWeight(_Trash* ptr)
{
  return ptr->weight;
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
DLLEXPORT char* fishGetSpecies(_Fish* ptr)
{
  return ptr->species;
}
DLLEXPORT int fishGetMaxHealth(_Fish* ptr)
{
  return ptr->maxHealth;
}
DLLEXPORT int fishGetCurHealth(_Fish* ptr)
{
  return ptr->curHealth;
}
DLLEXPORT int fishGetMaxMoves(_Fish* ptr)
{
  return ptr->maxMoves;
}
DLLEXPORT int fishGetMovementLeft(_Fish* ptr)
{
  return ptr->movementLeft;
}
DLLEXPORT int fishGetCarryCap(_Fish* ptr)
{
  return ptr->carryCap;
}
DLLEXPORT int fishGetCarryWeight(_Fish* ptr)
{
  return ptr->carryWeight;
}
DLLEXPORT int fishGetAttackPower(_Fish* ptr)
{
  return ptr->attackPower;
}
DLLEXPORT int fishGetIsVisible(_Fish* ptr)
{
  return ptr->isVisible;
}
DLLEXPORT int fishGetAttacksLeft(_Fish* ptr)
{
  return ptr->attacksLeft;
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
DLLEXPORT int playerGetCurReefHealth(_Player* ptr)
{
  return ptr->curReefHealth;
}
DLLEXPORT int playerGetSandDollars(_Player* ptr)
{
  return ptr->sandDollars;
}

}
