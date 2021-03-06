#include "reef.h"
#include "reefAnimatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include <utility>
#include <time.h>
#include <list>
#include <iomanip>
#include <algorithm>

namespace visualizer
{
    template< class T >
    string toString(const T& data)
    {
        ostringstream stream;
        stream << data;
        return stream.str();
    }

    float GetRandFloat(float a, float b)
    {
        float fRand = rand() / (RAND_MAX + 1.0f);
        return fRand*(b - a) + a;
    }

  glm::vec4 lerp( const glm::vec4& A, const glm::vec4& B, float t )
  {
      return A*(1.0f - t) + B*t;
  }

  void StringToLower(std::string& str)
  {
      std::transform(str.begin(),str.end(),str.begin(),::tolower);
  }

  Reef::Reef() : m_fDt(0.0f)
  {
    m_game = 0;
    m_suicide=false;

    m_WaterTimer.start();
    m_BubbleTimer.start();

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
      int height = input.sy - y;

      int right = x + width;
      int bottom = y + height - SEA_OFFSET;

      R.left = min(x,right);
      R.top = min(y,bottom);
      R.right = max(x,right);
      R.bottom = max(y,bottom);
    }

  void Reef::UpdateBubbles()
  {
      int delay = (int)options->getNumber("Bubble Emitting Delay(ms)");

      if(m_BubbleTimer.elapsed() > delay )
      {
          m_BubbleTimer.restart();

          bool bEnableBubbles = options->getNumber("Enable Bubbles") > 0;
          if(bEnableBubbles /*&& m_Bubbles.size() < 120*/)
          {
              int middle = m_game->states[0].mapWidth / 2;
              int sharedLength = m_game->states[0].boundLength;

              bool bLeft = (rand() % 2 == 0);
              float xPos = middle + sharedLength;
              xPos -= 2*bLeft*sharedLength;

              glm::vec2 pos(xPos - 0.5f,m_game->states[0].mapHeight - 0.5f);
              Color color(1.0f,1.0f,1.0f,0.5f); // todo: maybe change the color of the bubbles

              float maxAge = GetRandFloat(3.0f,5.0f);
              //float angle = GetRandFloat(0.523598f,2.61799f);
              float angle = 1.570796f; // pi/2, up
              float speed = GetRandFloat(3.0f,6.0f);

              // Add a bubble to be rendered
              m_Bubbles.push_back(Bubble(pos,color,speed,angle,maxAge));
          }

      }


      for(auto iter = m_Bubbles.begin(); iter != m_Bubbles.end(); )
      {
          Bubble& bubble = *iter;

          if(bubble.Update(m_fDt))
          {
              iter = m_Bubbles.erase(iter);
          }
          else
          {
              ++iter;
          }
      }
  }

  void Reef::ProccessInput()
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


  void Reef::preDraw()
  {
      m_WaterTimer.restart();

      ProccessInput();
      UpdateBubbles();

      RenderGrid();
      RenderPreWorld();
  }


  void Reef::postDraw()
  {
      RenderPostWorld();
      RenderBubbles();
      RenderPlayerInfo();
      RenderSpecies();
      RenderObjectSelection();

      m_fDt = (m_WaterTimer.elapsed()) / 1000.0f;
  }

  void Reef::RenderGrid() const
  {
      bool bEnableGrid = options->getNumber("Enable Grid") > 0;
      if(bEnableGrid)
      {
        int h = m_game->states[0].mapHeight;
        int w = m_game->states[0].mapWidth;

        //draw horizontal lines
        renderer->setColor(Color(0.0f,0.0f,0.0f,1.0f));
        for(unsigned int i = 0; i < h; i++)
        {
            renderer->drawLine(0,i,w,i,1.0f);
        }

        //draw vertical lines
        for(unsigned int i = 0; i < w; i++)
        {
            renderer->drawLine(i,0,i,h,1.0f);
        }

      }
  }

