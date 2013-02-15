#ifndef PARSER_H
#define PARSER_H

#include "structures.h"

namespace parser
{

bool parseFile(Game& game, const char* filename);
bool parseGameFromString(Game& game, const char* string);

} // parser

#endif
