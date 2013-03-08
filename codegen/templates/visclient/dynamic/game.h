//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef GAME_H
#define GAME_H

#include "network.h"
#include "vc_structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)

#ifdef ENABLE_THREADS
#include "pthread.h"
#endif

#else
#define DLLEXPORT

#ifdef ENABLE_THREADS
#include <pthread.h>
#endif

#endif

namespace client
{

struct Connection
{
  int socket;
  
  #ifdef ENABLE_THREADS
  pthread_mutex_t mutex;
  #endif
  
% for datum in globals + constants:
  ${conversions[datum.type]} ${datum.name};
% endfor

% for model in models:
%   if model.type == 'Model':
  _${model.name}* ${model.plural};
  int ${model.name}Count;
%   endif
% endfor
};

#ifdef __cplusplus
extern "C"
{
#endif
  DLLEXPORT Connection* createConnection();
  DLLEXPORT void destroyConnection(Connection* c);
  DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port);

  DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password);
  DLLEXPORT int createGame(Connection* c);
  DLLEXPORT int joinGame(Connection* c, int id, const char* playerType);

  DLLEXPORT void endTurn(Connection* c);
  DLLEXPORT void getStatus(Connection* c);


//commands

% for model in models:
%   for func in model.functions:
  ///${func.doc}
  DLLEXPORT int ${lowercase(model.name)}${capitalize(func.name)}(${conversions[model]} object\
%     for arg in func.arguments:
, \
${conversions[arg.type]} ${arg.name}\
%     endfor
);
%   endfor
% endfor

//derived properties

% for model in models:
%   for prop in model.properties:
  ///${prop.doc}
  DLLEXPORT ${conversions[prop.result]} ${lowercase(model.name)}${capitalize(prop.name)}(${conversions[model]} object\
%     for arg in prop.arguments:
, \
${conversions[arg.type]} ${arg.name}\
%     endfor
);
%   endfor
% endfor


//accessors

% for datum in globals + constants:
DLLEXPORT ${conversions[datum.type]} get${capitalize(datum.name)}(Connection* c);
% endfor

% for model in models:
%   if model.type == 'Model':
DLLEXPORT _${model.name}* get${model.name}(Connection* c, int num);
DLLEXPORT int get${model.name}Count(Connection* c);

%   endif
% endfor


  DLLEXPORT int networkLoop(Connection* c);
#ifdef __cplusplus
}
#endif

}

#endif
