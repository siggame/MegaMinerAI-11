// -*-c++-*-

#include "structures.h"

#include <iostream>

namespace parser
{


std::ostream& operator<<(std::ostream& stream, Mappable ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Tile ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "trashAmount: " << ob.trashAmount  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "hasEgg: " << ob.hasEgg  <<'\n';
  stream << "damages: " << ob.damages  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Species ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "name: " << ob.name  <<'\n';
  stream << "speciesNum: " << ob.speciesNum  <<'\n';
  stream << "cost: " << ob.cost  <<'\n';
  stream << "maxHealth: " << ob.maxHealth  <<'\n';
  stream << "maxMovement: " << ob.maxMovement  <<'\n';
  stream << "carryCap: " << ob.carryCap  <<'\n';
  stream << "attackPower: " << ob.attackPower  <<'\n';
  stream << "range: " << ob.range  <<'\n';
  stream << "maxAttacks: " << ob.maxAttacks  <<'\n';
  stream << "season: " << ob.season  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Fish ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "maxHealth: " << ob.maxHealth  <<'\n';
  stream << "currentHealth: " << ob.currentHealth  <<'\n';
  stream << "maxMovement: " << ob.maxMovement  <<'\n';
  stream << "movementLeft: " << ob.movementLeft  <<'\n';
  stream << "carryCap: " << ob.carryCap  <<'\n';
  stream << "carryingWeight: " << ob.carryingWeight  <<'\n';
  stream << "attackPower: " << ob.attackPower  <<'\n';
  stream << "maxAttacks: " << ob.maxAttacks  <<'\n';
  stream << "attacksLeft: " << ob.attacksLeft  <<'\n';
  stream << "range: " << ob.range  <<'\n';
  stream << "species: " << ob.species  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Player ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "playerName: " << ob.playerName  <<'\n';
  stream << "time: " << ob.time  <<'\n';
  stream << "currentReefHealth: " << ob.currentReefHealth  <<'\n';
  stream << "spawnFood: " << ob.spawnFood  <<'\n';
  return stream;
}



std::ostream& operator<<(std::ostream& stream, spawn ob)
{
  stream << "spawn" << "\n";
  stream << "playerID: " << ob.playerID  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "species: " << ob.species  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, move ob)
{
  stream << "move" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "fromX: " << ob.fromX  <<'\n';
  stream << "fromY: " << ob.fromY  <<'\n';
  stream << "toX: " << ob.toX  <<'\n';
  stream << "toY: " << ob.toY  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, pickUp ob)
{
  stream << "pickUp" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "targetID: " << ob.targetID  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "amount: " << ob.amount  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, death ob)
{
  stream << "death" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, drop ob)
{
  stream << "drop" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "targetID: " << ob.targetID  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "amount: " << ob.amount  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, attack ob)
{
  stream << "attack" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "targetID: " << ob.targetID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, playerTalk ob)
{
  stream << "playerTalk" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "message: " << ob.message  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, GameState ob)
{
  stream << "maxReefHealth: " << ob.maxReefHealth  <<'\n';
  stream << "boundLength: " << ob.boundLength  <<'\n';
  stream << "turnNumber: " << ob.turnNumber  <<'\n';
  stream << "playerID: " << ob.playerID  <<'\n';
  stream << "gameNumber: " << ob.gameNumber  <<'\n';
  stream << "mapWidth: " << ob.mapWidth  <<'\n';
  stream << "mapHeight: " << ob.mapHeight  <<'\n';
  stream << "trashAmount: " << ob.trashAmount  <<'\n';
  stream << "currentSeason: " << ob.currentSeason  <<'\n';
  stream << "seasonLength: " << ob.seasonLength  <<'\n';
  stream << "healPercent: " << ob.healPercent  <<'\n';
  stream << "maxFood: " << ob.maxFood  <<'\n';

  stream << "\n\nMappables:\n";
  for(std::map<int,Mappable>::iterator i = ob.mappables.begin(); i != ob.mappables.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nTiles:\n";
  for(std::map<int,Tile>::iterator i = ob.tiles.begin(); i != ob.tiles.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nSpeciess:\n";
  for(std::map<int,Species>::iterator i = ob.speciesList.begin(); i != ob.speciesList.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nFishs:\n";
  for(std::map<int,Fish>::iterator i = ob.fishes.begin(); i != ob.fishes.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nPlayers:\n";
  for(std::map<int,Player>::iterator i = ob.players.begin(); i != ob.players.end(); i++)
    stream << i->second << '\n';
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
//    if((*(*i)).type == SPAWN)
//      stream << *((spawn*)*i) << "\n";
//    if((*(*i)).type == MOVE)
//      stream << *((move*)*i) << "\n";
//    if((*(*i)).type == PICKUP)
//      stream << *((pickUp*)*i) << "\n";
//    if((*(*i)).type == DEATH)
//      stream << *((death*)*i) << "\n";
//    if((*(*i)).type == DROP)
//      stream << *((drop*)*i) << "\n";
//    if((*(*i)).type == ATTACK)
//      stream << *((attack*)*i) << "\n";
//    if((*(*i)).type == PLAYERTALK)
//      stream << *((playerTalk*)*i) << "\n";
  }
  

  }
  return stream;
}

Game::Game()
{
  winner = -1;
}

} // parser
