//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#pragma warning(disable : 4996)

#include <string>
#include <cstring>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <fstream>
#include <memory>

#include "game.h"
#include "network.h"
#include "vc_structures.h"

#include "sexp/sfcompat.h"

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

#ifdef _WIN32
//Doh, namespace collision.
namespace Windows
{
    #include <Windows.h>
};
#else
#include <unistd.h>
#endif

#ifdef ENABLE_THREADS
#define LOCK(X) pthread_mutex_lock(X)
#define UNLOCK(X) pthread_mutex_unlock(X)
#else
#define LOCK(X)
#define UNLOCK(X)
#endif

using namespace std;

namespace client
{

DLLEXPORT Connection* createConnection()
{
  Connection* c = new Connection;
  c->socket = -1;
  #ifdef ENABLE_THREADS
  pthread_mutex_init(&c->mutex, NULL);
  #endif

% for datum in globals + constants:
  c->${datum.name} = 0;
% endfor
% for model in models:
%   if model.type == 'Model':
  c->${model.plural} = NULL;
  c->${model.name}Count = 0;
%   endif
% endfor
  return c;
}

DLLEXPORT void destroyConnection(Connection* c)
{
  #ifdef ENABLE_THREADS
  pthread_mutex_destroy(&c->mutex);
  #endif
% for model in models:
%   if model.type == 'Model':
  if(c->${model.plural})
  {
    for(int i = 0; i < c->${model.name}Count; i++)
    {
%   for datum in model.data:
%     if datum.type == str:
      delete[] c->${model.plural}[i].${datum.name};
%       endif
%     endfor
    }
    delete[] c->${model.plural};
  }
%   endif
% endfor
  delete c;
}

DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port)
{
  c->socket = open_server_connection(host, port);
  return c->socket + 1; //false if socket == -1
}

DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password)
{
  string expr = "(login \"";
  expr += username;
  expr += "\" \"";
  expr += password;
  expr +="\")";

  send_string(c->socket, expr.c_str());

  sexp_t* expression, *message;

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  message = expression->list;
  if(message->val == NULL || strcmp(message->val, "login-accepted") != 0)
  {
    cerr << "Unable to login to server" << endl;
    destroy_sexp(expression);
    return 0;
  }
  destroy_sexp(expression);
  return 1;
}

DLLEXPORT int createGame(Connection* c)
{
  sexp_t* expression, *number;

  send_string(c->socket, "(create-game)");

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  number = expression->list->next;
  c->gameNumber = atoi(number->val);
  destroy_sexp(expression);

  std::cout << "Creating game " << c->gameNumber << endl;

  c->playerID = 0;

  return c->gameNumber;
}

DLLEXPORT int joinGame(Connection* c, int gameNum, const char* playerType)
{
  sexp_t* expression;
  stringstream expr;

  c->gameNumber = gameNum;

  expr << "(join-game " << c->gameNumber << " "<< playerType << ")";
  send_string(c->socket, expr.str().c_str());

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  if(strcmp(expression->list->val, "join-accepted") != 0)
  {
    cerr << "Game " << c->gameNumber << " doesn't exist." << endl;
    destroy_sexp(expression);
    return 0;
  }
  destroy_sexp(expression);

  c->playerID = 1;
  send_string(c->socket, "(game-start)");

  return 1;
}

DLLEXPORT void endTurn(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(end-turn)");
  UNLOCK( &c->mutex );
}

DLLEXPORT void getStatus(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(game-status)");
  UNLOCK( &c->mutex );
}

% for model in models:
%   for func in model.functions:

DLLEXPORT int ${lowercase(model.name)}${capitalize(func.name)}(${conversions[model]} object\
%     for arg in func.arguments:
, \
${conversions[arg.type]} ${arg.name}\
%     endfor
)
{
  stringstream expr;
  expr << "(game-${dashify(func.name)} " << object->id
%     for arg in func.arguments:
%       if isinstance(arg.type, Model):
      << " " << ${arg.name}->id
%       elif arg.type == str:
      << " \"" << escape_string(${arg.name}) << "\""
%       else:
       << " " << ${arg.name}
%       endif
%     endfor
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  return 1;
}
%   endfor

%   for prop in model.properties:

DLLEXPORT ${conversions[prop.result]} ${lowercase(model.name)}${capitalize(prop.name)}(${conversions[model]} object\
%     for arg in prop.arguments:
, \
${conversions[arg.type]} ${arg.name}\
%     endfor
)
{
}
%   endfor
% endfor

