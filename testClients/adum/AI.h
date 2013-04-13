#ifndef AI_H
#define AI_H

#include "BaseAI.h"
#include <vector>

#define nullptr NULL

struct VECTOR2D
{
	explicit VECTOR2D(int x = 0, int y = 0) : x(x), y(y) {}

	bool operator == (const VECTOR2D& other) const
	{
		return x == other.x && y == other.y;
	}
	bool operator != (const VECTOR2D& other) const
	{
		return !this->operator==(other);
	}

	VECTOR2D operator + (const VECTOR2D& other) const
	{
	  return VECTOR2D(x + other.x,y + other.y);
	}

	VECTOR2D& operator += (const VECTOR2D& other)
	{
	  x += other.x;
	  y += other.y;
	  return *this;
	}

	VECTOR2D operator - (const VECTOR2D& other) const
	{
	  return VECTOR2D(x - other.x,y - other.y);
	}

	VECTOR2D& operator -= (const VECTOR2D& other)
	{
	  x -= other.x;
	  y -= other.y;
	  return *this;
	}

	friend std::ostream& operator<<(std::ostream& output, const VECTOR2D& vec)
	{
	    output << "("<<vec.x<<","<<vec.y<<")";
	}

	int x;
	int y;
};

struct Tile2
{
	explicit Tile2(Tile* p = nullptr) : pObj(p), pNext(nullptr) {}

	Tile* pObj;
	Tile2* pNext;
	VECTOR2D pos;
	char list;
	float G;
	float F;
};

///The class implementing gameplay logic.
class AI: public BaseAI
{
public:
  AI(Connection* c);
  virtual const char* username();
  virtual const char* password();
  virtual void init();
  virtual bool run();
  virtual void end();

    // data members

	std::vector<Tile2> m_array;
	char m_currentList;

	// helper methods

	Tile2& TileAt(const VECTOR2D& pos)
	{
      return m_array[pos.x + pos.y* mapWidth()];
   }

	void UpdateAI();

	template< class T >
	void NearObject(T& list, const VECTOR2D& pos, VECTOR2D& out);

    // A* pathfinding
    template< class T >
	unsigned int FindPath(const VECTOR2D& from, const VECTOR2D& to, const T& heuristic, int iMaxPathLength, std::vector<VECTOR2D>& pathOut);

	void BuildMapArray()
   {
      m_array.clear();
      m_array.resize(mapWidth() * mapHeight());

      for(int i=0;i<tiles.size();i++)
      {
         TileAt(VECTOR2D(tiles[i].x(),tiles[i].y())) = Tile2(&tiles[i]);
      }
   }
};

//Thanks Bryce

#include <cfloat>
#include <cmath>
#include <vector>
#include <queue>

using namespace std;

class TileSorter
{
public:

	bool operator()(const Tile2* a,const Tile2* b) const
	{
		return a->F > b->F;
	}

};


// http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
class HeuristicFunctor
{
public:


  float operator()(const VECTOR2D& current, const VECTOR2D& from, const VECTOR2D& to) const
  {
    VECTOR2D d1 = current - to;
    VECTOR2D d2 = from - to;
    float cross = abs(d1.x*d2.y - d2.x*d1.y);
    return cross*0.001f;
  }

};

class HeuristicManhattanDistance
{
public:

  float operator()(const VECTOR2D& current, const VECTOR2D& from, const VECTOR2D& to) const
  {
    return (abs(current.x-to.x) + abs(current.y-to.y));
  }
};

float dist(const VECTOR2D& a, const VECTOR2D& b);

template< class T >
unsigned int AI::FindPath(const VECTOR2D& from, const VECTOR2D& to, const T& heuristic, int iMaxPathLength, std::vector<VECTOR2D>& pathOut)
{
	unsigned int total = 0;

	Tile2* pCurrentTile = &TileAt(from);
	pCurrentTile->pos = from;
	pCurrentTile->list = ++m_currentList;
	pCurrentTile->pNext = nullptr;
	pCurrentTile->G = 0;
	pCurrentTile->F = heuristic(from,from,to);

	priority_queue<Tile2*,std::vector<Tile2*>,TileSorter> fringe;
	fringe.push(pCurrentTile);

	const VECTOR2D nearNodes[4] =
	{
	  VECTOR2D(0,1),
	  VECTOR2D(0,-1),
	  VECTOR2D(-1,0),
	  VECTOR2D(1,0)
	};

	while((pCurrentTile->pos != to) && !fringe.empty() && (pCurrentTile->G < iMaxPathLength))
	{
	    for(unsigned int i = 0; i < 4; ++i)
		{
			VECTOR2D newPos = nearNodes[i] + pCurrentTile->pos;

			if(newPos.x < mapWidth() && newPos.y < mapHeight() && newPos.x >= 0 && newPos.y >= 0 )
			{
				Tile2& newTile = TileAt(newPos);

				// If the tile is walkable,
				// todo: clean this up
				// todo: create functor to change the behavior of seeing if this is a valid node to add
				bool bLookAtTile = newTile.pObj == nullptr || (newTile.pObj->owner() == playerID() && newTile.pObj->owner() == 2 && newTile.pObj->trashAmount() == 0);
				if((newPos == to) || (bLookAtTile && newTile.list != m_currentList))
				{
				    newTile.pos = newPos;
					newTile.list = m_currentList;
					newTile.G = pCurrentTile->G + 1;

					newTile.F = heuristic(newPos,from,to) + newTile.G;
					newTile.pNext = pCurrentTile;

					fringe.push(&newTile);
					total++;
				}
			}
		}

		fringe.pop();
		if(!fringe.empty())
		{
		  pCurrentTile = fringe.top();
		}

	}


	//if(pCurrentTile->pos == to)
	{
	  do
	  {
		  pathOut.push_back(pCurrentTile->pos);
		  pCurrentTile = pCurrentTile->pNext;

	  } while(pCurrentTile != nullptr);

	}

	return total;
}

template< class T >
void AI::NearObject(T& list, const VECTOR2D& pos, VECTOR2D& out)
{
	float fClosest = FLT_MAX;

	for(int i = 0; i < list.size(); i++)
	{
       	float fDistance = ::dist(VECTOR2D(pos.x,pos.y),VECTOR2D(list[i].x(),list[i].y()));
        if(fDistance < fClosest)
        {
            fClosest = fDistance;
            out = VECTOR2D(list[i].x(),list[i].y());
        }
	}
}
#endif
