#include "${lowercase(gameName)}.h"
#include "${lowercase(gameName)}Animatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include <utility>
#include <time.h>
#include <list>

namespace visualizer
{
  ${gameName}::${gameName}()
  {
    m_game = 0;
    m_suicide=false;
  } // ${gameName}::${gameName}()

  ${gameName}::~${gameName}()
  {
    destroy();
  }

  void ${gameName}::destroy()
  {
    m_suicide=true;
    wait();
    animationEngine->registerGame(0, 0);

    clear();
    delete m_game;
    m_game = 0;
    
    // Clear your memory here
    
    programs.clear();

  } // ${gameName}::~${gameName}()

  void ${gameName}::preDraw()
  {
    const Input& input = gui->getInput();
    
    // Handle player input here
  }

  void ${gameName}::postDraw()
  {
    if( renderer->fboSupport() )
    {
#if 0
      renderer->useShader( programs["post"] ); 
      renderer->swapFBO();
      renderer->useShader( 0 );
#endif

    }
  }


  PluginInfo ${gameName}::getPluginInfo()
  {
    PluginInfo i;
    i.searchLength = 1000;
    i.gamelogRegexPattern = "${gameName}";
    i.returnFilename = false;
    i.spectateMode = false;
    i.pluginName = "MegaMinerAI: ${gameName} Plugin";


    return i;
  } // PluginInfo ${gameName}::getPluginInfo()

  void ${gameName}::setup()
  {
    gui->checkForUpdate( "${gameName}", "./plugins/${lowercase(gameName)}/checkList.md5", VERSION_FILE );
    options->loadOptionFile( "./plugins/${lowercase(gameName)}/${lowercase(gameName)}.xml", "${lowercase(gameName)}" );
    resourceManager->loadResourceFile( "./plugins/${lowercase(gameName)}/resources.r" );
  }
  
  // Give the Debug Info widget the selected object IDs in the Gamelog
  list<int> ${gameName}::getSelectedUnits()
  {
    // TODO Selection logic
    return list<int>();  // return the empty list
  }

  void ${gameName}::loadGamelog( std::string gamelog )
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
    renderer->setCamera( 0, 0, 4, 4 );
    renderer->setGridDimensions( 4, 4 );
 
    start();
  } // ${gameName}::loadGamelog()
  
  // The "main" function
  void ${gameName}::run()
  {
    
    // Build the Debug Table's Headers
    QStringList header;
    header << "one" << "two" << "three";
    gui->setDebugHeader( header );
    timeManager->setNumTurns( 0 );

    animationEngine->registerGame(0, 0);

    // Look through each turn in the gamelog
    for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
    {
      Frame turn;  // The frame that will be drawn
      SmartPointer<Something> something = new Something();
      something->addKeyFrame( new DrawSomething( something ) );
      turn.addAnimatable( something );
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
    }
    
    if(!m_suicide)
    {
      timeManager->setNumTurns( m_game->states.size() );
      timeManager->play();
    }

  } // ${gameName}::run()

} // visualizer

Q_EXPORT_PLUGIN2( ${gameName}, visualizer::${gameName} );
