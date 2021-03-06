#include "animations.h"
#include "reef.h"

#include <iomanip>

namespace visualizer
{
    void RenderProgressBar(const IRenderer& renderer,
                           float xPos, float yPos,
                           float width, float height,
                           float percent, const Color& col, bool bDrawText)
    {
        // Render the health bars
        renderer.setColor(Color(0.0f,0.0f,0.0f,1.0f));
        renderer.drawQuad(xPos + width,yPos, -(1.0f - percent) * width, height); // height

        renderer.setColor(col);
        renderer.drawQuad(xPos,yPos, percent * width, height);

        if(bDrawText)
        {
            ostringstream stream;
            stream << fixed << setprecision(2) << percent * 100 << '%';

            float middle = (xPos + (width / 2.0f));
            renderer.setColor(Color(1.0f,1.0f,1.0f,1.0f));
            renderer.drawText(middle,yPos - 0.1f,"Roboto",stream.str(),5.0f*height,IRenderer::Center);
        }

    }


   /* void DrawMap::animate(const float& t, AnimData*, IGame* game)
    {
        // render each tile on the map
        int y = m_Map->GetHeight() - 1;
        for (int x = 0; x < m_Map->GetWidth(); x++)
        {
            game->renderer->drawTexturedQuad(x,y,1,1,"ocean_floor");
        }
        for (int x = 0; x < m_Map->GetWidth(); x++)
        {
          for (int y = 0; y < m_Map->GetHeight(); y++)
          {
              if(tile.bCove)
              {
                  Map::Tile& tile = (*m_Map)(y,x);

                  game->renderer->drawAnimQuad(x,y,1,1,"coral",tile.spriteId);
              }
          }
        }
    }*/
    void DrawSprite::animate(const float &t, AnimData *d, IGame *game)
    {
        game->renderer->setColor( Color(1.0f,1.0f,1.0f,1.0f) );
        game->renderer->drawTexturedQuad(m_sprite->pos.x, m_sprite->pos.y, m_sprite->scale.x, m_sprite->scale.y,m_sprite->m_sprite);
    }

    void DrawAnimation::animate(const float& t, AnimData*, IGame* game )
    {
        if(m_animation->enable.empty() || game->options->getNumber(m_animation->enable) > 0.0f)
        {
            game->renderer->setColor( Color(1.0f,1.0f,1.0f,1.0f) );
            game->renderer->drawAnimQuad( m_animation->pos.x, m_animation->pos.y, m_animation->scale.x, m_animation->scale.y, m_animation->m_sprite , (int)(m_animation->frames * t));
        }
    }

    void DrawMovingAnimation::animate(const float& t, AnimData*, IGame* game )
    {
        if(m_animation->enable.empty() || game->options->getNumber(m_animation->enable) > 0.0f)
        {
            glm::vec2 dir = (m_animation->pos - m_animation->source);
            glm::vec2 newPos = m_animation->source + dir * t;

            //cout<<"x: " << newPos.x << endl << "y: " << newPos.y << endl;

            game->renderer->setColor( Color(1.0f,1.0f,1.0f,1.0f) );
            game->renderer->drawAnimQuad( newPos.x, newPos.y, m_animation->scale.x, m_animation->scale.y, m_animation->m_sprite , (int)(m_animation->frames * t));
        }
    }


    void DrawFish::animate(const float &t, AnimData *d, IGame *game)
    {
        unsigned int index = (unsigned int)(m_Fish->m_moves.size() * t);
        float subT = m_Fish->m_moves.size() * t - index;

        glm::vec2 diff = m_Fish->m_moves[index].to - m_Fish->m_moves[index].from;
        glm::vec2 pos = m_Fish->m_moves[index].from + diff * subT;

        // todo: we could just combine all of these sprites into a sprite sheet
        game->renderer->setColor( GetTeamColor(m_Fish->owner) );
        game->renderer->drawTexturedQuad(pos.x,pos.y,1.0f,1.0f,
                                         (*m_Fish->speciesList)[m_Fish->species],
                                         m_Fish->flipped || (diff.x > 0.0f));

        if(m_Fish->carryingWeight > 0)
        {
            ostringstream stream;
            stream << m_Fish->carryingWeight;
            game->renderer->setColor( Color(1.0f,1.0f,1.0f,1.0f) );
            game->renderer->drawText(pos.x,pos.y,"Roboto",stream.str(),2.5f); // 3.0f
        }

        RenderProgressBar(*game->renderer,pos.x,pos.y - 0.2f,
                          0.8f,0.2f,(float)m_Fish->currentHealth / (float)m_Fish->maxHealth,
                          Color(0.8f,0.1f,0.1f,1.0f));
    }

    void DrawTrash::animate(const float &t, AnimData *d, IGame *game)
    {
        /*if((m_Trash->moveTurn == game->timeManager->getTurn()) && t < 0.8f)
            return;*/

        // todo: someone needs to make the trash get darker based on the amount of trash
        game->renderer->setColor( Color( 1.0f, 1.0f, 1.0f, 1.0f ) );
        game->renderer->drawTexturedQuad(m_Trash->x,m_Trash->y,1,1,"trash");

        stringstream stream;
        stream << m_Trash->amount;
        game->renderer->setColor( Color( 1.0f, 1.0f, 0.0f, 1.0f ) );
        game->renderer->drawText(m_Trash->x,m_Trash->y,"Roboto",stream.str(),3.0f);

    }

    void DrawSplashScreen::animate(const float &t, AnimData *d, IGame *game)
    {
        game->renderer->setColor(Color(1.0f,1.0f,1.0f,t));

        game->renderer->drawQuad(0.0f,0.0f,m_SplashScreen->width,m_SplashScreen->height);

        game->renderer->setColor(Color(0.2f,1.0f,1.0f,1.0f));
        game->renderer->drawText(m_SplashScreen->width / 2.0f,
                                 m_SplashScreen->height / 2.0f,
                                 "Roboto",
                                 m_SplashScreen->winReason,8.0f,
                                 IRenderer::Center);
    }

}

