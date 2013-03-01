#include "animations.h"
#include "reef.h"

namespace visualizer
{
  void StartAnim::animate( const float& /* t */, AnimData * /* d */, IGame* /*game*/ )
  {
  }

  void DrawSomething::animate( const float& /*t*/, AnimData * /*d*/, IGame* game )
  {
    // Set the color to red
    game->renderer->setColor( Color( 1, 0, 0, 1 ) );
    // Draw a 2x2 rectangle at (1,1), with the top left corner of the screen being the origin 
    game->renderer->drawQuad( 1, 1, 2, 2 );
  }
  
  Reef::Reef()
  {
    m_game = 0;
    m_suicide=false;
  }
  
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
    
    SeedRand();
    
    m_GUIHeight = 4;

    //CHANGE ISLANDOFFSET TO SOMETHING FOR REEF
    //renderer->setCamera( m_IslandVisualOffset, m_IslandVisualOffset, m_game->states[0].mapWidth-m_IslandVisualOffset, m_game->states[0].mapHeight+m_GUIHeight-m_IslandVisualOffset);
    renderer->setCamera( 0, 0, m_game->states[0].mapWidth+IslandOffset()*2, m_game->states[0].mapHeight+m_GUIHeight+IslandOffset()*2);
    renderer->setGridDimensions( m_game->states[0].mapWidth+IslandOffset()*2, m_game->states[0].mapHeight+m_GUIHeight+IslandOffset()*2);
    
    start();
  } // Reef::loadGamelog()

}
