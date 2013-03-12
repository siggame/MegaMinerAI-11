#include "reef.h"
#include "reefAnimatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include <utility>
#include <time.h>
#include <list>

namespace visualizer
{
  Reef::Reef()
  {
    m_game = 0;
    m_suicide=false;

    m_WaterTimer.start();

    srand(time(0));
  } // Reef::Reef()

  Reef::~Reef()
  {
    destroy();
  }

  void Reef::destroy()
  {
    m_suicide=true;
    wait();
    animationEngine->registerGame(0, 0);

    clear();
    delete m_game;
    m_game = 0;
    
    // Clear your memory here
    
    programs.clear();

  } // Reef::~Reef()

  void Reef::preDraw()
  {
    const Input& input = gui->getInput();
    
    // Handle player input here
  }

  void Reef::postDraw()
  {
      // todo: change the direction of the water based on time?
      float fSeconds = m_WaterTimer.elapsed() / 1000.0f * options->getNumber("Enable Water Animation");
      float fTransparency = (float)options->getNumber("Water Transparency Level") / 100.0f;

      renderer->setColor(Color(1.0f,1.0f,1.0f,1.0f));
      for(unsigned int i = 0; i < m_game->states[0].mapWidth; ++i)
      {
        renderer->drawSubTexturedQuad(i,-2.0f,1.0f,2.0f,(fSeconds)/2.0f,0.0f,1,1,"waves");
      }

      //renderer->drawTexturedQuad(0,-2,m_game->states[0].mapWidth,2,"waves");

      // blend water map ontop of all the tiles
      renderer->setColor(Color(1.0,1.0f,1.0f,fTransparency));
      renderer->drawSubTexturedQuad(0,0,m_game->states[0].mapWidth,m_game->states[0].mapHeight,(fSeconds)/53.0f,-(fSeconds)/53.0f,1.0f,1.0f,"water");
  }


  PluginInfo Reef::getPluginInfo()
  {
    PluginInfo i;
    i.searchLength = 1000;
    i.gamelogRegexPattern = "Reef";
    i.returnFilename = false;
    i.spectateMode = false;
    i.pluginName = "MegaMinerAI: Reef Plugin";


    return i;
  } // PluginInfo Reef::getPluginInfo()

  void Reef::setup()
  {
    gui->checkForUpdate( "Reef", "./plugins/reef/checkList.md5", VERSION_FILE );
    options->loadOptionFile( "./plugins/reef/reef.xml", "reef" );
    resourceManager->loadResourceFile( "./plugins/reef/resources.r" );
  }
  
  // Give the Debug Info widget the selected object IDs in the Gamelog
  list<int> Reef::getSelectedUnits()
  {
    // TODO Selection logic
    return list<int>();  // return the empty list
  }

  void Reef::loadGamelog( std::string gamelog )
  {
    if(isRunning())
    {
      m_suicide = true;
      wait();
    }
    m_suicide = false;

    // BEGIN: Initial Setup
    setup();

    delete m_game;
    m_game = new parser::Game;

    if( !parser::parseGameFromString( *m_game, gamelog.c_str() ) )
    {
      delete m_game;
      m_game = 0;
      WARNING(
          "Cannot load gamelog, %s", 
          gamelog.c_str()
          );
    }
    // END: Initial Setup

    // Setup the renderer as a 4 x 4 map by default
    // TODO: Change board size to something useful
    renderer->setCamera( 0, 4, m_game->states[0].mapWidth, m_game->states[0].mapHeight+4);
    renderer->setGridDimensions( m_game->states[0].mapWidth, m_game->states[0].mapHeight+4 );
 
    start();
  } // Reef::loadGamelog()

  void Reef::BuildWorld(Map* pMap)
  {
      int coralHeight = 4* pMap->GetHeight() / 5;

      for (int x = 0; x < pMap->GetWidth(); x++)
      {
        for (int y = pMap->GetHeight() - 2; y >= coralHeight; y--)
        {
            Map::Tile& tile = (*pMap)(y,x);
            tile.isCove = rand() % 2;
            tile.spriteId = 2;
        }
      }

      for (int x = 0; x < pMap->GetWidth(); x++)
      {
         Map::Tile& tile = (*pMap)(pMap->GetHeight() - 1,x);
         tile.isCove = 1;
         tile.spriteId = rand() % 2;
      }

  }
  
