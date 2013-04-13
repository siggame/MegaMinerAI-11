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
library.speciesSpawn.restype = c_int
library.speciesSpawn.argtypes = [c_void_p, c_void_p]

library.fishMove.restype = c_int
library.fishMove.argtypes = [c_void_p, c_int, c_int]

library.fishPickUp.restype = c_int
library.fishPickUp.argtypes = [c_void_p, c_void_p, c_int]

library.fishDrop.restype = c_int
library.fishDrop.argtypes = [c_void_p, c_void_p, c_int]

library.fishAttack.restype = c_int
library.fishAttack.argtypes = [c_void_p, c_void_p]

library.playerTalk.restype = c_int
library.playerTalk.argtypes = [c_void_p, c_char_p]

# accessors

#Globals
library.getMaxReefHealth.restype = c_int
library.getMaxReefHealth.argtypes = [c_void_p]

library.getBoundLength.restype = c_int
library.getBoundLength.argtypes = [c_void_p]

library.getTurnNumber.restype = c_int
library.getTurnNumber.argtypes = [c_void_p]

library.getPlayerID.restype = c_int
library.getPlayerID.argtypes = [c_void_p]

library.getGameNumber.restype = c_int
library.getGameNumber.argtypes = [c_void_p]

library.getMapWidth.restype = c_int
library.getMapWidth.argtypes = [c_void_p]

library.getMapHeight.restype = c_int
library.getMapHeight.argtypes = [c_void_p]

library.getTrashAmount.restype = c_int
library.getTrashAmount.argtypes = [c_void_p]

library.getCurrentSeason.restype = c_int
library.getCurrentSeason.argtypes = [c_void_p]

library.getSeasonLength.restype = c_int
library.getSeasonLength.argtypes = [c_void_p]

library.getHealPercent.restype = c_int
library.getHealPercent.argtypes = [c_void_p]

library.getMaxFood.restype = c_int
library.getMaxFood.argtypes = [c_void_p]

library.getMappable.restype = c_void_p
library.getMappable.argtypes = [c_void_p, c_int]

library.getMappableCount.restype = c_int
library.getMappableCount.argtypes = [c_void_p]

library.getTile.restype = c_void_p
library.getTile.argtypes = [c_void_p, c_int]

library.getTileCount.restype = c_int
library.getTileCount.argtypes = [c_void_p]

library.getSpecies.restype = c_void_p
library.getSpecies.argtypes = [c_void_p, c_int]

library.getSpeciesCount.restype = c_int
library.getSpeciesCount.argtypes = [c_void_p]

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

library.tileGetHasEgg.restype = c_int
library.tileGetHasEgg.argtypes = [c_void_p]

library.tileGetDamages.restype = c_int
library.tileGetDamages.argtypes = [c_void_p]

library.speciesGetId.restype = c_int
library.speciesGetId.argtypes = [c_void_p]

library.speciesGetName.restype = c_char_p
library.speciesGetName.argtypes = [c_void_p]

library.speciesGetIndex.restype = c_int
library.speciesGetIndex.argtypes = [c_void_p]

library.speciesGetCost.restype = c_int
library.speciesGetCost.argtypes = [c_void_p]

library.speciesGetMaxHealth.restype = c_int
library.speciesGetMaxHealth.argtypes = [c_void_p]

library.speciesGetMaxMovement.restype = c_int
library.speciesGetMaxMovement.argtypes = [c_void_p]

library.speciesGetCarryCap.restype = c_int
library.speciesGetCarryCap.argtypes = [c_void_p]

library.speciesGetAttackPower.restype = c_int
library.speciesGetAttackPower.argtypes = [c_void_p]

library.speciesGetRange.restype = c_int
library.speciesGetRange.argtypes = [c_void_p]

library.speciesGetMaxAttacks.restype = c_int
library.speciesGetMaxAttacks.argtypes = [c_void_p]

library.speciesGetSeason.restype = c_int
library.speciesGetSeason.argtypes = [c_void_p]

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

library.fishGetSpecies.restype = c_int
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
