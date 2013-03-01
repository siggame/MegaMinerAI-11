# -*-python-*-

import os

from ctypes import *

try:
  if os.name == 'posix':
    library = CDLL("./libclient.so")
  elif os.name == 'nt':
    library = CDLL("./client.dll")
  else:
    raise Exception("Unrecognized OS: "+os.name)
except OSError:
  raise Exception("It looks like you didn't build libclient. Run 'make' and try again.")

# commands

library.createConnection.restype = c_void_p
library.createConnection.argtypes = []

library.serverConnect.restype = c_int
library.serverConnect.argtypes = [c_void_p, c_char_p, c_char_p]

library.serverLogin.restype = c_int
library.serverLogin.argtypes = [c_void_p, c_char_p, c_char_p]

library.createGame.restype = c_int
library.createGame.argtypes = [c_void_p]

library.joinGame.restype = c_int
library.joinGame.argtypes = [c_void_p, c_int, c_char_p]

library.endTurn.restype = None
library.endTurn.argtypes = [c_void_p]

library.getStatus.restype = None
library.getStatus.argtypes = [c_void_p]

library.networkLoop.restype = c_int
library.networkLoop.argtypes = [c_void_p]

#Functions
library.fishSpeciesSpawn.restype = c_int
library.fishSpeciesSpawn.argtypes = [c_void_p, c_int, c_int]

library.fishMove.restype = c_int
library.fishMove.argtypes = [c_void_p, c_int, c_int]

library.fishPickUp.restype = c_int
library.fishPickUp.argtypes = [c_void_p, c_int, c_int, c_int]

library.fishDrop.restype = c_int
library.fishDrop.argtypes = [c_void_p, c_int, c_int, c_int]

library.fishAttack.restype = c_int
library.fishAttack.argtypes = [c_void_p, c_int, c_int]

library.playerTalk.restype = c_int
library.playerTalk.argtypes = [c_void_p, c_char_p]

# accessors

#Globals
library.getInitialFood.restype = c_int
library.getInitialFood.argtypes = [c_void_p]

library.getSharedLowerBound.restype = c_int
library.getSharedLowerBound.argtypes = [c_void_p]

library.getSharedUpperBound.restype = c_int
library.getSharedUpperBound.argtypes = [c_void_p]

library.getSpawnFoodPerTurn.restype = c_int
library.getSpawnFoodPerTurn.argtypes = [c_void_p]

library.getTurnNumber.restype = c_int
library.getTurnNumber.argtypes = [c_void_p]

library.getPlayerID.restype = c_int
library.getPlayerID.argtypes = [c_void_p]

library.getGameNumber.restype = c_int
library.getGameNumber.argtypes = [c_void_p]

library.getTurnsTillSpawn.restype = c_int
library.getTurnsTillSpawn.argtypes = [c_void_p]

library.getMaxReefHealth.restype = c_int
library.getMaxReefHealth.argtypes = [c_void_p]

library.getTrashDamage.restype = c_int
library.getTrashDamage.argtypes = [c_void_p]

library.getMapWidth.restype = c_int
library.getMapWidth.argtypes = [c_void_p]

library.getMapHeight.restype = c_int
library.getMapHeight.argtypes = [c_void_p]

library.getTrashAmount.restype = c_int
library.getTrashAmount.argtypes = [c_void_p]

library.getCoveX.restype = c_int
library.getCoveX.argtypes = [c_void_p]

library.getCoveY.restype = c_int
library.getCoveY.argtypes = [c_void_p]

library.getMappable.restype = c_void_p
library.getMappable.argtypes = [c_void_p, c_int]

library.getMappableCount.restype = c_int
library.getMappableCount.argtypes = [c_void_p]

library.getFishSpecies.restype = c_void_p
library.getFishSpecies.argtypes = [c_void_p, c_int]

library.getFishSpeciesCount.restype = c_int
library.getFishSpeciesCount.argtypes = [c_void_p]

library.getTile.restype = c_void_p
library.getTile.argtypes = [c_void_p, c_int]

library.getTileCount.restype = c_int
library.getTileCount.argtypes = [c_void_p]

library.getFish.restype = c_void_p
library.getFish.argtypes = [c_void_p, c_int]

library.getFishCount.restype = c_int
library.getFishCount.argtypes = [c_void_p]

library.getPlayer.restype = c_void_p
library.getPlayer.argtypes = [c_void_p, c_int]

library.getPlayerCount.restype = c_int
library.getPlayerCount.argtypes = [c_void_p]

# getters

#Data
library.mappableGetId.restype = c_int
library.mappableGetId.argtypes = [c_void_p]

