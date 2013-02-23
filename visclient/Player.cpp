// -*-c++-*-

#include "Player.h"
#include "game.h"


namespace client
{

Player::Player(_Player* pointer)
{
    ptr = (void*) pointer;
}

int Player::id()
{
  return ((_Player*)ptr)->id;
}

char* Player::playerName()
{
  return ((_Player*)ptr)->playerName;
}

float Player::time()
{
  return ((_Player*)ptr)->time;
}

int Player::currentReefHealth()
{
  return ((_Player*)ptr)->currentReefHealth;
}

int Player::spawnFood()
{
  return ((_Player*)ptr)->spawnFood;
}


int Player::talk(char* message)
{
  return playerTalk( (_Player*)ptr, message);
}



std::ostream& operator<<(std::ostream& stream,Player ob)
{
  stream << "id: " << ((_Player*)ob.ptr)->id  <<'\n';
  stream << "playerName: " << ((_Player*)ob.ptr)->playerName  <<'\n';
  stream << "time: " << ((_Player*)ob.ptr)->time  <<'\n';
  stream << "currentReefHealth: " << ((_Player*)ob.ptr)->currentReefHealth  <<'\n';
  stream << "spawnFood: " << ((_Player*)ob.ptr)->spawnFood  <<'\n';
  return stream;
}

}
