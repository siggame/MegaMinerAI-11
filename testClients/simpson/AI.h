#ifndef AI_H
#define AI_H

#include "BaseAI.h"

///The class implementing gameplay logic.
class AI: public BaseAI
{
public:
  AI(Connection* c);
  virtual const char* username();
  virtual const char* password();
  virtual void init();
  virtual bool run();
  virtual void end();
  Tile& myGetTile(const int x, const int y);
  Fish& myGetFish(const int targetX, const int targetY);
  bool isValidLoc(const int x,const int y);
  bool isValidLoc(const int x,const int y,bool & isFish,bool & isTrash,int & trash);
  bool findPath(const int beginX, const int beginY,const int endX,const int endY,
              Fish & f);
};

#endif
