#include "animations.h"
#include "reef.h"

namespace visualizer
{

    void DrawAnimation::animate(const float& t, AnimData*, IGame* game )
    {

        if(m_animation->enable.empty() || game->options->getNumber(m_animation->enable) > 0.0f)
        {
            game->renderer->setColor( Color(1.0f,1.0f,1.0f,1.0f) );
            game->renderer->drawAnimQuad( m_animation->x, m_animation->y, m_animation->dx, m_animation->dy, m_animation->animation , (int)(m_animation->frames * t));
        }

    }

    void StartAnim::animate( const float& /* t */, AnimData * /* d */, IGame* /*game*/ )
    {
    }

    void DrawSomething::animate( const float& /*t*/, AnimData * /*d*/, IGame* game )
    {
        // Set the color to red
        game->renderer->setColor( Color( 1, 0, 0, 1 ) );
        // Draw a 2x2 rectangle at (1,1), with the top left corner of the screen being the origin
        game->renderer->drawQuad( 1, 1, 2, 2 );
    }
}

