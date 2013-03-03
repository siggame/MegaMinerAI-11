#ifndef REEF_ANIMATABLE_H
#define REEF_ANIMATABLE_H

//#include "reefAnimatable.h"
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
            Tile() : trashAmount(0), isCove(0), hasEgg(0)
            {
            }

            Tile(int ta, int ic) : trashAmount(ta), isCove(ic)
            {
            }

            int trashAmount; // trash to be rendered, this value would change based off of the game being played
            int isCove; // teh cove, need to make it look nice, this value does not change between frames
            int hasEgg; // teh egg

           // int turn;
           // todo: add more?
        };

        Map(int w, int h /*float pc, float mc, float xp*/) : m_tiles(w*h), width(w), height(h)/*, prevMapColor(pc), mapColor(mc), xPos(xp)*/
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

    struct Something: public Animatable
    {
    };

} // visualizer

#endif // REEF_ANIMATABLE_H
