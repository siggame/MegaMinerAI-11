//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef BASEAI_H
#define BASEAI_H

#include <vector>
#include <ctime>
#include "game.h"

% for model in models:
#include "${model.name}.h"
% endfor

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of boiler-plate code out of the way
///The provided AI class does just that.
class BaseAI
{
protected:
  Connection* c;
% for model in models:
%   if model.type == 'Model':
  std::vector<${model.name}> ${lowercase(model.plural)};
%   endif
% endfor
public:
% for datum in globals + constants:
%   if datum.doc:
  ///${datum.doc}
%   endif
  ${conversions[datum.type]} ${datum.name}();
% endfor
  
  BaseAI(Connection* c);
  virtual ~BaseAI();
  ///
  ///Make this your username, which should be provided.
  virtual const char* username() = 0;
  ///
  ///Make this your password, which should be provided.
  virtual const char* password() = 0;
  ///
  ///This function is run once, before your first turn.
  virtual void init() = 0;
  ///
  ///This function is called each time it is your turn
  ///Return true to end your turn, return false to ask the server for updated information
  virtual bool run() = 0;
  ///
  ///This function is called after the last turn.
  virtual void end() = 0;


  bool startTurn();
};

#endif
