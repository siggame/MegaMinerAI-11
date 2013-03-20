#ifndef REEF_ANIMATABLE_H
#define REEF_ANIMATABLE_H

#include "irenderer.h"
#include "parser/structures.h"

#include <glm/glm.hpp>
#include "math.h"

namespace visualizer
{
    // todo: remove this
    // class that stores the info about how a map is rendered
    class Map : public Animatable
    {
      public:

        struct Tile
        {
            Tile() : bCove(false), bEgg(false), spriteId(0)
            {
            }

            Tile(bool cove) : bCove(cove), bEgg(false), spriteId(0)
            {
            }

            bool bCove; // teh cove, need to make it look nice, this value does not change between frames
            bool bEgg; // teh egg
            int spriteId;

           // int turn;
           // todo: add more?
        };

        Map(int w, int h) : m_tiles(w*h), width(w), height(h)
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

        void AddTurn(int turn, const SmartPointer<struct TrashMovingInfo>& trash);

        int GetWidth() const { return width; }
        int GetHeight() const { return height; }
        float GetPrevMapColor() const { return prevMapColor; }
        float GetxPos() const { return xPos; }
        float GetMapColor() const { return mapColor; }

    private:

      std::vector<Tile> m_tiles;
      int width;
      int height;

      //todo: lighting
      float prevMapColor;
      float mapColor;
      float xPos;

        // todo: add more?
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

    struct BasicTrash
    {
        BasicTrash() : amount(0)
        {
        }

        BasicTrash(float xPos, float yPos, int iAmount) : x(xPos), y(yPos), amount(iAmount)
        {
        }

        float x;
        float y;
        int amount;
    };

    struct Trash : public Animatable, public BasicTrash
    {
        Trash(float xPos, float yPos, int iAmount) : BasicTrash(xPos, yPos, iAmount)
        {
        }
    };

    struct BaseSprite : public Animatable
    {
        BaseSprite(float posX, float posY, float dx, float dy, const string& s) :
            x(posX), y(posY), dx(dx), dy(dy), m_sprite(s)  {}

        float x;
        float y;
        float dx;
        float dy;
        string m_sprite;
    };

    // used for static non moving sprite animations
    struct SpriteAnimation : public BaseSprite
    {
        // todo: maybe reorder these
        SpriteAnimation(float posX, float posY, float dx, float dy ,const string& sprite, int f, const string& e = "") :
            BaseSprite(posX,posY,dx,dy,sprite), frames(f), enable(e) {}

        int frames;
        string enable; // used for enabling/disabling this sprite via gui
    };

    struct HUDInfo : public Animatable
    {
        explicit HUDInfo(int s) : season(s) {}

        int season;
    };

} // visualizer

#endif // REEF_ANIMATABLE_H
