#ifndef REEF_ANIMATABLE_H
#define REEF_ANIMATABLE_H

#include "irenderer.h"
#include "parser/structures.h"

#include <glm/glm.hpp>
#include "math.h"

namespace visualizer
{
    // class that stores the info about how a map is rendered
    class Map : public Animatable
    {
      public:

        struct Tile
        {
            Tile() : trashAmount(0), isCove(0), hasEgg(0), spriteId(0)
            {
            }

            Tile(int ta, int ic) : trashAmount(ta), isCove(ic)
            {
            }

            int trashAmount; // trash to be rendered, this value would change based off of the game being played
            int isCove; // teh cove, need to make it look nice, this value does not change between frames
            int hasEgg; // teh egg
            int spriteId;

           // int turn;
           // todo: add more?
        };

        Map(int w, int h, int turns) : m_tiles(w*h), m_updaters(turns), width(w), height(h)
        {
        }

        // todo: need to create a better interface
        Tile& operator()(unsigned int r, unsigned int c)
        {
          return m_tiles[c + r*width];
        }

        const Tile& operator()(unsigned int r, unsigned int c) const
        {
          return m_tiles[c + r*width];
        }

        void Update(int turn);

        void AddTurn(int turn, const SmartPointer<struct TrashMovingInfo>& trash);

        int GetWidth() const;
        int GetHeight() const;
        float GetPrevMapColor() const;
        float GetxPos() const;
        float GetMapColor() const;

    private:

      std::vector<Tile> m_tiles;
      std::vector<std::vector<SmartPointer<struct TrashMovingInfo> > > m_updaters; // stupid C++
      int width;
      int height;

      //todo: lighting
      float prevMapColor;
      float mapColor;
      float xPos;

        // todo: add more?
    };

    // todo: rename this struct
    struct TrashMovingInfo : public Animatable
    {
        TrashMovingInfo() : x(0), y(0), amount(0), active(true) {}

        int x;
        int y;
        int amount;

        SmartPointer<Map> m_map;
        bool active;
    };

    struct Fish : public Animatable
    {
        struct Moves
        {
            Moves() {}
            Moves(const glm::vec2& t, const glm::vec2& f) : to(t), from(f)
            {
            }

            // todo: maybe rename these
            glm::vec2 to;
            glm::vec2 from;
        };

        int owner;          // color of the fish
        int maxHealth;      // would this effect the way the fish will be rendered?
        int currentHealth;  // A healthbar?
        int maxMovement;    //
        int movementLeft;   //
        int carryCap;       //
        int carryingWeight; //
        int attackPower;    //
        int isVisible;      //
        int maxAttacks;     //
        int attacksLeft;    //
        int range;          //
        char* species;      //

        std::vector<Moves> m_moves;

    };

    // used for static non moving sprite animations
    struct SpriteAnimation : public Animatable
    {
        // todo: maybe reorder these
        SpriteAnimation(float posX, float posY, int f, float dx, float dy,const string& a, const string& e = "") :
            x(posX), y(posY), frames(f), dx(dx), dy(dy), animation(a), enable(e) {}

        float x;
        float y;
        int frames;
        float dx;
        float dy;
        string animation;
        string enable; // used for enabling/disabling this sprite via gui
    };

} // visualizer

#endif // REEF_ANIMATABLE_H
