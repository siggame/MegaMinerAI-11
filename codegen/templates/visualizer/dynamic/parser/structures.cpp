// -*-c++-*-

#include "structures.h"

#include <iostream>

namespace parser
{

% for model in models:

std::ostream& operator<<(std::ostream& stream, ${model.name} ob)
{
%   for datum in model.data:
  stream << "${datum.name}: " << ob.${datum.name}  <<'\n';
%   endfor
  return stream;
}

% endfor

% for animation in animations:

std::ostream& operator<<(std::ostream& stream, ${animation.name} ob)
{
  stream << "${animation.name}" << "\n";
%   for datum in animation.data:
  stream << "${datum.name}: " << ob.${datum.name}  <<'\n';
%   endfor
  return stream;
}

% endfor

std::ostream& operator<<(std::ostream& stream, GameState ob)
{
% for datum in globals:
  stream << "${datum.name}: " << ob.${datum.name}  <<'\n';
% endfor

% for model in models:
  stream << "\n\n${model.name}s:\n";
  for(std::map<int,${model.name}>::iterator i = ob.${lowercase(model.plural)}.begin(); i != ob.${lowercase(model.plural)}.end(); i++)
    stream << i->second << '\n';
% endfor
  stream << "\nAnimation\n";
  for
    (
    std::map< int, std::vector< SmartPointer< Animation > > >::iterator j = ob.animations.begin(); 
    j != ob.animations.end(); 
    j++ 
    )
  {
  for(std::vector< SmartPointer< Animation > >::iterator i = j->second.begin(); i != j->second.end(); i++)
  {
% for animation in animations:
//    if((*(*i)).type == ${animation.name.upper()})
//      stream << *((${animation.name}*)*i) << "\n";
% endfor
  }
  

  }
  return stream;
}

Game::Game()
{
  winner = -1;
}

} // parser
