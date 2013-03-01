#ifndef REEF_ANIMATABLE_H
#define REEF_ANIMATABLE_H

//#include "reefAnimatable.h"
#include "irenderer.h"
#include "parser/structures.h"

#include <glm/glm.hpp>
#include "math.h"

namespace visualizer
{

    struct Tile : public Animatable
    {
        int trashAmount; // trash to be rendered
        int owner;       // needed?
        int isCove; // teh cove, need to make it look nice
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
