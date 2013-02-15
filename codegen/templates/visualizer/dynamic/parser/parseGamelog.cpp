#include "parser.h"
#include "sexp/sexp.h"
#include "sexp/parser.h"
#include "sexp/sfcompat.h"

#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <iostream>

using namespace std;

namespace parser
{

char *ToLower( char *str )
{
  for( int i = 0; i < strlen( str ); i++ )
  {
    str[ i ] = tolower( str[ i ] );
  }
  return str;
}


% for model in models:
static bool parse${model.name}(${model.name}& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

%   for datum in model.data:
  if ( !sub ) 
  {
    cerr << "Error in parse${model.name}.\n Parsing: " << *expression << endl;
    return false;
  }

%     if datum.type == int:
  object.${datum.name} = atoi(sub->val);
%     elif datum.type == float:
  object.${datum.name} = atof(sub->val);
%    elif datum.type == str:
  object.${datum.name} = new char[strlen(sub->val)+1];
  strncpy(object.${datum.name}, sub->val, strlen(sub->val));
  object.${datum.name}[strlen(sub->val)] = 0;
%    endif
  sub = sub->next;

%  endfor
  return true;

}
% endfor

% for animation in animations:
static bool parse${capitalize(animation.name)}(${animation.name}& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = ${animation.name.upper()};
  sub = expression->list->next;
%   for datum in animation.data:
  if( !sub ) 
  {
    cerr << "Error in parse${animation.name}.\n Parsing: " << *expression << endl;
    return false;
  }
%     if datum.type == int or isinstance(datum.type, Model):
  object.${datum.name} = atoi(sub->val);
%     elif datum.type == float:
  object.${datum.name} = atof(sub->val);
%    elif datum.type == str:
  object.${datum.name} = new char[strlen(sub->val)+1];
  strncpy(object.${datum.name}, sub->val, strlen(sub->val));
  object.${datum.name}[strlen(sub->val)] = 0;
%    endif
  sub = sub->next;
%  endfor
  return true;

}
% endfor

static bool parseSexp(Game& game, sexp_t* expression)
{
  sexp_t* sub, *subsub;
  if( !expression ) return false;
  expression = expression->list;
  if( !expression ) return false;
  if(expression->val != NULL && strcmp(expression->val, "status") == 0)
  {
    GameState gs;
    while(expression->next != NULL)
    {
      expression = expression->next;
      sub = expression->list;
      if ( !sub ) return false;
      if(string(sub->val) == "game")
      {
          sub = sub->next;
% for datum in globals:
          if ( !sub ) return false;
%   if datum.type == int:
          gs.${datum.name} = atoi(sub->val);
%   elif datum.type == float:
          gs.${datum.name} = atof(sub->val);
%   elif datum.type == str:
          if(c->${datum.name}) delete[] c->${datum.name};
          gs.${datum.name} = new char[strlen(sub->val)+1];
          strncpy(gs.${datum.name}, sub->val, strlen(sub->val));
          gs.${datum.name}[strlen(sub->val)] = 0;
%   endif
          sub = sub->next;
% endfor
      }
% for model in models:
      else if(string(sub->val) == "${model.name}")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          ${model.name} object;
          flag = parse${model.name}(object, sub);
          gs.${lowercase(model.plural)}[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
% endfor
    }
    game.states.push_back(gs);
  }
  else if(string(expression->val) == "animations")
  {
    std::map< int, std::vector< SmartPointer< Animation > > > animations;
    while(expression->next)
    {
      expression = expression->next;
      sub = expression->list;
      if ( !sub ) return false;
% for animation in animations:
      if(string(ToLower( sub->val ) ) == "${dashify(animation.name)}")
      {
        SmartPointer<${animation.name}> animation = new ${animation.name};
        if ( !parse${capitalize(animation.name)}(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
% endfor
    }
    game.states[game.states.size()-1].animations = animations;
  }
  else if(string(expression->val) == "ident")
  {
    expression = expression->next;
    if ( !expression ) return false;
    sub = expression->list;
    while(sub)
    {
      subsub = sub->list;
      if ( !subsub ) return false;
      int number = atoi(subsub->val);
      if(number >= 0)
      {
        subsub = subsub->next;
        if ( !subsub ) return false;
        subsub = subsub->next;
        if ( !subsub ) return false;
        game.players[number] = subsub->val;
      }
      sub = sub->next;
    }
  }
  else if(string(expression->val) == "game-winner")
  {
    expression = expression->next;
    if ( !expression ) return false;
    expression = expression->next;
    if ( !expression ) return false;
    expression = expression->next;
    if ( !expression ) return false;
    game.winner = atoi(expression->val);
		expression = expression->next;
		if( !expression ) return false;
		game.winReason = expression->val;
  }

  return true;
}


bool parseFile(Game& game, const char* filename)
{
  //bool value;
  FILE* in = fopen(filename, "r");
  //int size;
  if(!in)
    return false;

  parseFile(in);

  sexp_t* st = NULL;

  while((st = parse()))
  {
    if( !parseSexp(game, st) )
    {
      while(parse()); //empty the file, keep Lex happy.
      fclose(in);
      return false;
    }
    destroy_sexp(st);
  }

  fclose(in);

  return true;
}


bool parseGameFromString(Game& game, const char* string)
{

  parseString( string );

  sexp_t* st = NULL;

  while((st = parse()))
  {
    if( !parseSexp(game, st) )
    {
      while(parse()); //empty the file, keep Lex happy.
      return false;
    }
    destroy_sexp(st);
  }

  return true;
}

} // parser
