//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

struct Connection;
struct _Mappable;
struct _FishSpecies;
struct _Tile;
struct _Fish;
struct _Player;


struct _Mappable
{
  Connection* _c;
  int id;
  int x;
  int y;
};
struct _FishSpecies
{
  Connection* _c;
  int id;
  char* species;
  int cost;
  int maxHealth;
  int maxMovement;
  int carryCap;
  int attackPower;
  int range;
};
struct _Tile
{
  Connection* _c;
  int id;
  int x;
  int y;
  int trashAmount;
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
  int carryWeight;
  int attackPower;
  int isVisible;
  int attacksLeft;
  int range;
  char* species;
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
