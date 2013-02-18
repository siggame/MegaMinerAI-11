//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that

#include "BaseAI.h"
#include "game.h"

int BaseAI::dollarsPerTurn()
{
  return getDollarsPerTurn(c);
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
int BaseAI::turnsTillSpawn()
{
  return getTurnsTillSpawn(c);
}
int BaseAI::maxReefHealth()
{
  return getMaxReefHealth(c);
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

  count = getTrashCount(c);
  trashs.clear();
  trashs.resize(count);
  for(int i = 0; i < count; i++)
  {
    trashs[i] = Trash(getTrash(c, i));
  }

  count = getFishCount(c);
  fishs.clear();
  fishs.resize(count);
  for(int i = 0; i < count; i++)
  {
    fishs[i] = Fish(getFish(c, i));
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
