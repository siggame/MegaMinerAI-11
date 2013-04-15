#ifndef AI_H
#define AI_H

#include "BaseAI.h"

///The class implementing gameplay logic.
class AI: public BaseAI
{
public:
  #ifdef _WIN32
	enum speciesIndex { SEA_STAR, SPONGE, ANGELFISH, CONESHELL_SNAIL, SEA_URCHIN, OCTOPUS, TOMCOD, REEF_SHARK, CUTTLEFISH, CLEANER_SHRIMP, ELECTRIC_EEL, JELLYFISH };
  #endif

  AI(Connection* c);
  virtual const char* username();
  virtual const char* password();
  virtual void init();
  virtual bool run();
  virtual void end();
};

#endif
