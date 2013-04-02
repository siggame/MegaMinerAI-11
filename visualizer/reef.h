#ifndef REEF_H
#define REEF_H

#include <QObject>
#include <QThread>
#include <QElapsedTimer>
#include "igame.h"
#include "animsequence.h"
#include <map>
#include <string>
#include <list>
#include "reefAnimatable.h"

// The Codegen's Parser
#include "parser/parser.h"
#include "parser/structures.h"

using namespace std;

namespace visualizer
{
    struct Rect
    {
        int left;
        int top;
        int right;
        int bottom;
    };

    struct ReefPlayerInfo
    {
        ReefPlayerInfo(int health, int food, float t) : currentReefHealth(health), spawnFood(food), time(t) {}

        int currentReefHealth;
        int spawnFood;
        float time;
    };

    class Bubble
    {
    public:

        Bubble(const glm::vec2& pos, const Color& color, float speed,float angle, float maxAge) :
            m_pos(pos), m_color(color), m_fSpeed(speed), m_fAngle(angle), m_fAge(0.0f), m_fMaxAge(maxAge) {}

        bool Update(float dt)
        {
            glm::vec2 dir(cos(m_fAngle),-sin(m_fAngle));
            m_pos += m_fSpeed * dir * dt;

            m_fAge += dt;

            return m_fAge >= m_fMaxAge;
        }

        void Render(const IRenderer& renderer) const
        {
            renderer.setColor(m_color);
            renderer.drawTexturedQuad(m_pos.x,m_pos.y,1.0f,1.0f,"bubble");
        }

    private:
        glm::vec2 m_pos;
        Color m_color;
        float m_fSpeed;
        float m_fAngle;
        float m_fAge;
        float m_fMaxAge;
    };

    class Reef: public QThread, public AnimSequence, public IGame
    {
        Q_OBJECT;
        Q_INTERFACES( visualizer::IGame );
        public: 
            Reef();
            ~Reef();

            PluginInfo getPluginInfo();
            void loadGamelog( std::string gamelog );

            void run(); //main function
            void setup();
            void destroy();

            void preDraw();
            void postDraw();

            void addCurrentBoard();
    
            map<string, int> programs;
            
            list<int> getSelectedUnits();

             static const int SEA_OFFSET = 2;

        private:
            parser::Game *m_game;  // The Game Object from parser/structures.h that is generated by the Codegen
            QElapsedTimer m_WaterTimer;
            QElapsedTimer m_BubbleTimer;
            float m_fDt; // time differential between frames in seconds, this value is not accurate
            bool m_suicide;

            list<int> m_selectedUnitIDs;

            std::vector<ReefPlayerInfo> m_ReefPlayerInfo;

            std::vector<std::map<int,BasicTrash> > m_Trash;
            std::vector<std::vector<parser::Species> > m_Species;

            std::list<Bubble> m_Bubbles;

            void BuildWorld(class Map* pMap);

            void ProccessInput();

            void GetSelectedRect(Rect& out) const;

            void UpdateBubbles();

            void RenderWorld() const;

            void RenderObjectSelection() const;

            void RenderSpecies() const;

            void RenderPlayerInfo() const;

            void RenderBubbles() const;

            void RenderPlayerInfo(int id, float xPos = 1.0f) const;

            template< class T >
            bool DrawQuadAroundObj(const T& datastruct, const typename T::key_type& key) const
            {
              auto iter = datastruct.find(key);

              if(iter != datastruct.end())
              {
                const auto& obj = iter->second;

                renderer->setColor( Color( 1.0, 0.4, 0.4, 0.6 ) );
                renderer->drawQuad(obj.x,obj.y,1,1);
                return true;
              }

              return false;
            }
    }; 

} // visualizer

#endif // REEF_H
