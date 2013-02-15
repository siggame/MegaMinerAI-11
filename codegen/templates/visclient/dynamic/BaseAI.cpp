//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that

#include "BaseAI.h"
#include "game.h"

namespace client
{

% for datum in globals + constants:
${conversions[datum.type]} BaseAI::${datum.name}()
{
  return get${capitalize(datum.name)}(c);
}
% endfor

bool BaseAI::startTurn()
{
  static bool initialized = false;
  int count = 0;
% for model in models:
%   if model.type == 'Model':
  count = get${model.name}Count(c);
  ${lowercase(model.plural)}.clear();
  ${lowercase(model.plural)}.resize(count);
  for(int i = 0; i < count; i++)
  {
    ${lowercase(model.plural)}[i] = ${model.name}(get${model.name}(c, i));
  }

%   endif
% endfor
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
