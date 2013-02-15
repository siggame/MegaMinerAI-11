// -*-c++-*-

#include "Player.h"
#include "game.h"


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

int Player::curReefHealth()
{
  return ((_Player*)ptr)->curReefHealth;
}

int Player::sandDollars()
{
  return ((_Player*)ptr)->sandDollars;
}


bool Player::talk(char* message)
{
  return playerTalk( (_Player*)ptr, message);
}



std::ostream& operator<<(std::ostream& stream,Player ob)
{
  stream << "id: " << ((_Player*)ob.ptr)->id  <<'\n';
  stream << "playerName: " << ((_Player*)ob.ptr)->playerName  <<'\n';
  stream << "time: " << ((_Player*)ob.ptr)->time  <<'\n';
  stream << "curReefHealth: " << ((_Player*)ob.ptr)->curReefHealth  <<'\n';
  stream << "sandDollars: " << ((_Player*)ob.ptr)->sandDollars  <<'\n';
  return stream;
}
