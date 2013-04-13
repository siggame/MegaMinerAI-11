#ifndef ANIMATIONS_H
#define ANIMATIONS_H

#include "reefAnimatable.h"

namespace visualizer
{
    // xPos: starting pos of where the healthbar gets rendered
    // yPos: ^
    // width: width of bar
    // height: height of bar
    // percent: rate of change between 0 and 1
    // col: color of the bar
    void RenderProgressBar(const IRenderer&,
                           float xPos, float yPos,
                           float width, float height,
                           float percent, const Color& col, bool bDrawText = false);

    struct StartAnim : public Anim
    {
      public:
        void animate( const float& t, AnimData *d, IGame* game );

    };

    class DrawSprite : public Anim
    {
    public:
        DrawSprite( BaseSprite* sprite ) : m_sprite(sprite) {}
        void animate( const float& t, AnimData* d, IGame* game );

    private:
        BaseSprite* m_sprite;
    };

    class DrawAnimation : public Anim
    {
    public:
        DrawAnimation( SpriteAnimation* animation ) : m_animation(animation) {}
        void animate( const float& t, AnimData* d, IGame* game );

    private:
        SpriteAnimation* m_animation;
    };

    class DrawMovingAnimation : public Anim
    {
    public:
        DrawMovingAnimation( MovingSpriteAnimation* animation ) : m_animation(animation) {}
        void animate( const float& t, AnimData* d, IGame* game );

    private:
        MovingSpriteAnimation* m_animation;
    };

    class DrawFish : public Anim
    {
    public:
        DrawFish(Fish* fish) : m_Fish(fish) {}

        void animate(const float &t, AnimData *d, IGame *game);

    private:
        Fish* m_Fish;
    };//DrawFish
    
    class DrawTrash : public Anim
    {
    public:
        DrawTrash(Trash* trash) : m_Trash(trash) {}
        
        void animate(const float &t, AnimData *d, IGame *game);
        
    private:
        Trash *m_Trash;
    };//DrawTrash

    class DrawSplashScreen : public Anim
    {
    public:

        DrawSplashScreen(SplashScreen* screen) : m_SplashScreen(screen) {}

        void animate(const float &t, AnimData *d, IGame *game);

    private:
        SplashScreen* m_SplashScreen;
    };



}

#endif // ANIMATION_H
