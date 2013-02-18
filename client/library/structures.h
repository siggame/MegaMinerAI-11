//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

struct Connection;
struct _Mappable;
struct _Trash;
struct _Fish;
struct _Player;


struct _Mappable
{
  Connection* _c;
  int id;
  int x;
  int y;
};
struct _Trash
{
  Connection* _c;
  int id;
  int x;
  int y;
  int weight;
};
struct _Fish
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  char* species;
  int maxHealth;
  int curHealth;
  int maxMoves;
  int movementLeft;
  int carryCap;
  int carryWeight;
  int attackPower;
  int isVisible;
  int attacksLeft;
};
struct _Player
{
  Connection* _c;
  int id;
  char* playerName;
  float time;
  int curReefHealth;
  int sandDollars;
};

#endif
