#ifndef SEXP_PARSER_H
#define SEXP_PARSER_H

#include "sexp.h"
#include <cstdio>

Sexp* parse();
void parseFile(FILE* in);
void parseString( const char* string );


#endif
