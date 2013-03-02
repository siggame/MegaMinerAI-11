//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that

#include "BaseAI.h"
#include "game.h"

namespace client
{

int BaseAI::boundLength()
{
  return getBoundLength(c);
}
int BaseAI::turnNumber()
{
  return getTurnNumber(c);
}
int BaseAI::playerID()
{
  return getPlayerID(c);
}
int BaseAI::gameNumber()
{
  return getGameNumber(c);
}
int BaseAI::trashDamage()
{
  return getTrashDamage(c);
}
int BaseAI::mapWidth()
{
  return getMapWidth(c);
}
int BaseAI::mapHeight()
{
  return getMapHeight(c);
}
int BaseAI::trashAmount()
{
  return getTrashAmount(c);
}
int BaseAI::currentSeason()
{
  return getCurrentSeason(c);
}
int BaseAI::seasonLength()
{
  return getSeasonLength(c);
}

bool BaseAI::startTurn()
{
  static bool initialized = false;
  int count = 0;
  count = getMappableCount(c);
  mappables.clear();
  mappables.resize(count);
  for(int i = 0; i < count; i++)
  {
    mappables[i] = Mappable(getMappable(c, i));
  }

  count = getSpeciesCount(c);
  species.clear();
  species.resize(count);
  for(int i = 0; i < count; i++)
  {
    species[i] = Species(getSpecies(c, i));
  }

  count = getTileCount(c);
  tiles.clear();
  tiles.resize(count);
  for(int i = 0; i < count; i++)
  {
    tiles[i] = Tile(getTile(c, i));
  }

  count = getFishCount(c);
  fishes.clear();
  fishes.resize(count);
  for(int i = 0; i < count; i++)
  {
    fishes[i] = Fish(getFish(c, i));
  }

  count = getPlayerCount(c);
  players.clear();
  players.resize(count);
  for(int i = 0; i < count; i++)
  {
    players[i] = Player(getPlayer(c, i));
  }

  if(!initialized)
  {
    initialized = true;
    init();
  }
  return run();
}

BaseAI::BaseAI(Connection* conn) : c(conn) {}
BaseAI::~BaseAI() {}

}
