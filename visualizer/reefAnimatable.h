#ifndef REEF_ANIMATABLE_H
#define REEF_ANIMATABLE_H

#include "irenderer.h"
#include "parser/structures.h"

#include <glm/glm.hpp>
#include "math.h"

namespace visualizer
{
    struct Fish : public Animatable
    {
        // todo: maybe use the ctor for more init
        Fish() : flipped(false), isVisible(true) {}

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

        // todo: need to remove some of these
        int owner;          // color of the fish
        int maxHealth;      // would this effect the way the fish will be rendered?
        int currentHealth;  // A healthbar?
        int maxMovement;    //
        int movementLeft;   //
        int carryCap;       //
        int carryingWeight; //
        //int attackPower;    //
        //int maxAttacks;     //
       // int attacksLeft;    //
        int range;          //
        int species;      //
        bool flipped;
        bool isVisible;      //

        SmartPointer<std::vector<string>> speciesList;

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
       // int moveTurn;
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

    struct SplashScreen : public Animatable
    {
        SplashScreen(const string& reason, const string& nam, int w, int h) :
            winReason(reason), name(nam), width(w), height(h) {}

        string winReason;
        string name;
        int width;
        int height;
    };


} // visualizer

#endif // REEF_ANIMATABLE_H
