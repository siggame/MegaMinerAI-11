
#include "reefAnimatable.h"

namespace visualizer
{

void Map::AddTurn(int turn, const SmartPointer<TrashMovingInfo>& trash)
{
    m_updaters[turn].push_back(trash);
}

void Map::Update(int turn)
{
    if(!m_updaters.empty())
    {
        int index = turn - 1;
        if(index >= 0 && index < m_updaters.size())
        {
            for(int i = 0; i < m_updaters[index].size(); ++i)
            {
               m_updaters[index][i]->active = true;
            }
        }
    }
}

int Map::GetWidth() const { return width; }
int Map::GetHeight() const { return height; }
float Map::GetPrevMapColor() const { return prevMapColor; }
float Map::GetxPos() const { return xPos; }
float Map::GetMapColor() const { return mapColor; }

}
