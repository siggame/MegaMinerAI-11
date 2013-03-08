#include "animations.h"
#include "reef.h"

namespace visualizer
{

    void DrawMap::animate(const float& t, AnimData*, IGame* game)
    {

        game->renderer->setColor(Color(1.0f,.8f,1.0f,1.0f));

        // render each tile on the map
        for (int x = 0; x < m_Map->GetWidth(); x++)
        {
          for (int y = 0; y < m_Map->GetHeight(); y++)
          {
              Map::Tile& tile = (*m_Map)(y,x);

              if(tile.isCove > 0)
              {
                  game->renderer->drawAnimQuad(x,y,1,1,"coral",tile.spriteId);
              }
              else
              {

              }
          }
        }

        // todo: change the direction of the water based on time
        float fSeconds = timer.elapsed() / 1000.0f * game->options->getNumber("Enable Water Animation");
        float fTransparency = (float)game->options->getNumber("Water Transparency Level") / 100.0f;

        // blend water map ontop of all the tiles
        game->renderer->setColor(Color(1.0,1.0f,1.0f,fTransparency));
        game->renderer->drawSubTexturedQuad(0,0,m_Map->GetWidth(),m_Map->GetHeight(),(fSeconds)/53.0f,-(fSeconds)/53.0f,1.0f,1.0f,"water");

    }

    void DrawAnimation::animate(const float& t, AnimData*, IGame* game )
    {

        if(m_animation->enable.empty() || game->options->getNumber(m_animation->enable) > 0.0f)
        {
            game->renderer->setColor( Color(1.0f,1.0f,1.0f,1.0f) );
            game->renderer->drawAnimQuad( m_animation->x, m_animation->y, m_animation->dx, m_animation->dy, m_animation->animation , (int)(m_animation->frames * t));
        }

    }


    void DrawFish::animate(const float &t, AnimData *d, IGame *game)
    {
      game->renderer->setColor( Color( 1, 1, 0, 1 ) );

      unsigned int index = (unsigned int)(m_Fish->m_moves.size() * t);
      float subT = m_Fish->m_moves.size() * t - index;

      glm::vec2 pos = m_Fish->m_moves[index].from + (m_Fish->m_moves[index].to - m_Fish->m_moves[index].from) * subT;

      //game->renderer->drawQuad(pos.x,pos.y,0.01f,0.01f);
      game->renderer->drawTexturedQuad(pos.x,pos.y,1,1,"fish");
      //game->renderer->drawText(pos.x,pos.y,"Roboto","fish");
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

