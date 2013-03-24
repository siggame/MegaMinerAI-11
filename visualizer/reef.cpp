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
    template< class T >
    string toString(const T& data)
    {
        ostringstream stream;
        stream << data;
        return stream.str();
    }

  glm::vec4 lerp( const glm::vec4& A, const glm::vec4& B, float t )
  {
      return A*(1.0f - t) + B*t;
  }

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
      int y = input.y - SEA_OFFSET - 1;
      int width = input.sx - x;
      int height = input.sy - y - SEA_OFFSET - 1;

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

          for(auto& iter : m_Trash[turn])
          {
              const auto& trash = iter.second;
          
              if(trash.amount > 0)
              {
                  // todo: move this logic into another function
                  if(R.left <= trash.x && R.right >= trash.x && R.top <= trash.y && R.bottom >= trash.y)
                  {
                      m_selectedUnitIDs.push_back(iter.first);
                  }
              }
          }

          for(auto& iter : m_game->states[ turn ].fishes)
          {
              const auto& fish = iter.second;

              // todo: move this logic into another function
              if(R.left <= fish.x && R.right >= fish.x && R.top <= fish.y && R.bottom >= fish.y)
              {
                  m_selectedUnitIDs.push_back(fish.id);
              }
          }

          cout<<"Selected Units:" << m_selectedUnitIDs.size() << endl;
      }
  }

  void Reef::postDraw()
  {
      RenderPlayerInfo();
      RenderReefHealthBar();
      RenderSpecies();
      RenderWorld();
      RenderObjectSelection();
  }

  void Reef::RenderPlayerName(unsigned int id, float xPos) const
  {
      if(m_game->players[id].empty())
      {
          ostringstream stream;
          stream << "Player " << id << " Has No Name" ;

          renderer->drawText(xPos,-4.0f,"Roboto",stream.str(),4.0f);
      }
      else
      {
          renderer->drawText(xPos,-4.0f,"Roboto",this->m_game->players[id],4.0f);
      }
  }

  void Reef::RenderReefHealthBar(unsigned int id, float xPos) const
  {
      int turn = timeManager->getTurn();
      const ReefInfo& info = m_ReefInfo[id + turn * 2];

      //renderer->drawText(xPos,-3.0f,"Roboto","Reef Health:" + toString(info.currentReefHealth),4.0f);
      renderer->setColor(Color(1.0f,0.0f,0.0f,1.0f));
      renderer->drawQuad(xPos, -3.0f, info.currentReefHealth/10000.0f * m_game->states[0].mapWidth/3.0f, 3.0f);
  }

  void Reef::RenderPlayerInfo() const
  {
      float xPos = 2.0f * m_game->states[0].mapWidth / 3.0f;

      RenderPlayerName(0);
      RenderPlayerName(1,xPos);

      RenderReefHealthBar(0);
      RenderReefHealthBar(1,xPos);
  }

  void Reef::RenderSpecies() const
  {
      // todo: need to make this look nice
      // todo: change these colors
      static const string seasons[] = {"winter" , "spring", "summer", "fall"};
      static const glm::vec4 seasonsColor[] =
      {
          glm::vec4(1.0f,0.8f,0.8f,0.0f),
          glm::vec4(.2f,0.8f,0.2f,0.0f),
          glm::vec4(1.0f,0.3f,0.1f,0.0f),
          glm::vec4(.8f,0.4f,0.5f,0.0f)
      };

      int turn = timeManager->getTurn();
      int currentSeason = m_game->states[turn].currentSeason;
      int nextSeason = (currentSeason + 1) % m_Species.size();
      float seasonPercent = (turn % m_game->states[turn].seasonLength) / (float)m_game->states[turn].seasonLength;

      glm::vec4 newColor = lerp(seasonsColor[currentSeason],seasonsColor[nextSeason],seasonPercent);

      glClearColor(newColor.x,newColor.y,
                   newColor.z,newColor.w);

      renderer->drawText(1.0f,20.0f,"Roboto","Current Selection: ",4.0f);
      renderer->drawText(1.0,21.0f,"Roboto","Next Selection: ",4.0f);

      ostringstream stream;
      stream << "Next season begins in: " << 100.0f*(1.0f - seasonPercent);
      renderer->drawText(1.0f,22.0f,"Roboto",stream.str(),4.0f);

      for(unsigned int i = 0; i < m_Species[currentSeason].size(); ++i)
      {
          renderer->drawText(12.0f + 8*i,20.0f,"Roboto",m_Species[currentSeason][i].name,4.0f,IRenderer::Center);
          renderer->drawText(12.0f + 8*i,21.0f,"Roboto",m_Species[nextSeason][i].name,4.0f,IRenderer::Center);
      }
  }

  void Reef::RenderWorld() const
  {
      // todo: change the direction of the water based on time?
      float fSeconds = m_WaterTimer.elapsed() / 1000.0f * options->getNumber("Enable Water Animation");
      float fTransparency = (float)options->getNumber("Water Transparency Level") / 100.0f;

      renderer->setColor(Color(1.0f,1.0f,1.0f,1.0f));
      for(unsigned int i = 0; i < m_game->states[0].mapWidth; ++i)
      {
        renderer->drawSubTexturedQuad(i,-1.0f,1.0f,1.0f,(fSeconds)/2.0f,0.0f,1,1,"waves");
      }

      //renderer->drawTexturedQuad(0,-2,m_game->states[0].mapWidth,2,"waves");

      // blend water map ontop of all the tiles
      renderer->setColor(Color(1.0,1.0f,1.0f,fTransparency));
      renderer->drawSubTexturedQuad(0,0,m_game->states[0].mapWidth,m_game->states[0].mapHeight,(fSeconds)/53.0f,-(fSeconds)/53.0f,1.0f,1.0f,"water");

  }

  void Reef::RenderObjectSelection() const
  {
      // render object selection
      // todo: put this code into its own method.
      int turn = timeManager->getTurn();

      for(auto iter = m_selectedUnitIDs.begin(); iter != m_selectedUnitIDs.end(); ++iter)
      {
        // If polymorphism was used, we would not have to search both lists.....................
        if(!DrawQuadAroundObj(m_Trash[turn],*iter))
        {
          DrawQuadAroundObj(m_game->states[turn].fishes,*iter);
        }
      }
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

    // we must clear the previous games data
    m_selectedUnitIDs.clear();
    m_Trash.clear();

    m_Species.clear();
    m_Species.resize(4);

    m_ReefInfo.clear();
 
    start();
  } // Reef::loadGamelog()

  void Reef::BuildWorld(Map* pMap)
  {
      m_Trash.resize(m_game->states.size());

      // Loop over all of the tiles in the first turn
      for(auto iter = m_game->states[0].tiles.begin(); iter != m_game->states[0].tiles.end(); ++iter)
      {
          // if there is trash
          if(iter->second.trashAmount > 0)
          {
            // add it
            BasicTrash trash;
            trash.x = iter->second.x;
            trash.y = iter->second.y;
            trash.amount = iter->second.trashAmount;

            m_Trash[0][iter->second.id] = trash;
          }
          else if(iter->second.owner < 2) // If the tile is not a water tile
          {
              // it is a cove, so draw it
              Map::Tile& tile = (*pMap)(iter->second.y,iter->second.x);
              tile.bCove = true;
              tile.spriteId = 2;
          }

      }

      // Draw other coral on the bottom of the map.
      for (int x = 0; x < pMap->GetWidth(); x++)
      {
         Map::Tile& tile = (*pMap)(pMap->GetHeight() - 1,x);
         tile.bCove = true;
         tile.spriteId = rand() % 2;
      }

  }
  
  // The "main" function
  void Reef::run()
  {
    // Build the Debug Table's Headers
    QStringList header;
    header<<"Species" << "Trash Amount" << "X" << "Y" /*<< "Owner" << "Type"*/;
    gui->setDebugHeader( header );
    timeManager->setNumTurns( 0 );

    animationEngine->registerGame(0, 0);

    SmartPointer<Map> pMap = new Map(m_game->states[0].mapWidth,m_game->states[0].mapHeight);
    pMap->addKeyFrame( new DrawMap( pMap ) );

    BuildWorld(pMap);

    for(auto iter = m_game->states[0].species.begin(); iter != m_game->states[0].species.end(); ++iter)
    {
        m_Species[iter->second.season].push_back(iter->second);
    }

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

      // for each player in the current turn
      for( auto& p : m_game->states[ state ].players )
      {
          // todo: I could resize this vector
          m_ReefInfo.push_back(ReefInfo(p.second.currentReefHealth,p.second.spawnFood));
          /*SmartPointer<HUDInfo> hud = new HUDInfo(p.second.id - 800,p.second.currentReefHealth,p.second.spawnFood);
          hud->addKeyFrame( new DrawHUD( hud ) );
          turn.addAnimatable(hud);*/
      }

      // for each fish in the current turn
      for( auto& p : m_game->states[ state ].fishes )
      {
        SmartPointer<Fish> newFish = new Fish();

        // for each animation each fish has
        for(auto& j : m_game->states[state].animations[p.second.id])
        {
            cout<<"Turn: "<<state<<" animation:"<<j->type<<endl;
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
                     // todo: do something with the drop
                    parser::drop& dropAnim = (parser::drop&)*j;
                    BasicTrash& trash = m_Trash[state][dropAnim.targetID];

                    trash.amount += dropAnim.amount;
                    trash.x = dropAnim.x;
                    trash.y = dropAnim.y;

                }
                else
                {
                    //todo: do something with the pickup

                    parser::pickUp& pickupAnim = (parser::pickUp&)*j;
                    BasicTrash& trash = m_Trash[state][pickupAnim.targetID];

                    trash.amount -= pickupAnim.amount;
                    
                    if(trash.amount < 1)
                    {
                        m_Trash[state].erase(pickupAnim.targetID);
                    }
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

        //turn[p.second.id]["Owner"] = p.second.owner;
        //turn[p.second.id]["Type"] = "fish";
        turn[p.second.id]["Species"] = p.second.species;
        turn[p.second.id]["X"] = p.second.x;
        turn[p.second.id]["Y"] = p.second.y;


        newFish->addKeyFrame( new DrawFish( newFish ) );
        turn.addAnimatable(newFish);
        //cout<<"created a fish! "<<newFish->m_moves[0].from.x<<endl;

     }

      //cout<<"Trash Amount: " <<  m_Trash[state].size() << endl;

      // this code does not do anything
     /* for(auto iter = m_game->states[state].tiles.begin(); iter != m_game->states[state].tiles.end(); ++iter)
      {
          if(iter->second.trashAmount > 0)
          {
              // Draw the trash
              SmartPointer<Trash> trashSprite = new Trash(iter->second.x,iter->second.y,iter->second.trashAmount);
              trashSprite->addKeyFrame(new DrawTrash(trashSprite));

              turn.addAnimatable(trashSprite);

              //turn[trashList[i].id]["Owner"] = trashList[i].owner;

              // Add trash to debug table
              turn[iter->first]["Species"] = "Trash";
              turn[iter->first]["Trash Amount"] = iter->second.trashAmount;
              turn[iter->first]["X"] = iter->second.x;
              turn[iter->first]["Y"] = iter->second.y;
          }
      }*/

      // Loop over all the trash in the current turn
      for(auto iter = m_Trash[state].begin(); iter != m_Trash[state].end(); ++iter)
      {
          // Draw the trash
          SmartPointer<Trash> trashSprite = new Trash(iter->second.x,iter->second.y,iter->second.amount);
          trashSprite->addKeyFrame(new DrawTrash(trashSprite));

          turn.addAnimatable(trashSprite);

          //turn[trashList[i].id]["Owner"] = trashList[i].owner;

          // Add trash to debug table
          turn[iter->first]["Species"] = "Trash";
          turn[iter->first]["Trash Amount"] = iter->second.amount;
          turn[iter->first]["X"] = iter->second.x;
          turn[iter->first]["Y"] = iter->second.y;

          //turn[iter->first]["Type"] = "trash";
      }

      /*SmartPointer<HUDInfo> pHud = new HUDInfo(m_game->states[state].currentSeason);
      pHud->addKeyFrame(new DrawHUD(pHud));
      turn.addAnimatable(pHud);*/

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