  void Reef::RenderPlayerInfo(int id, float xPos) const
  {
      const char* name = m_game->states[0].players[id].playerName;
      int turn = timeManager->getTurn();
      int index = id + turn * 2; // index into the player info vector
      const ReefPlayerInfo& info = m_ReefPlayerInfo[index];
      float currentPercent = (float)info.currentReefHealth / (float)m_game->states[0].maxReefHealth; // current power lvl
      float foodPercent = (float)info.spawnFood / (float)m_game->states[0].maxFood; // current food

      stringstream stream;

      stream << fixed << setprecision(1) << m_ReefPlayerInfo[index].time;

      // Render AI's time
      renderer->setColor(Color(1.0f,1.0f,1.0f,1.0f));
      renderer->drawText(xPos + 5.0f,-Reef::SEA_OFFSET - 0.3f,"Roboto",name,3.0f);
      renderer->drawText(xPos,-Reef::SEA_OFFSET - 0.3f,"Roboto",stream.str(),3.0f);

      float xHealthPos = m_game->states[0].mapWidth/3.0f;

      // Health bar
      RenderProgressBar(*renderer,xPos,-SEA_OFFSET + 0.8f,xHealthPos,0.5f,currentPercent,Color(1.0f,0.0f,0.0f,1.0f),true);
      // Food bar
      RenderProgressBar(*renderer,xPos,-SEA_OFFSET + 0.55f,xHealthPos,0.25f,foodPercent,Color(0.0f,1.0f,0.0f,1.0f),true);
  }

  void Reef::RenderPlayerInfo() const
  {
      float xPos = 1.8f * m_game->states[0].mapWidth / 3.0f;

      RenderPlayerInfo(0);
      RenderPlayerInfo(1,xPos);
  }

  void Reef::RenderSpecies() const
  {
      // todo: need to make this look nice
      // todo: change these colors

      //Render season colors
      static const string seasons[] = {"winter" , "spring", "summer", "fall"};
      static const glm::vec4 seasonsColor[] =
      {
          glm::vec4(0.5f,0.5f,0.5f,0.0f), // white
          glm::vec4(.2f,0.7f,0.2f,0.0f), // greenish
          glm::vec4(.4f,0.4f,0.5f,0.0f), // silverish blue
          glm::vec4(0.7f,0.3f,0.1f,0.0f) // red-orange
      };

      int turn = timeManager->getTurn();
      int currentSeason = m_game->states[turn].currentSeason;
      int nextSeason = (currentSeason + 1) % m_Species.size();
      float seasonPercent = (turn % m_game->states[turn].seasonLength) / (float)m_game->states[turn].seasonLength;

      glm::vec4 newColor = lerp(seasonsColor[currentSeason],seasonsColor[nextSeason],seasonPercent);

      glClearColor(newColor.x,newColor.y,
                   newColor.z,newColor.w);

      renderer->setColor(Color(1.0f,1.0f,1.0f,1.0f));

      renderer->drawTexturedQuad(m_game->states[0].mapWidth / 2.0f - 1.5f, -SEA_OFFSET - 0.5f, 5,5, seasons[currentSeason]);

      //Display text for Current Selection and Next Selection of fish
      renderer->drawText(3.0f,20.4f,"Roboto","Available Fish: ",4.0f);
      renderer->drawText(24.0,20.4f,"Roboto","Next Selection: ",4.0f);

      //Display Next Season Progress Bar
      //ostringstream stream;
      //stream << "Next season begins in: " << (int)(100.0f*(1.0f - seasonPercent));
      //renderer->drawText(1.0f,22.0f,"Roboto",stream.str(),4.0f);


      for(unsigned int i = 0; i < m_Species[currentSeason].size(); ++i)
      {
          renderer->drawTexturedQuad(11.0f + 2*i,20.4f,1.5f,1.5f,m_speciesList->at(m_Species[currentSeason][i].speciesNum));
          renderer->drawTexturedQuad(32.0f + 2*i,20.4f,1.5f,1.5f,m_speciesList->at(m_Species[nextSeason][i].speciesNum));
          //renderer->drawText(13.0f + 8*i,20.0f,"Roboto",m_Species[currentSeason][i].name,2.5f,IRenderer::Center);
         // renderer->drawText(13.0f + 8*i,21.0f,"Roboto",m_Species[nextSeason][i].name,2.5f,IRenderer::Center);
      }

      RenderProgressBar(*renderer,0.0f,m_game->states[0].mapHeight, m_game->states[0].mapWidth, 0.25f,seasonPercent,Color(newColor.x,newColor.y,newColor.z,1.0f),true);

  }


  void Reef::RenderPreWorld() const
  {
      int width = m_game->states[0].mapWidth;
      int height = m_game->states[0].mapHeight;

      // draw a blue background
      renderer->setColor(Color(0.1f,0.1f,.8f,0.5f));
      renderer->drawQuad(0.0f,0.0f,width,height);

      // render the waves
      renderer->setColor(Color(1.0f,1.0f,1.0f,1.0f));

      // render the coves
      for(unsigned int i = 0; i < m_Tiles.size(); ++i)
      {
          // switch the type of the tile
          switch(m_Tiles[i].owner)
          {
            case 0:
            case 1:
              renderer->setColor(GetTeamColor(m_Tiles[i].owner));
              renderer->drawAnimQuad(m_Tiles[i].x,m_Tiles[i].y,1.0f,1.0f,"coral",2);
              // Render cove
              break;
            //case 2:
            //break;
            case 3:
              renderer->setColor(Color(1.0f,1.0f,1.0f,1.0f));
              renderer->drawTexturedQuad(m_Tiles[i].x,m_Tiles[i].y,1.0f,1.0f,"wall");
              // Render wall
              break;

          }
      }

  }


