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

  void Reef::GetSelectedRect(Rect& R) const
    {
      const Input& input = gui->getInput();

      // offset the input

      int x = input.x;
      int y = input.y - SEA_OFFSET;
      int width = input.sx - x;
      int height = input.sy - y - SEA_OFFSET;

      int right = x + width;
      int bottom = y + height;

      R.left = min(x,right);
      R.top = min(y,bottom);
      R.right = max(x,right);
      R.bottom = max(y,bottom);
    }

  void Reef::preDraw()
  {
      const Input& input = gui->getInput();
      if( input.leftRelease )
      {
          int turn = timeManager->getTurn();

          Rect R;
          GetSelectedRect(R);

          m_selectedUnitIDs.clear();

          for(unsigned int i = 0; i < m_Trash.size(); ++i)
          {
              if(m_Trash[turn][i].trashAmount > 0)
              {
                  // todo: move this logic into another function
                  if(R.left <= m_Trash[turn][i].x && R.right >= m_Trash[turn][i].x && R.top <= m_Trash[turn][i].y && R.bottom >= m_Trash[turn][i].y)
                  {
                      m_selectedUnitIDs.push_back(m_Trash[turn][i].id);
                  }
              }
          }

          for(auto& iter : m_game->states[ turn ].fishes)
          {
              const auto& obj = iter.second;

              // todo: move this logic into another function
              if(R.left <= obj.x && R.right >= obj.x && R.top <= obj.y && R.bottom >= obj.y)
              {
                  m_selectedUnitIDs.push_back(obj.id);
              }
          }

          cout<<"Selected Units:" << m_selectedUnitIDs.size() << endl;
      }
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
    return m_selectedUnitIDs;
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
    renderer->setCamera( 0, SEA_OFFSET, m_game->states[0].mapWidth, m_game->states[0].mapHeight+SEA_OFFSET);
    renderer->setGridDimensions( m_game->states[0].mapWidth, m_game->states[0].mapHeight+SEA_OFFSET );
 
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
    header << "Owner" << "Type" << "Trash Amount" << "X" << "Y";
    gui->setDebugHeader( header );
    timeManager->setNumTurns( 0 );

    animationEngine->registerGame(0, 0);

    SmartPointer<Map> pMap = new Map(m_game->states[0].mapWidth,m_game->states[0].mapHeight);
    pMap->addKeyFrame( new DrawMap( pMap ) );

    BuildWorld(pMap);

    m_Trash.resize(m_game->states.size());

    // Look through each turn in the gamelog
    for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
    {
      Frame turn;  // The frame that will be drawn

      // todo: remove this from each frame
      turn.addAnimatable(pMap);

      if(state > 0)
      {
        m_Trash[state] = m_Trash[state - 1];
      }

      // for each fish in the current turn
      for( auto& p : m_game->states[ state ].fishes )
      {
        SmartPointer<Fish> newFish = new Fish();

        // for each animation each fish has
        for(auto& j : m_game->states[state].animations[p.second.id])
        {
            if(j->type == parser::MOVE)
            {
                //cout<<"Move!"<<endl;
                parser::move& move = (parser::move&)*j;
                newFish->m_moves.push_back(Fish::Moves(glm::vec2(move.toX, move.toY),glm::vec2(move.fromX, move.fromY)));
            }
            else if(j->type == parser::DROP || j->type == parser::PICKUP)
            {
                cout<<"Move Trash!"<<endl;

                if(j->type == parser::DROP)
                {
                    parser::drop& dropAnim = (parser::drop&)*j;

                    // todo: do something with the drop
                }
                else
                {
                    parser::pickUp& pickupAnim = (parser::pickUp&)*j;

                    // todo: do something with the pickup

                }

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

        turn[p.second.id]["Owner"] = p.second.owner;
        turn[p.second.id]["Type"] = "fish";
        turn[p.second.id]["X"] = p.second.x;
        turn[p.second.id]["Y"] = p.second.y;

        newFish->addKeyFrame( new DrawFish( newFish ) );
        turn.addAnimatable(newFish);
        //cout<<"created a fish! "<<newFish->m_moves[0].from.x<<endl;

     }

      // If the tiles are not empty
      if(!m_game->states[state].tiles.empty())
      {
          bool cleared = false;
          for(auto iter = m_game->states[state].tiles.begin(); iter != m_game->states[state].tiles.end(); ++iter)
          {
              // if there is trash
              if(iter->second.trashAmount > 0)
              {
                  Trash trash;
                  trash.id = iter->second.id;
                  trash.x = iter->second.x;
                  trash.y = iter->second.y;
                  trash.trashAmount = iter->second.trashAmount;

                  if(!cleared)
                  {
                      m_Trash[state].clear();
                      cleared = true;
                  }

                  m_Trash[state].push_back(trash);
              }
          }
      }

      cout<<"Trash Amount: " <<  m_Trash[state].size() << endl;

      for(unsigned int i = 0; i < m_Trash[state].size(); ++i)
      {
          const Trash& trash = m_Trash[state][i];
          SmartPointer<BaseSprite> trashSprite = new BaseSprite(trash.x,trash.y,1.0f,1.0f,"trash");
          trashSprite->addKeyFrame(new DrawSprite(trashSprite));

          turn.addAnimatable(trashSprite);

          //turn[trashList[i].id]["Owner"] = trashList[i].owner;
          turn[trash.id]["X"] = trash.x;
          turn[trash.id]["Y"] = trash.y;
          turn[trash.id]["Trash Amount"] = trash.trashAmount;
          turn[trash.id]["Type"] = "trash";
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
