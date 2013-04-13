#ifndef REEF_ANIMATABLE_H
#define REEF_ANIMATABLE_H

#include "irenderer.h"
#include "parser/structures.h"

#include <glm/glm.hpp>
#include "math.h"

namespace visualizer
{
    inline Color GetTeamColor(int team)
    {
        return (team == 1) ? Color(1.0f,.1f,0.1f,1.0f) : Color(0.1f,0.4f,0.1f,1.0f);
    }

    struct Fish : public Animatable
    {
        // todo: maybe use the ctor for more init
        Fish() : flipped(false) {}

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
        //int maxMovement;    //
        //int movementLeft;   //
        //int carryCap;       //
        int carryingWeight; //
        //int attackPower;    //
        //int maxAttacks;     //
       // int attacksLeft;    //
        int range;          //
        int species;      //
        bool flipped;

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
        BaseSprite(const glm::vec2& pos, const glm::vec2& scale, const string& sprite) :
            pos(pos), scale(scale), m_sprite(sprite)  {}

        glm::vec2 pos;
        glm::vec2 scale;
        string m_sprite;
    };

    // used for static non moving sprite animations
    struct SpriteAnimation : public BaseSprite
    {
        // todo: maybe reorder these
        SpriteAnimation(const glm::vec2& pos, const glm::vec2& scale,const string& sprite, int f, const string& e = "") :
            BaseSprite(pos,scale,sprite), frames(f), enable(e) {}

        int frames;
        string enable; // used for enabling/disabling this sprite via gui
    };

    struct MovingSpriteAnimation : public SpriteAnimation
    {
        // todo: maybe reorder these
        MovingSpriteAnimation(const glm::vec2& source, const glm::vec2& target, const glm::vec2& scale,const string& sprite, int f, const string& e = "") :
            SpriteAnimation(target,scale,sprite,f,e), source(source) {}

        glm::vec2 source;

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