//Utility functions for parsing data
% for model in models:
void parse${model.name}(Connection* c, _${model.name}* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

%   for datum in model.data:
%     if datum.type == int:
  object->${datum.name} = atoi(sub->val);
%     elif datum.type == float:
  object->${datum.name} = atof(sub->val);
%     elif datum.type == str:
  object->${datum.name} = new char[strlen(sub->val)+1];
  strncpy(object->${datum.name}, sub->val, strlen(sub->val));
  object->${datum.name}[strlen(sub->val)] = 0;
%     endif
  sub = sub->next;
%   endfor

}
% endfor

DLLEXPORT int networkLoop(Connection* c)
{
  while(true)
  {
    sexp_t* base, *expression, *sub, *subsub;

    char* message = rec_string(c->socket);
    string text = message;
    base = extract_sexpr(message);
    delete[] message;
    expression = base->list;
    if(expression->val != NULL && strcmp(expression->val, "game-winner") == 0)
    {
      expression = expression->next->next->next;
      int winnerID = atoi(expression->val);
      if(winnerID == c->playerID)
      {
        cout << "You win!" << endl << expression->next->val << endl;
      }
      else
      {
        cout << "You lose. :(" << endl << expression->next->val << endl;
      }
      stringstream expr;
      expr << "(request-log " << c->gameNumber << ")";
      send_string(c->socket, expr.str().c_str());
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "log") == 0)
    {
      ofstream out;
      stringstream filename;
      expression = expression->next;
      filename << expression->val;
      filename << ".gamelog";
      expression = expression->next;
      out.open(filename.str().c_str());
      if (out.good())
        out.write(expression->val, strlen(expression->val));
      else
        cerr << "Error : Could not create log." << endl;
      out.close();
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "game-accepted")==0)
    {
      char gameID[30];

      expression = expression->next;
      strcpy(gameID, expression->val);
      cout << "Created game " << gameID << endl;
    }
    else if(expression->val != NULL && strstr(expression->val, "denied"))
    {
      cout << expression->val << endl;
      cout << expression->next->val << endl;
    }
    else if(expression->val != NULL && strcmp(expression->val, "status") == 0)
    {
      while(expression->next != NULL)
      {
        expression = expression->next;
        sub = expression->list;
        if(string(sub->val) == "game")
        {
          sub = sub->next;
% for datum in globals:
%   if datum.type == int:
          c->${datum.name} = atoi(sub->val);
%   elif datum.type == float:
          c->${datum.name} = atof(sub->val);
%   elif datum.type == str:
          if(c->${datum.name}) delete[] c->${datum.name};
          c->${datum.name} = new char[strlen(sub->val)+1];
          strncpy(c->${datum.name}, sub->val, strlen(sub->val));
          c->${datum.name}[strlen(sub->val)] = 0;
%   endif
          sub = sub->next;

% endfor
        }
% for model in models:
%   if model.type == 'Model':
        else if(string(sub->val) == "${model.name}")
        {
          if(c->${model.plural})
          {
            for(int i = 0; i < c->${model.name}Count; i++)
            {
%     for datum in model.data:
%       if datum.type == str:
              delete[] c->${model.plural}[i].${datum.name};
%       endif
%     endfor
            }
            delete[] c->${model.plural};
          }
          c->${model.name}Count =  sexp_list_length(expression)-1; //-1 for the header
          c->${model.plural} = new _${model.name}[c->${model.name}Count];
          for(int i = 0; i < c->${model.name}Count; i++)
          {
            sub = sub->next;
            parse${model.name}(c, c->${model.plural}+i, sub);
          }
        }
%   endif
% endfor
      }
      destroy_sexp(base);
      return 1;
    }
    else
    {
#ifdef SHOW_WARNINGS
      cerr << "Unrecognized message: " << text << endl;
#endif
    }
    destroy_sexp(base);
  }
}

% for model in models:
%   if model.type == 'Model':
DLLEXPORT _${model.name}* get${model.name}(Connection* c, int num)
{
  return c->${model.plural} + num;
}
DLLEXPORT int get${model.name}Count(Connection* c)
{
  return c->${model.name}Count;
}

% endif
% endfor

% for datum in globals + constants:
DLLEXPORT ${conversions[datum.type]} get${capitalize(datum.name)}(Connection* c)
{
  return c->${datum.name};
}
% endfor

}
