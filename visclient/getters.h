#ifndef GETTERS_H 
#define GETTERS_H
#include "vc_structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif

namespace client
{

#ifdef __cplusplus
extern "C" {
#endif

DLLEXPORT int mappableGetId(_Mappable* ptr);
DLLEXPORT int mappableGetX(_Mappable* ptr);
DLLEXPORT int mappableGetY(_Mappable* ptr);


DLLEXPORT int trashGetId(_Trash* ptr);
DLLEXPORT int trashGetX(_Trash* ptr);
DLLEXPORT int trashGetY(_Trash* ptr);
DLLEXPORT int trashGetWeight(_Trash* ptr);


DLLEXPORT int fishGetId(_Fish* ptr);
DLLEXPORT int fishGetX(_Fish* ptr);
DLLEXPORT int fishGetY(_Fish* ptr);
DLLEXPORT int fishGetOwner(_Fish* ptr);
DLLEXPORT char* fishGetSpecies(_Fish* ptr);
DLLEXPORT int fishGetMaxHealth(_Fish* ptr);
DLLEXPORT int fishGetCurHealth(_Fish* ptr);
DLLEXPORT int fishGetMaxMoves(_Fish* ptr);
DLLEXPORT int fishGetMovementLeft(_Fish* ptr);
DLLEXPORT int fishGetCarryCap(_Fish* ptr);
DLLEXPORT int fishGetCarryWeight(_Fish* ptr);
DLLEXPORT int fishGetAttackPower(_Fish* ptr);
DLLEXPORT int fishGetIsVisible(_Fish* ptr);
DLLEXPORT int fishGetAttacksLeft(_Fish* ptr);


DLLEXPORT int playerGetId(_Player* ptr);
DLLEXPORT char* playerGetPlayerName(_Player* ptr);
DLLEXPORT float playerGetTime(_Player* ptr);
DLLEXPORT int playerGetCurReefHealth(_Player* ptr);
DLLEXPORT int playerGetSandDollars(_Player* ptr);



#ifdef __cplusplus
}
#endif

}

#endif
