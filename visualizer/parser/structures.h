//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <iostream>
#include <vector>
#include <map>
#include <string>

#include "smartpointer.h"

namespace parser
{

const int SPAWN = 0;
const int MOVE = 1;
const int PICKUP = 2;
const int DEATH = 3;
const int DROP = 4;
const int ATTACK = 5;
const int PLAYERTALK = 6;

struct Mappable
{
  int id;
  int x;
  int y;

  friend std::ostream& operator<<(std::ostream& stream, Mappable obj);
};

struct Trash: public Mappable 
{
  int weight;

  friend std::ostream& operator<<(std::ostream& stream, Trash obj);
};

struct Fish: public Mappable 
{
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

  friend std::ostream& operator<<(std::ostream& stream, Fish obj);
};

struct Player
{
  int id;
  char* playerName;
  float time;
  int curReefHealth;
  int sandDollars;

  friend std::ostream& operator<<(std::ostream& stream, Player obj);
};


struct Animation
{
  int type;
};

struct spawn : public Animation
{
  int x;
  int y;

  friend std::ostream& operator<<(std::ostream& stream, spawn obj);
};

struct move : public Animation
{
  int actingID;
  int fromX;
  int fromY;
  int toX;
  int toY;

  friend std::ostream& operator<<(std::ostream& stream, move obj);
};

struct pickUp : public Animation
{
  int x;
  int y;
  int actingID;

  friend std::ostream& operator<<(std::ostream& stream, pickUp obj);
};

struct death : public Animation
{
  int actingID;

  friend std::ostream& operator<<(std::ostream& stream, death obj);
};

struct drop : public Animation
{
  int x;
  int y;
  int actingID;

  friend std::ostream& operator<<(std::ostream& stream, drop obj);
};

struct attack : public Animation
{
  int actingID;
  int targetID;

  friend std::ostream& operator<<(std::ostream& stream, attack obj);
};

struct playerTalk : public Animation
{
  int actingID;
  char* message;

  friend std::ostream& operator<<(std::ostream& stream, playerTalk obj);
};


struct AnimOwner: public Animation
{
  int owner;
};

struct GameState
{
  std::map<int,Mappable> mappables;
  std::map<int,Trash> trashs;
  std::map<int,Fish> fishs;
  std::map<int,Player> players;

  int dollarsPerTurn;
  int turnNumber;
  int playerID;
  int gameNumber;
  int turnsTillSpawn;
  int maxReefHealth;
  int trashDamage;
  int mapWidth;
  int mapHeight;

  std::map< int, std::vector< SmartPointer< Animation > > > animations;
  friend std::ostream& operator<<(std::ostream& stream, GameState obj);
};

struct Game
{
  std::vector<GameState> states;
  std::string players[2];
  int winner;
	std::string winReason;

  Game();
};

} // parser

#endif
