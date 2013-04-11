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


static bool parseMappable(Mappable& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseMappable.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseMappable.\n Parsing: " << *expression << endl;
    return false;
  }

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseMappable.\n Parsing: " << *expression << endl;
    return false;
  }

  object.y = atoi(sub->val);
  sub = sub->next;

  return true;

}
static bool parseTile(Tile& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.trashAmount = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.owner = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.hasEgg = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.damages = atoi(sub->val);
  sub = sub->next;

  return true;

}
static bool parseSpecies(Species& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.name = new char[strlen(sub->val)+1];
  strncpy(object.name, sub->val, strlen(sub->val));
  object.name[strlen(sub->val)] = 0;
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.index = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.cost = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxHealth = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxMovement = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.carryCap = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.attackPower = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.range = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxAttacks = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseSpecies.\n Parsing: " << *expression << endl;
    return false;
  }

  object.season = atoi(sub->val);
  sub = sub->next;

  return true;

}
static bool parseFish(Fish& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.owner = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxHealth = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.currentHealth = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxMovement = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.movementLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.carryCap = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.carryingWeight = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.attackPower = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.isVisible = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxAttacks = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.attacksLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.range = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseFish.\n Parsing: " << *expression << endl;
    return false;
  }

  object.species = new char[strlen(sub->val)+1];
  strncpy(object.species, sub->val, strlen(sub->val));
  object.species[strlen(sub->val)] = 0;
  sub = sub->next;

  return true;

}
static bool parsePlayer(Player& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.playerName = new char[strlen(sub->val)+1];
  strncpy(object.playerName, sub->val, strlen(sub->val));
  object.playerName[strlen(sub->val)] = 0;
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.time = atof(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.currentReefHealth = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.spawnFood = atoi(sub->val);
  sub = sub->next;

  return true;

}

static bool parseSpawn(spawn& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = SPAWN;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsespawn.\n Parsing: " << *expression << endl;
    return false;
  }
  object.playerID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsespawn.\n Parsing: " << *expression << endl;
    return false;
  }
  object.x = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsespawn.\n Parsing: " << *expression << endl;
    return false;
  }
  object.y = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsespawn.\n Parsing: " << *expression << endl;
    return false;
  }
  object.species = new char[strlen(sub->val)+1];
  strncpy(object.species, sub->val, strlen(sub->val));
  object.species[strlen(sub->val)] = 0;
  sub = sub->next;
  return true;

}
static bool parseMove(move& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = MOVE;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.fromX = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.fromY = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.toX = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.toY = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parsePickUp(pickUp& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = PICKUP;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsepickUp.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsepickUp.\n Parsing: " << *expression << endl;
    return false;
  }
  object.targetID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsepickUp.\n Parsing: " << *expression << endl;
    return false;
  }
  object.x = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsepickUp.\n Parsing: " << *expression << endl;
    return false;
  }
  object.y = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsepickUp.\n Parsing: " << *expression << endl;
    return false;
  }
  object.amount = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseDeath(death& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = DEATH;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsedeath.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseDrop(drop& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = DROP;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsedrop.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsedrop.\n Parsing: " << *expression << endl;
    return false;
  }
  object.targetID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsedrop.\n Parsing: " << *expression << endl;
    return false;
  }
  object.x = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsedrop.\n Parsing: " << *expression << endl;
    return false;
  }
  object.y = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsedrop.\n Parsing: " << *expression << endl;
    return false;
  }
  object.amount = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseAttack(attack& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = ATTACK;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parseattack.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parseattack.\n Parsing: " << *expression << endl;
    return false;
  }
  object.targetID = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseStealth(stealth& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = STEALTH;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsestealth.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parsePlayerTalk(playerTalk& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = PLAYERTALK;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parseplayerTalk.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parseplayerTalk.\n Parsing: " << *expression << endl;
    return false;
  }
  object.message = new char[strlen(sub->val)+1];
  strncpy(object.message, sub->val, strlen(sub->val));
  object.message[strlen(sub->val)] = 0;
  sub = sub->next;
  return true;

}
static bool parseDeStealth(deStealth& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = DESTEALTH;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsedeStealth.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  return true;

}

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
          if ( !sub ) return false;
          gs.maxReefHealth = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.boundLength = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.turnNumber = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.playerID = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.gameNumber = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.mapWidth = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.mapHeight = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.trashAmount = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.currentSeason = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.seasonLength = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.healPercent = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.maxFood = atoi(sub->val);
          sub = sub->next;
      }
      else if(string(sub->val) == "Mappable")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Mappable object;
          flag = parseMappable(object, sub);
          gs.mappables[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Tile")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Tile object;
          flag = parseTile(object, sub);
          gs.tiles[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Species")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Species object;
          flag = parseSpecies(object, sub);
          gs.speciesList[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Fish")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Fish object;
          flag = parseFish(object, sub);
          gs.fishes[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Player")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Player object;
          flag = parsePlayer(object, sub);
          gs.players[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
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
      if(string(ToLower( sub->val ) ) == "spawn")
      {
        SmartPointer<spawn> animation = new spawn;
        if ( !parseSpawn(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "move")
      {
        SmartPointer<move> animation = new move;
        if ( !parseMove(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "pick-up")
      {
        SmartPointer<pickUp> animation = new pickUp;
        if ( !parsePickUp(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "death")
      {
        SmartPointer<death> animation = new death;
        if ( !parseDeath(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "drop")
      {
        SmartPointer<drop> animation = new drop;
        if ( !parseDrop(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "attack")
      {
        SmartPointer<attack> animation = new attack;
        if ( !parseAttack(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "stealth")
      {
        SmartPointer<stealth> animation = new stealth;
        if ( !parseStealth(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "player-talk")
      {
        SmartPointer<playerTalk> animation = new playerTalk;
        if ( !parsePlayerTalk(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "de-stealth")
      {
        SmartPointer<deStealth> animation = new deStealth;
        if ( !parseDeStealth(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
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