  void Reef::RenderPostWorld() const
  {
      static float counter = 0.0f;
      counter += m_fDt;

      if(counter > 53.0f)
      {
          counter = 0.0f;
      }

      // todo: change the direction of the water based on time?
      float fSeconds = (3.0f*counter) * options->getNumber("Enable Water Animation");
      float fTransparency = (float)options->getNumber("Water Transparency Level") / 100.0f;

      // render the waves
      renderer->setColor(Color(1.0f,1.0f,1.0f,1.0f));

      for(int i = 0; i < m_game->states[0].mapWidth; ++i)
      {
        renderer->drawSubTexturedQuad(i,-0.5f,0.5f,0.5f,(fSeconds),0.0f,1,1,"waves");
        renderer->drawSubTexturedQuad(i+ 0.5f,-0.5f,0.5f,0.5f,(fSeconds),0.0f,1,1,"waves");
      }

      // render the ocean floor

      for(int y = 0; y < 2*SEA_OFFSET + 1; ++y)
      {
          for (int x = 0; x < m_game->states[0].mapWidth; x++)
          {
              renderer->drawTexturedQuad(x,y + m_game->states[0].mapHeight,1,1,"ocean_floor");
          }
      }


      // blend water map ontop of all the tiles
      renderer->setColor(Color(1.0,1.0f,1.0f,fTransparency));
      renderer->drawSubTexturedQuad(0,0,m_game->states[0].mapWidth,m_game->states[0].mapHeight,(fSeconds)/53.0f,-(fSeconds)/53.0f,1.0f,1.0f,"water");

  }

  void Reef::RenderBubbles() const
  {
     for(auto iter = m_Bubbles.begin(); iter != m_Bubbles.end(); ++iter)
     {
         const Bubble& bubble = *iter;
         bubble.Render(*renderer);
     }
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
    renderer->setGridDimensions( m_game->states[0].mapWidth, m_game->states[0].mapHeight + SEA_OFFSET );

    // we must clear the previous games data
    m_selectedUnitIDs.clear();
    m_Trash.clear();

    m_Species.clear();
    m_Species.resize(4);

    m_ReefPlayerInfo.clear();
    m_ReefPlayerInfo.reserve(m_game->states.size() * 2);

    m_Bubbles.clear();

    m_Tiles.clear();

    start();
  } // Reef::loadGamelog()

