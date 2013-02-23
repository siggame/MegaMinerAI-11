#ifndef GETTERS_H 
#define GETTERS_H
#include "structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

DLLEXPORT int mappableGetId(_Mappable* ptr);
DLLEXPORT int mappableGetX(_Mappable* ptr);
DLLEXPORT int mappableGetY(_Mappable* ptr);


DLLEXPORT int fishSpeciesGetId(_FishSpecies* ptr);
DLLEXPORT char* fishSpeciesGetSpecies(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetCost(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetMaxHealth(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetMaxMovement(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetCarryCap(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetAttackPower(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetRange(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetMaxAttacks(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetCanStealth(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetTurnsTillAvailalbe(_FishSpecies* ptr);
DLLEXPORT int fishSpeciesGetTurnsTillUnavailable(_FishSpecies* ptr);


DLLEXPORT int tileGetId(_Tile* ptr);
DLLEXPORT int tileGetX(_Tile* ptr);
DLLEXPORT int tileGetY(_Tile* ptr);
DLLEXPORT int tileGetTrashAmount(_Tile* ptr);


DLLEXPORT int fishGetId(_Fish* ptr);
DLLEXPORT int fishGetX(_Fish* ptr);
DLLEXPORT int fishGetY(_Fish* ptr);
DLLEXPORT int fishGetOwner(_Fish* ptr);
DLLEXPORT int fishGetMaxHealth(_Fish* ptr);
DLLEXPORT int fishGetCurrentHealth(_Fish* ptr);
DLLEXPORT int fishGetMaxMovement(_Fish* ptr);
DLLEXPORT int fishGetMovementLeft(_Fish* ptr);
DLLEXPORT int fishGetCarryCap(_Fish* ptr);
DLLEXPORT int fishGetCarryingWeight(_Fish* ptr);
DLLEXPORT int fishGetAttackPower(_Fish* ptr);
DLLEXPORT int fishGetIsVisible(_Fish* ptr);
DLLEXPORT int fishGetMaxAttacks(_Fish* ptr);
DLLEXPORT int fishGetAttacksLeft(_Fish* ptr);
DLLEXPORT int fishGetRange(_Fish* ptr);
DLLEXPORT char* fishGetSpecies(_Fish* ptr);


DLLEXPORT int playerGetId(_Player* ptr);
DLLEXPORT char* playerGetPlayerName(_Player* ptr);
DLLEXPORT float playerGetTime(_Player* ptr);
DLLEXPORT int playerGetCurrentReefHealth(_Player* ptr);
DLLEXPORT int playerGetSpawnFood(_Player* ptr);



#ifdef __cplusplus
}
#endif

#endif
