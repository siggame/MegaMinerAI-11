//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef VC_STRUCTURES_H
#define VC_STRUCTURES_H

namespace client
{

struct Connection;
%  for model in models:
struct _${model.name};
%  endfor


% for model in models:
struct _${model.name}
{
  Connection* _c;
%  for datum in model.data:
  ${conversions[datum.type]} ${datum.name};
%  endfor
};
% endfor

}

#endif
