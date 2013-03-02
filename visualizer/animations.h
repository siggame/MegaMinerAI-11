#ifndef ANIMATIONS_H
#define ANIMATIONS_H

#include "reefAnimatable.h"

namespace visualizer
{

    struct StartAnim: public Anim
    {
      public:
        void animate( const float& t, AnimData *d, IGame* game );

    };

    class DrawAnimation : public Anim
    {
    public:
        DrawAnimation( SpriteAnimation* animation ) : m_animation(animation) {}
        void animate( const float& t, AnimData* d, IGame* game );

    private:
        SpriteAnimation* m_animation;
    };
  
    class DrawSomething: public Anim
    {
        public:
            DrawSomething( Something* something ) { m_Something = something; }
            void animate( const float& t, AnimData* d, IGame* game );
        
        private:
            Something *m_Something;

    }; // DrawBackground
}

#endif // ANIMATION_H