library.mappableGetX.restype = c_int
library.mappableGetX.argtypes = [c_void_p]

library.mappableGetY.restype = c_int
library.mappableGetY.argtypes = [c_void_p]

library.fishSpeciesGetId.restype = c_int
library.fishSpeciesGetId.argtypes = [c_void_p]

library.fishSpeciesGetSpecies.restype = c_char_p
library.fishSpeciesGetSpecies.argtypes = [c_void_p]

library.fishSpeciesGetCost.restype = c_int
library.fishSpeciesGetCost.argtypes = [c_void_p]

library.fishSpeciesGetMaxHealth.restype = c_int
library.fishSpeciesGetMaxHealth.argtypes = [c_void_p]

library.fishSpeciesGetMaxMovement.restype = c_int
library.fishSpeciesGetMaxMovement.argtypes = [c_void_p]

library.fishSpeciesGetCarryCap.restype = c_int
library.fishSpeciesGetCarryCap.argtypes = [c_void_p]

library.fishSpeciesGetAttackPower.restype = c_int
library.fishSpeciesGetAttackPower.argtypes = [c_void_p]

library.fishSpeciesGetRange.restype = c_int
library.fishSpeciesGetRange.argtypes = [c_void_p]

library.fishSpeciesGetMaxAttacks.restype = c_int
library.fishSpeciesGetMaxAttacks.argtypes = [c_void_p]

library.fishSpeciesGetTurnsTillAvailalbe.restype = c_int
library.fishSpeciesGetTurnsTillAvailalbe.argtypes = [c_void_p]

library.fishSpeciesGetTurnsTillUnavailable.restype = c_int
library.fishSpeciesGetTurnsTillUnavailable.argtypes = [c_void_p]

library.tileGetId.restype = c_int
library.tileGetId.argtypes = [c_void_p]

library.tileGetX.restype = c_int
library.tileGetX.argtypes = [c_void_p]

library.tileGetY.restype = c_int
library.tileGetY.argtypes = [c_void_p]

library.tileGetTrashAmount.restype = c_int
library.tileGetTrashAmount.argtypes = [c_void_p]

library.tileGetOwner.restype = c_int
library.tileGetOwner.argtypes = [c_void_p]

library.tileGetIsCove.restype = c_int
library.tileGetIsCove.argtypes = [c_void_p]

library.fishGetId.restype = c_int
library.fishGetId.argtypes = [c_void_p]

library.fishGetX.restype = c_int
library.fishGetX.argtypes = [c_void_p]

library.fishGetY.restype = c_int
library.fishGetY.argtypes = [c_void_p]

library.fishGetOwner.restype = c_int
library.fishGetOwner.argtypes = [c_void_p]

library.fishGetMaxHealth.restype = c_int
library.fishGetMaxHealth.argtypes = [c_void_p]

library.fishGetCurrentHealth.restype = c_int
library.fishGetCurrentHealth.argtypes = [c_void_p]

library.fishGetMaxMovement.restype = c_int
library.fishGetMaxMovement.argtypes = [c_void_p]

library.fishGetMovementLeft.restype = c_int
library.fishGetMovementLeft.argtypes = [c_void_p]

library.fishGetCarryCap.restype = c_int
library.fishGetCarryCap.argtypes = [c_void_p]

library.fishGetCarryingWeight.restype = c_int
library.fishGetCarryingWeight.argtypes = [c_void_p]

library.fishGetAttackPower.restype = c_int
library.fishGetAttackPower.argtypes = [c_void_p]

library.fishGetIsVisible.restype = c_int
library.fishGetIsVisible.argtypes = [c_void_p]

library.fishGetMaxAttacks.restype = c_int
library.fishGetMaxAttacks.argtypes = [c_void_p]

library.fishGetAttacksLeft.restype = c_int
library.fishGetAttacksLeft.argtypes = [c_void_p]

library.fishGetRange.restype = c_int
library.fishGetRange.argtypes = [c_void_p]

library.fishGetSpecies.restype = c_char_p
library.fishGetSpecies.argtypes = [c_void_p]

library.playerGetId.restype = c_int
library.playerGetId.argtypes = [c_void_p]

library.playerGetPlayerName.restype = c_char_p
library.playerGetPlayerName.argtypes = [c_void_p]

library.playerGetTime.restype = c_float
library.playerGetTime.argtypes = [c_void_p]

library.playerGetCurrentReefHealth.restype = c_int
library.playerGetCurrentReefHealth.argtypes = [c_void_p]

library.playerGetSpawnFood.restype = c_int
library.playerGetSpawnFood.argtypes = [c_void_p]


#Properties
