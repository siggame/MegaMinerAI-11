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

% for i, animation in enumerate(animations):
const int ${animation.name.upper()} = ${i};
% endfor

% for model in models:
struct ${model.name}\
% if model.parent:
: public ${model.parent.name} \
% endif

{
%   for datum in model.data:
%     if not (model.parent and datum.name in [i.name for i in model.parent.data]):
%       if isinstance(datum.type, Model):
  int ${datum.name};
%       else:
  ${conversions[datum.type]} ${datum.name};
%       endif
%     endif
%   endfor

  friend std::ostream& operator<<(std::ostream& stream, ${model.name} obj);
};

% endfor

struct Animation
{
  int type;
};

% for animation in animations:
struct ${animation.name} : public Animation
{
%   for datum in animation.data:
%     if isinstance(datum.type, Model):
  int ${datum.name};
%     else:
  ${conversions[datum.type]} ${datum.name};
%     endif
%   endfor

  friend std::ostream& operator<<(std::ostream& stream, ${animation.name} obj);
};

% endfor

struct AnimOwner: public Animation
{
  int owner;
};

struct GameState
{
% for model in models:
  std::map<int,${model.name}> ${lowercase(model.plural)};
% endfor

% for datum in globals:
  ${conversions[datum.type]} ${datum.name};
% endfor

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
