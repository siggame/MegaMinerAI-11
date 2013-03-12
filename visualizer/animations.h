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

    class DrawMap: public Anim
    {
        public:

        DrawMap( Map* map ) : m_Map(map) {}

        void animate( const float& t, AnimData* d, IGame* game );

        private:
            Map *m_Map;


    }; // DrawBackground

    class DrawFish: public Anim
    {
    public:
        DrawFish(Fish* fish) : m_Fish(fish) {}

        void animate(const float &t, AnimData *d, IGame *game);

    private:
        Fish* m_Fish;
    };//DrawFish

    class MapUpdater : public Anim
    {
    public:

        MapUpdater( TrashMovingInfo* info) : m_info(info)
        {
        }

        void animate( const float& t, AnimData* d, IGame* game );

    private:

        TrashMovingInfo* m_info;

    };
}

#endif // ANIMATION_H