  void Reef::BuildWorld(std::vector<int>& idMap)
  {
      m_Trash.resize(m_game->states.size());
      idMap.resize(m_game->states[0].tiles.size());

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
          else if(iter->second.owner < 4) // If the tile is not a water tile
          {
              m_Tiles.push_back(iter->second);
          }

          //idMap.insert(make_pair(iter->second))

          // creating a map of ids
          idMap[iter->second.y * m_game->states[0].mapWidth + iter->second.x] = iter->second.id;
      }
  }

  // The "main" function
  void Reef::run()
  {
    // Build the Debug Table's Headers
    QStringList header;
    header<<"Species" << "carryingWeight" << "Fish Health" << "Max Health" << "Attack Power" << "Trash Amount" << "X" << "Y" ;
    gui->setDebugHeader( header );
    timeManager->setNumTurns( 0 );

    animationEngine->registerGame(0, 0);

    m_speciesList = new std::vector<string>(m_game->states[0].speciesList.size());

    std::map<int,bool> dirMap;
    std::vector<int> idMap;
    BuildWorld(idMap);

    for(auto iter = m_game->states[0].speciesList.begin(); iter != m_game->states[0].speciesList.end(); ++iter)
    {
        m_Species[iter->second.season].push_back(iter->second);

        string& speciesStr = (*m_speciesList)[iter->second.speciesNum] = iter->second.name;
        StringToLower(speciesStr);
        auto spacePos = speciesStr.find(' ');

        if(spacePos != string::npos)
        {
            speciesStr[spacePos] = '_';
        }

    }

    // Look through each turn in the gamelog
    for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
    {
      Frame turn;  // The frame that will be drawn

      if(state > 0)
      {
        m_Trash[state] = m_Trash[state - 1];
      }

      // for each player in the current turn
      for( auto& p : m_game->states[ state ].players )
      {
          // todo: I could resize this vector
          m_ReefPlayerInfo.push_back(ReefPlayerInfo(p.second.currentReefHealth,p.second.spawnFood,p.second.time));

          for(auto& j : m_game->states[state].animations[p.second.id])
          {
              if(j->type == parser::SPAWN)
              {
                  //cout<<"Spawn!"<<endl;
                   parser::spawn& spawnAnim = (parser::spawn&)*j;
                   SmartPointer<BaseSprite> pSpawnAnim = new BaseSprite(glm::vec2(spawnAnim.x,spawnAnim.y), glm::vec2(1.0f,1.0f), "egg");
                   pSpawnAnim->addKeyFrame(new DrawSprite(pSpawnAnim));
                   turn.addAnimatable(pSpawnAnim);

                   cout<<"Spawn: "<<state<<endl;
              }
              else if(j->type == parser::PLAYERTALK)
              {
                  parser::playerTalk &talk = (parser::playerTalk&)*j;
                  stringstream talkstring;
                  talkstring << "(" << state << ") " << talk.message;
                  //turn[-1]["TALK"] = talkstring.str().c_str();

                  //cout<<"hello Talk"<<endl;
                  //cout<<talkstring.str() << endl;
              }
          }
      }

      // for each fish in the current turn
      for( auto& p : m_game->states[ state ].fishes )
      {
        SmartPointer<Fish> newFish = new Fish();

        newFish->addKeyFrame( new DrawFish( newFish ) );
        turn.addAnimatable(newFish);

        // for each animation each fish has
        for(auto& j : m_game->states[state].animations[p.second.id])
        {
            if(j->type == parser::ATTACK)
            {
                parser::attack& attackAnim = (parser::attack&)*j;

                auto targetIter = m_game->states[state].fishes.find(attackAnim.targetID); // get the target fish
                auto sourceIter = m_game->states[state - 1].fishes.find(attackAnim.actingID); // get the source fish

                if(targetIter != m_game->states[state].fishes.end() &&
                   sourceIter != m_game->states[state - 1].fishes.end())
                {


                    SmartPointer<MovingSpriteAnimation> pAttackAnim = new MovingSpriteAnimation(glm::vec2(sourceIter->second.x,sourceIter->second.y),
                        glm::vec2(targetIter->second.x, targetIter->second.y),glm::vec2(1.0f),"fin",2);

                    pAttackAnim->addKeyFrame( new DrawMovingAnimation( pAttackAnim ) );
                    turn.addAnimatable(pAttackAnim);

                    cout<<"Attack: "<<state<<endl;
                }
                else
                {
                    cout << "Error, fish not found"<<endl;
                }

            }
            else if(j->type == parser::MOVE)
            {
                //cout<<"Move!"<<endl;
                parser::move& move = (parser::move&)*j;
                newFish->m_moves.push_back(Fish::Moves(glm::vec2(move.toX, move.toY),glm::vec2(move.fromX, move.fromY)));
            }   
            else if(j->type == parser::DROP || j->type == parser::PICKUP)
            {
                if(j->type == parser::DROP)
                {
                    // todo: do something with the drop
                    parser::drop& dropAnim = (parser::drop&)*j;

                    if(dropAnim.amount == 0)
                    {
                        cout<<"They are dropping nothing"<<endl;
                    }
                    else
                    {
                        BasicTrash& trash = m_Trash[state][dropAnim.targetID];

                        //BasicTrash& trash = m_Trash[state][idMap[dropAnim.y * m_game->states[0].mapWidth + dropAnim.x]];
                        trash.amount += dropAnim.amount;
                        trash.x = dropAnim.x;
                        trash.y = dropAnim.y;

                        SmartPointer<MovingSpriteAnimation> pDropAnim = new MovingSpriteAnimation(glm::vec2(p.second.x,p.second.y),
                            glm::vec2(trash.x, trash.y),glm::vec2(1.0f),"trash",1);

                        pDropAnim->addKeyFrame( new DrawMovingAnimation( pDropAnim ) );
                        turn.addAnimatable(pDropAnim);
                    }
                }
                else
                {
                    parser::pickUp& pickupAnim = (parser::pickUp&)*j;
                    if(pickupAnim.amount > 0)
                    {
                        BasicTrash& trash = m_Trash[state][pickupAnim.targetID];
                        //trash.moveTurn = state;

                        if(trash.amount == 0)
                        {
                            cout<<"\n\nTurn: "<<state<<" No Trash on the tile for pickup"<<endl;
                            cout<<'('<<pickupAnim.x<<','<<pickupAnim.y<<')'<<endl<<endl;
                        }

                        trash.amount -= pickupAnim.amount;

                        if(trash.amount < 1)
                        {
                           m_Trash[state].erase(pickupAnim.targetID);
                        }

                        SmartPointer<MovingSpriteAnimation> pDropAnim = new MovingSpriteAnimation(glm::vec2(trash.x,trash.y),
                            glm::vec2(p.second.x, p.second.y),glm::vec2(1.0f),"trash",1);

                        pDropAnim->addKeyFrame( new DrawMovingAnimation( pDropAnim ) );
                        turn.addAnimatable(pDropAnim);
                    }
                }

            }
        }

        if(newFish->m_moves.empty())
        {
            newFish->m_moves.push_back(Fish::Moves(glm::vec2(p.second.x, p.second.y),glm::vec2(p.second.x, p.second.y)));

	    //take current direction of the fish
            auto iter = dirMap.find(p.second.id);
	    //permanently flips the fish for a turn
	    // todo: conditional operator can be removed
            newFish->flipped = (iter != dirMap.end() ? iter->second : false);
        }
        else if(newFish->m_moves.size() > 0)
        {
            //caching the fish's direction at end of turn
            glm::vec2 diff = (newFish->m_moves[newFish->m_moves.size() - 1].to) -
                             (newFish->m_moves[newFish->m_moves.size() - 1].from);
            dirMap[p.second.id] = diff.x > 0.0f;
        }

        // the fish is dead next turn
        // todo: check to make sure this is correct
        if( (state + 1) < (int)m_game->states.size() )
        {
          if(m_game->states[ state + 1 ].fishes.find( p.second.id ) == m_game->states[ state + 1 ].fishes.end())
          {
             if(p.second.carryingWeight > 0)
             {
                BasicTrash& trash = m_Trash[state][idMap[p.second.y * m_game->states[0].mapWidth + p.second.x]];
              	trash.amount += p.second.carryingWeight;
              	trash.x = p.second.x;
              	trash.y = p.second.y;

              }
          }
        }


        newFish->owner = p.second.owner;
        newFish->maxHealth = p.second.maxHealth;
        newFish->currentHealth = p.second.currentHealth;
        //newFish->maxMovement = p.second.maxMovement;
        //newFish->movementLeft = p.second.movementLeft;
        //newFish->carryCap = p.second.carryCap;
        //newFish->attackPower = p.second.attackPower;
        //newFish->maxAttacks = p.second.maxAttacks;
       // newFish->attacksLeft = p.second.attacksLeft;
        newFish->range = p.second.range;
        newFish->species = p.second.species;
        newFish->carryingWeight = p.second.carryingWeight;
        newFish->speciesList = m_speciesList;

        //cout<<(*speciesList)[p.second.species].c_str()<<endl;
        turn[p.second.id]["Species"] = (*m_speciesList)[p.second.species].c_str();
        turn[p.second.id]["carryingWeight"] = p.second.carryingWeight;
        turn[p.second.id]["X"] = p.second.x;
        turn[p.second.id]["Y"] = p.second.y; //carryingWeight
        turn[p.second.id]["Fish Health"] = p.second.currentHealth;
        turn[p.second.id]["Max Health"] = p.second.maxHealth;
        turn[p.second.id]["Attack Power"] = p.second.attackPower;


     }

      // Loop over all the trash in the current turn
      for(auto iter = m_Trash[state].begin(); iter != m_Trash[state].end(); ++iter)
      {
          // Draw the trash
          SmartPointer<Trash> trashSprite = new Trash(iter->second.x,iter->second.y,iter->second.amount);
          //trashSprite->moveTurn = iter->second.moveTurn;
          trashSprite->addKeyFrame(new DrawTrash(trashSprite));

          turn.addAnimatable(trashSprite);

          // Add trash to debug table
          turn[iter->first]["Species"] = "Trash";
          turn[iter->first]["Trash Amount"] = iter->second.amount;
          turn[iter->first]["X"] = iter->second.x;
          turn[iter->first]["Y"] = iter->second.y;
      }

      // When the game if over, display who won
      if( (int)m_game->states.size() == state + 1)
      {
          const char* playerName = m_game->states[state].players[m_game->winner].playerName;
          SmartPointer<SplashScreen> splashScreen = new SplashScreen(m_game->winReason,playerName,
                                                                     m_game->states[state].mapWidth,
                                                                     m_game->states[state].mapHeight
                                                                     );

          splashScreen->addKeyFrame(new DrawSplashScreen(splashScreen));

          turn.addAnimatable(splashScreen);
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