  // The "main" function
  void Reef::run()
  {
    
    // Build the Debug Table's Headers
    QStringList header;
    header << "one" << "two" << "three";
    gui->setDebugHeader( header );
    timeManager->setNumTurns( 0 );

    animationEngine->registerGame(0, 0);

    SmartPointer<Map> pMap = new Map(m_game->states[0].mapWidth,m_game->states[0].mapHeight,m_game->states.size());
    pMap->addKeyFrame( new DrawMap( pMap ) );

    BuildWorld(pMap);

    for(auto iter = m_game->states[0].tiles.begin(); iter != m_game->states[0].tiles.end(); ++iter)
    {
        Map::Tile& tile = (*pMap)(iter->second.y,iter->second.x);

        // todo: make the ammount of trash do something else
        tile.trashAmount = iter->second.trashAmount % 4;
    }

    // Look through each turn in the gamelog
    for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
    {
      Frame turn;  // The frame that will be drawn

      turn.addAnimatable(pMap);

      // for each fish in the current turn
      for( auto& p : m_game->states[ state ].fishes )
      {
        SmartPointer<Fish> newFish = new Fish();

        // for each animation each fish has
        for(auto& j : m_game->states[state].animations[p.second.id])
        {
            if(j->type == parser::MOVE)
            {
                cout<<"Move!"<<endl;
                parser::move& move = (parser::move&)*j;
                newFish->m_moves.push_back(Fish::Moves(glm::vec2(move.toX, move.toY),glm::vec2(move.fromX, move.fromY)));
            }
            else if(j->type == parser::DROP || j->type == parser::PICKUP)
            {
                cout<<"Move Trash!"<<endl;
                SmartPointer<TrashMovingInfo> trashInfo = new TrashMovingInfo;
                trashInfo->m_map = pMap;

                if(j->type == parser::DROP)
                {
                    parser::drop& dropAnim = (parser::drop&)*j;
                    trashInfo->amount = dropAnim.amount;
                    trashInfo->x = dropAnim.x;
                    trashInfo->y = dropAnim.y;
                }
                else
                {
                    parser::pickUp& pickupAnim = (parser::pickUp&)*j;
                    trashInfo->amount = pickupAnim.amount;
                    trashInfo->x = pickupAnim.x;
                    trashInfo->y = pickupAnim.y;
                }
                trashInfo->addKeyFrame(new MapUpdater(trashInfo));
                pMap->AddTurn(state,trashInfo);
                turn.addAnimatable(trashInfo);

            }
        }

        if(newFish->m_moves.empty())
        {
            newFish->m_moves.push_back(Fish::Moves(glm::vec2(p.second.x, p.second.y),glm::vec2(p.second.x, p.second.y)));
        }

        newFish->owner = p.second.owner;
        newFish->maxHealth = p.second.maxHealth;
        newFish->currentHealth = p.second.currentHealth;
        newFish->maxMovement = p.second.maxMovement;
        newFish->movementLeft = p.second.movementLeft;
        newFish->carryCap = p.second.carryingWeight;
        newFish->attackPower = p.second.attackPower;
        newFish->isVisible = p.second.isVisible;
        newFish->maxAttacks = p.second.maxAttacks;
        newFish->attacksLeft = p.second.attacksLeft;
        newFish->range = p.second.range;
        newFish->species = p.second.species;

        newFish->addKeyFrame( new DrawFish( newFish ) );
        turn.addAnimatable(newFish);
        cout<<"created a fish! "<<newFish->m_moves[0].from.x<<endl;

     }


      animationEngine->buildAnimations(turn);
      addFrame(turn);
      
      // Register the game and begin playing delayed due to multithreading
      if(state > 5)
      {
        timeManager->setNumTurns(state - 5);
        animationEngine->registerGame( this, this );
        if(state == 6)
        {
          animationEngine->registerGame(this, this);
          timeManager->setTurn(0);
          timeManager->play();
        }
      }
      else
      {
        timeManager->setNumTurns(state);
        animationEngine->registerGame( this, this );
        animationEngine->registerGame(this, this);
        timeManager->setTurn(0);
        timeManager->play();
      }
    }
    
    if(!m_suicide)
    {
      timeManager->setNumTurns( m_game->states.size() );
      timeManager->play();
    }

  } // Reef::run()

} // visualizer

Q_EXPORT_PLUGIN2( Reef, visualizer::Reef );
