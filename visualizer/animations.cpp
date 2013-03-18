#include "animations.h"
#include "reef.h"

#include <assert.h>

namespace visualizer
{

    void DrawMap::animate(const float& t, AnimData*, IGame* game)
    {
        // draw a blue background
        game->renderer->setColor(Color(0.0f,0.0f,1.0f,1.0f));
        game->renderer->drawQuad(0.0f,0.0f,m_Map->GetWidth(),m_Map->GetHeight());

        game->renderer->setColor(Color(1.0f,.8f,1.0f,1.0f));

        // render each tile on the map
        for (int x = 0; x < m_Map->GetWidth(); x++)
        {
          for (int y = 0; y < m_Map->GetHeight(); y++)
          {
              Map::Tile& tile = (*m_Map)(y,x);

              if(tile.bCove)
              {
                  game->renderer->drawAnimQuad(x,y,1,1,"coral",tile.spriteId);
              }
          }
        }
    }

    void DrawSprite::animate(const float &t, AnimData *d, IGame *game)
    {
        game->renderer->setColor( Color(1.0f,1.0f,1.0f,1.0f) );
        game->renderer->drawTexturedQuad(m_sprite->x, m_sprite->y, m_sprite->dx, m_sprite->dy,m_sprite->m_sprite);
    }

    void DrawAnimation::animate(const float& t, AnimData*, IGame* game )
    {

        if(m_animation->enable.empty() || game->options->getNumber(m_animation->enable) > 0.0f)
        {
            game->renderer->setColor( Color(1.0f,1.0f,1.0f,1.0f) );
            game->renderer->drawAnimQuad( m_animation->x, m_animation->y, m_animation->dx, m_animation->dy, m_animation->m_sprite , (int)(m_animation->frames * t));
        }

    }


    void DrawFish::animate(const float &t, AnimData *d, IGame *game)
    {
        game->renderer->setColor( Color( 1, 1, 1, 1 ) );

        unsigned int index = (unsigned int)(m_Fish->m_moves.size() * t);
        float subT = m_Fish->m_moves.size() * t - index;

        glm::vec2 pos = m_Fish->m_moves[index].from + (m_Fish->m_moves[index].to - m_Fish->m_moves[index].from) * subT;

        game->renderer->drawTexturedQuad(pos.x,pos.y,1,1,"fish");
    }
    
    void DrawTrash::animate(const float &t, AnimData *d, IGame *game)
    {
        //is this right?????
        game->renderer->setColor( Color( 0, 1, 1, 1 ) );
        game->renderer->drawTexturedQuad(pos.x,pos.y,1,1,"trash");
    }

    void DrawHUD::animate(const float &t, AnimData *d, IGame *game)
    {
        // todo: maybe this could go somewhere else

        static const string seasons[] = {"winter" , "spring", "summer", "fall"};
        static const glm::vec4 seasonsColor[] =
        {
            glm::vec4(1.0f,0.8f,0.8f,0.0f),
            glm::vec4(1.0f,0.49f,0.0f,0.0f),
            glm::vec4(1.0f,0.1f,0.1f,0.0f),
            glm::vec4(.8f,0.4f,0.5f,0.0f)
        };

        assert(m_pHud->season < 4);

        int currentS = (m_pHud->season /*+ 3*/) % 4;

        glClearColor(seasonsColor[currentS].x,seasonsColor[currentS].y,
                     seasonsColor[currentS].z,seasonsColor[currentS].w);

        stringstream stream;
        stream << "Current Season: " << seasons[currentS];

        // todo: maybe repos the text
        game->renderer->drawText(19.0f,19.5f,"Roboto",stream.str(),7.0f,IRenderer::Center);
    }
}

