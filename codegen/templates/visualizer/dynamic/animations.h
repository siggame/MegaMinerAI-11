#ifndef ANIMATIONS_H
#define ANIMATIONS_H

#include "${lowercase(gameName)}Animatable.h"

namespace visualizer
{

    struct StartAnim: public Anim
    {
      public:
        void animate( const float& t, AnimData *d, IGame* game );

    };
  
    class DrawSomething: public Anim
    {
        public:
            DrawSomething( Something* something ) { m_Something = something; }
            void animate( const float& t, AnimData* d, IGame* game );

            float controlDuration() const
            { return 0; }

            float totalDuration() const
            { return 0; }
        
        private:
            Something *m_Something;

    }; // DrawBackground
}

#endif // ANIMATION_H
