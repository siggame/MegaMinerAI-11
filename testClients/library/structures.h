//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

struct Connection;
struct _Mappable;
struct _Tile;
struct _Species;
struct _Fish;
struct _Player;


struct _Mappable
{
  Connection* _c;
  int id;
  int x;
  int y;
};
struct _Tile
{
  Connection* _c;
  int id;
  int x;
  int y;
  int trashAmount;
  int owner;
  int hasEgg;
};
struct _Species
{
  Connection* _c;
  int id;
  char* name;
  int index;
  int cost;
  int maxHealth;
  int maxMovement;
  int carryCap;
  int attackPower;
  int range;
  int maxAttacks;
  int season;
};
struct _Fish
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int maxHealth;
  int currentHealth;
  int maxMovement;
  int movementLeft;
  int carryCap;
  int carryingWeight;
  int attackPower;
  int isVisible;
  int maxAttacks;
  int attacksLeft;
  int range;
  int species;
};
struct _Player
{
  Connection* _c;
  int id;
  char* playerName;
  float time;
  int currentReefHealth;
  int spawnFood;
};

#endif
